from django.db import models
from django.contrib.auth.models import AbstractUser
import openai
import os
from dotenv import load_dotenv
# import environ

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

    def __str__(self):
        return str(self.id)

    def send_filters(self):
        # Load environment variables from a .env file in the current directory
        load_dotenv()
        filters_input = f'You are a tool that helps people buy gifts for others. Suggest 10 ideal gifts for somebody with these characteristics and traits, they are {self.age} years old, their gender identify is {self.gender}, they are my {self.relationship}, my price range is {self.price_range}, the occasion this gift is for is {self.occasion}, I want to give them a {self.gift_type}, their main interest is {self.interest}. Please take all parameters into equal consideration.'
        # env = environ.Env()
        # environ.Env.read_env()
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