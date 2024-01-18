from django.db import models
from django.contrib.auth.models import AbstractUser
from openai import ChatCompletion
import os
from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Filter(models.Model):
    age = models.CharField(max_length=300)
    gender = models.CharField(max_length=300)
    relationship = models.CharField(max_length=300)
    price_range = models.CharField(max_length=300)
    occasion = models.CharField(max_length=300)
    gift_type = models.CharField(max_length=300)
    interest = models.CharField(max_length=300)
    activity_level = models.CharField(max_length=300)
    personality = models.CharField(max_length=300)
    nature = models.CharField(max_length=300)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="filters", blank=True, null=True)
    output_text = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now())
    item_title_string = models.TextField(default='')
    item_descrip_string = models.TextField(default='')
    openai_descrip_string = models.TextField(default='')
    item_title_array = []
    item_descrip_array = []
    openai_descrip_array = []

    class FilterManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().order_by('created_at')

    def __str__(self):
        return str(self.id)

    def parsingFunc(self, string1):

        # Clears string and arrays each time we send a POST and GET a request back from OpenAI
        self.item_descrip_string = ""
        self.item_title_string = ""
        self.openai_descrip_string = ""
        self.item_descrip_array = []
        self.item_title_array = []
        self.openai_descrip_array = []

        # Parsed output_text response to initial array that will be used for further parsing
        if (string1.count("\n\n") >= 3):
            parsedArray = str(string1).split("\n\n")
        else:
            parsedArray = str(string1).split("\n")
        # Parsed array length
        parsedArrayLen = len(parsedArray)
        items_and_descrip_Array = []

        # Appending openAI general description of responses
        self.openai_descrip_array.append(parsedArray[0])
        self.openai_descrip_array.append(parsedArray[parsedArrayLen-1])

        # Get rid of first and last item of intial array that contains openAI general description of responses already stored in separate array above
        parsedArray.pop(0)
        parsedArray.pop(len(parsedArray)-1)

        # Parse array one extra step to get rid of item number
        for items in parsedArray:
            updatedString = items[3:]
            items_and_descrip_Array.append(updatedString)

        # Final parse to respective arrays for item titles and item descriptions
        for x in items_and_descrip_Array:
            indexAt = x.find(":")
            # This if will catch the ValueError: substring not found. Arrays are parsed correctly but when items are separated by only one '\n' then
            # extra index at the front of the array and at the last element. They are empty strings and do not contain ":". Since the .find() will return a -1
            # if not found, then it will not append the blank strings.
            if (indexAt != -1):
                self.item_title_array.append(x[0:indexAt])
                self.item_descrip_array.append(x[indexAt+2:])

        # Remove leading white space on item 10. Keep line if items is 10 or more
        if len(self.item_title_array) >= 10:
            self.item_title_array[len(
                self.item_title_array)-1] = self.item_title_array[len(self.item_title_array)-1].lstrip(" ")

        # Join all elements of parsed arrays into separate strings to have ready to pass over to front end.
        self.item_title_string = ",".join(self.item_title_array)
        # The * seperates each description, and allows us to parse each description to its own response card
        self.item_descrip_string = "*".join(self.item_descrip_array)
        self.openai_descrip_string = ",".join(self.openai_descrip_array)
        # print(self.item_descrip_string)
        # print(self.item_title_string)
        # print(self.openai_descrip_string)

    def send_filters(self):
        # Load environment variables from a .env file in the current directory
        load_dotenv()
        filters_input = f'Consider the following details about the recipient: they are a {self.age}, identify as {self.gender}, they are my {self.relationship}, my price range is {self.price_range}, the occasion this gift is for is {self.occasion}, I want to give them a {self.gift_type}, their main interest is {self.interest}, and their activity level is {self.activity_level}. They are {self.personality} and they prefer being {self.nature}.Please provide a curated list of 10 diverse and thoughtful gift suggestions that take into account all the specified characteristics.'

        MODEL = "gpt-3.5-turbo"

        response = ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an AI-powered gift advisor assisting users in selecting the perfect gift for their loved ones."},
                {"role": "user", "content": filters_input}
            ],
            temperature=1,
            api_key=os.environ.get('OPENAI_API_KEY')
        )
        # print(response.choices[0].message.content)

# # Access the generated content
#         try:
#             generated_content = response['choices'][0]['message']['content']
#         except KeyError:
#     # Handle the case where the structure of the response is different
#             generated_content = str(response)

        self.output_text = response.choices[0].message.content
        self.parsingFunc(self.output_text)
        print(self.created_at)
        self.created_at = (self.created_at - timedelta(hours=5))
        print(self.created_at)
        self.save()