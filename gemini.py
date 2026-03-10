# Using Gemini 3.1 Flash Lite 
# This program will take the input from values in a previously generated Excel sheet as run it through the AI to extract various data parameters in JSON form

from google import genai
from dotenv import load_dotenv
import pandas as pd
import os
import json

# Get API key from .env
#load_dotenv()

#api_key = os.getenv("GEMINI_API_KEY")
#client = genai.Client(api_key=api_key)

# Read CSV file 
df = pd.read_csv('data/jobs.csv')
descriptions = df['description'] # All description cells
window = 5 # Amount of cells the AI will go through at a time 



#response = client.models.generate_content(
#    model="gemini-3.1-flash-lite-preview", 
#    contents="Explain how AI works in a few words"
#)

#print(response.text)
