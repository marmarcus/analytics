# Using Gemini 3.1 Flash Lite 
# This program will take the input from values in a previously generated Excel sheet as run it through the AI to extract various data parameters in JSON form

from google import genai
from dotenv import load_dotenv
import pandas as pd
import os
import json
import time

# Function which contains the prompt for Gemini to analyze
def analyze_description(posts, id_number):
    prompt = f"""
             Each description contains and ID followed by its description text.
 
             Analyze the description and extract structured information that is applicable to each specified field.
             Do not add the same item to multiple fields.

             The output will be put in a JSON file so ONLY return a JSON array with a object matching each field and NOTHING else in the SAME ORDER as the descriptions.
             The output must be formatted for JSON.

             Programming languages include things like Python, SQL, R, Java, C++, etc.

             Tools include software platforms such as Tableau, Power BI, Excel, AWS, Docker, Airflow, Kubernetes, etc.
             
             If a field cannot be determined, return N/A into the field.

             JSON Fields:
             - ID
             - years_experience 
             - programming_languages
             - tools

             The output must ONLY be formatted for JSON.

             Id:
             {id_number}

             {id_number}'s Description:
             {posts}
             """
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite-preview',
        contents=prompt
    )

    return json.loads(response.text)

#Get API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Read CSV file 
df = pd.read_csv('data/jobs.csv')

descriptions = df['description'] # Get all description column cells
id_number = df['id'] # Get all ids from column cells
window_size = 1 # Amount of cells the AI will go through at a time 

# File defined for output
output_file = "job_data.json"

# Check for output file, create if doesn't exist
if not os.path.exists(output_file):
    with open(output_file, "w") as file:
        json.dump([], file)

# Loop through all the cells from 0 to end of descriptions array
for i in range(len(descriptions)):
    results = analyze_description(descriptions[i], id_number[i])

    # Start outputting results to JSON file 

    # Get the data from the JSON file
    with open(output_file, "r") as file:
        data = json.load(file)
    
    # Append results to the end of the JSON file
    data.extend(results)

    # Write to JSON file
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)

    # 4 seconds between API call because of limit on tokens per minute
    time.sleep(4)