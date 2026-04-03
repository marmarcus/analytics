# Using Gemini 3.1 Flash Lite 
# This program will take the input from values in a previously generated Excel sheet as run it through the AI to extract various data parameters in JSON form

from google import genai
from dotenv import load_dotenv
import pandas as pd
import os
import json
import time

# Function which contains the prompt for Gemini to analyze
def analyze_description(posts, id_number, location, date):
    prompt = f"""
             Each job description contains and ID followed by its description text.
 
             Analyze the description and extract structured information that is applicable to each specified field.
             Do not add the same item to multiple fields.

             The output will be put in a JSON file so ONLY return a JSON array with a object matching each field and NOTHING else in the SAME ORDER as the descriptions.
             The output must be formatted for JSON.

             Do not use parentheses for any reason whether its to give an acronym or to group tools or programming languages for example, Microsoft Office (Word, Excel, Powerpoint) should instead list either "Microsoft Office" OR "Word", "Excel", "Powerpoint".

             Programming languages include things like Python, SQL, R, Java, C++, etc.

             Tools include software platforms such as Tableau, Power BI, Excel, AWS, Docker, Airflow, Kubernetes, etc.

             If listing out multiple keys for the fields programming_languages and tools, each item must be its own key. For example this is incorrect: "tools": "Claude, Stable Diffusion". It has to be "tools": ["Claude", "Stable Diffusion"]

             If a requirement is being currently enrolled then it is an internship.
             
             If a field cannot be determined, return N/A into the field.

             JSON Fields:
             - ID
             - location
             - date
             - years_experience
             - salary
             - in-person/remote/hybrid
             - fulltime/parttime/internship
             - programming_languages
             - tools

             The output must ONLY be formatted for JSON.

             Id:
             {id_number}

             Location:
             {location}

             Date:
             {date}

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
df = pd.read_csv('job_scraper/jobs.csv')

descriptions = df['description'] # Get all description column cells
id_number = df['id'] # Get all ids from column cells
location = df['location'] # Get all location from column cells
date = df['date_posted'] # Get all posting dates from column cells

# File defined for output
output_file = "job_data2.json"

# Check for output file, create if doesn't exist
if not os.path.exists(output_file):
    with open(output_file, "w") as file:
        json.dump([], file)

# Loop through all the cells from 0 to end of descriptions array
for i in range(len(descriptions)):
    # Start outputting results to JSON file 

    # Get the data from the JSON file
    with open(output_file, "r") as file:
        data = json.load(file)

    # Check for any existing keys to prevent duplicates
    existing_keys = {item["ID"] for item in data}

    # If current id already exists within the JSON file, then skip to the next id
    if id_number[i] in existing_keys:
        print(f"Skipped existing ID - {id_number[i]}")
        continue

    results = analyze_description(descriptions[i], id_number[i], location[i], date[i])    

    # Append results to the end of the JSON file
    data.extend(results)

    # Write to JSON file
    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)

    # 5 seconds between API call because of limit on tokens per minute
    time.sleep(7)