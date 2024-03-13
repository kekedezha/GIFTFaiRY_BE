from django.db import models
from django.contrib.auth.models import AbstractUser
from openai import ChatCompletion
import os
from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class User(AbstractUser):

    uid = models.CharField(max_length=300, null=True)
    password = models.CharField(max_length=300, null=True, blank=True)
    username = models.CharField(
        max_length=300, null=True, blank=True, unique=True)
    email = models.CharField(max_length=300, null=True,
                             blank=True, unique=True)

    pass

    def __str__(self):
        return self.username

    def saveToUserDatabase(self):
        self.save()


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
    giftee_name = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="filters", blank=True, null=True)
    email = models.CharField(max_length=300, default='')
    output_text = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)
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

    def getUserInstance(self):
        userInstance = User.objects.get(email=self.email)
        return userInstance

    # Function to parse OpenAIs response if response is a numbered list.
    def numberedListParsing(self, openAIResponseString):
        # Clears string and arrays each time we send a POST and GET a request back from OpenAI
        self.item_descrip_string = ""
        self.item_title_string = ""
        self.openai_descrip_string = ""
        self.item_descrip_array = []
        self.item_title_array = []
        self.openai_descrip_array = []

        # For the incoming string, separate the string into an array to start parsing.
        if (openAIResponseString.count("\n\n") >= 3):
            parsedArray = str(openAIResponseString).split("\n\n")
        else:
            parsedArray = str(openAIResponseString).split("\n")
        # Create array that will hold the string with the list of items after the numerical value has been cleared
        items_and_descrip_Array = []

        # Parse array one extra step to get rid of item number
        for items in parsedArray:
            updatedString = items[3:]
            items_and_descrip_Array.append(updatedString)

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
        self.item_title_string = ", ".join(self.item_title_array)
        # The * separates each description, and allows us to parse each description to its own response card
        self.item_descrip_string = "*".join(self.item_descrip_array)
        self.openai_descrip_string = ",".join(self.openai_descrip_array)

    # Function to parse OpenAIs response if response has extra content that is unnecessary for the user.
    # Function may not be used anymore as of 3/8/2024. Updated API call to specify response back from OpenAI
    def parseIfBeginNormal(self, openAIResponseString):
        # Clears string and arrays each time we send a POST and GET a request back from OpenAI
        self.item_descrip_string = ""
        self.item_title_string = ""
        self.openai_descrip_string = ""
        self.item_descrip_array = []
        self.item_title_array = []
        self.openai_descrip_array = []

        # Parsed output_text response to initial array that will be used for further parsing
        if (openAIResponseString.count("\n\n") >= 3):
            parsedArray = str(openAIResponseString).split("\n\n")
        else:
            parsedArray = str(openAIResponseString).split("\n")
        # Parsed array length
        parsedArrayLen = len(parsedArray)
        items_and_descrip_Array = []

        # Appending openAI general description of responses
        self.openai_descrip_array.append(parsedArray[0])
        self.openai_descrip_array.append(parsedArray[parsedArrayLen-1])

        # Get rid of first and last item of initial array that contains openAI general description of responses already stored in separate array above
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

        # Reduce all item descriptions to only one sentence.
        self.itemDescriptionParse(self.item_descrip_array)

        # Remove leading white space on item 10. Keep line if items is 10 or more
        if len(self.item_title_array) >= 10:
            self.item_title_array[len(
                self.item_title_array)-1] = self.item_title_array[len(self.item_title_array)-1].lstrip(" ")

        # Join all elements of parsed arrays into separate strings to have ready to pass over to front end.
        self.item_title_string = ", ".join(self.item_title_array)
        # The * separates each description, and allows us to parse each description to its own response card
        self.item_descrip_string = "*".join(self.item_descrip_array)
        self.openai_descrip_string = ",".join(self.openai_descrip_array)

    # Function to clear asterisks in item title
    def clearAsterisk(self, string):
        if string.count("**") >= 1:
            self.item_title_string = string.replace("**", "")
        elif string.count("*") >= 1:
            self.item_title_string = string.replace("*", "")

    # Function to limit item description to one sentence for better visualization in UI
    def itemDescriptionParse(self, itemDescriptionArray):
        # Loop through item_descrip_array
        for description in itemDescriptionArray:
            #
            description = description.split(".")[0]
            print(description)

    def send_filters(self):
        # Load environment variables from a .env file in the current directory
        load_dotenv()
        # Updated end of string to specify a list of ideas.
        # -Christian Dezha 3/8/2024
        filters_input = f'Consider the following details about the recipient: they are a {self.age}, identify as {self.gender}, they are my {self.relationship}, my price range is {self.price_range}, the occasion this gift is for is {self.occasion}, I want to give them a {self.gift_type}, their main interest is {self.interest}, and their activity level is {self.activity_level}. They are {self.personality} and they prefer being {self.nature}. Please provide a curated list of 10 diverse and thoughtful gift suggestions that take into account all the specified characteristics. Please cater the gift suggestions to retail products, do not suggest live events or anything else that is not a physical product. Lastly, please make sure to list all gift ideas separate them and their descriptions by a colon (:) and not by a dash (-).'

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

        self.output_text = response.choices[0].message.content

        # if the response we get back from OpenAI beings with "1. ... 2..." then parse with the following method
        if (self.output_text[0] == '1'):
            print("Parsing with 'parseIfBeginWithNum' method")
            self.numberedListParsing(self.output_text)
        # Else if the response we get back from OpenAI beings with "Based on..." or some other text then parse normally
        else:
            print("Parsing normally")
            self.parseIfBeginNormal(self.output_text)

        # If the Item Title String contains any asterisks then parse the strings and take out the asterisks
        if self.item_title_string.count("**") >= 1 or self.item_title_string.count("*") >= 1:
            self.clearAsterisk(self.item_title_string)

        userInstance = User.objects.get(email=self.email)
        self.user = userInstance
        self.save()
