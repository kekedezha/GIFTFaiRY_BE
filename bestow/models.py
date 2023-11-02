from django.db import models
from django.contrib.auth.models import AbstractUser
import openai
import os
from dotenv import load_dotenv
from django.contrib.postgres.fields import ArrayField


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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="filters", blank=True, null=True)
    output_text = models.TextField(default='')
    item_title_array = []
    item_descrip_array = []
    openai_descrip_array = []

    def __str__(self):
        return str(self.id)
    
    def parsingFunc(self, string1):
        #Parsed output_text response to initial array that will be used for further parsing
        parsedArray = str(string1).split("\n\n")
        items_and_descrip_Array = []
        
        #Appending openAI general description of responses
        self.openai_descrip_array.append(parsedArray[0])
        self.openai_descrip_array.append(parsedArray[0])  

        #Get rid of first and last item of intial array that contains openAI general description of responses already stored in separate array above
        parsedArray.pop(0)
        parsedArray.pop(len(parsedArray)-1)

        #Parse array one extra step to get rid of item number
        for items in parsedArray:
            updatedString = items[3:]
            items_and_descrip_Array.append(updatedString)

        #Final parse to respective arrays for item titles and item descriptions
        for x in items_and_descrip_Array:
            indexAt = x.index(":")
            print(indexAt)
            self.item_title_array.append(x[0:indexAt])
            self.item_descrip_array.append(x[indexAt+2:])

        #Remove leading white space on item 10. Keep line if items is 10 or more
        if len(self.item_title_array) >= 10: 
            self.item_title_array[len(self.item_title_array)-1] = self.item_title_array[len(self.item_title_array)-1].lstrip(" ")

        print(self.item_descrip_array)
        print(self.item_title_array)

    def send_filters(self):
        # Load environment variables from a .env file in the current directory
        load_dotenv()
        filters_input = f'You are a tool that helps people buy gifts for others. Suggest 10 ideal gifts for somebody with these characteristics and traits, they are {self.age} years old, their gender identify is {self.gender}, they are my {self.relationship}, my price range is {self.price_range}, the occasion this gift is for is {self.occasion}, I want to give them a {self.gift_type}, their main interest is {self.interest}. Please take all parameters into equal consideration.'

        MODEL = "gpt-3.5-turbo"
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "system",
                    "content": "You are a helpful assistant"},
                {"role": "user", 
                 "content": filters_input}
            ],
            temperature=0.8,
        )
        self.output_text = response['choices'][0]['message']['content']
        self.save()
        self.parsingFunc(self.output_text)