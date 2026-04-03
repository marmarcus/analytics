import pandas as pd
import json

# Function that will look through object's keys and check if its a list or string.
# If list -> continue
# If string -> turn into list
# If N/A -> turn to null
def make_list(x):
    if isinstance(x, list):
        return x
    elif isinstance(x, str):
        if x == "N/A":
            return []
        return [key for key in x.split(',')]
    return []

# Read CSV file 
df = pd.read_json('job_data2.json')

#print(df.columns)
# Index(['ID', 'location', 'date', 'years_experience', 'salary', 'in-person/remote/hybrid', 'fulltime/parttime/internship', 'programming_languages', 'tools']

# Remove any rows where the ID does not contain the correctly generated string
# Afterwards, reset the index to completely remove it from the count
df.drop(df[~df.ID.str.contains(r'^in-[0-9a-zA-Z]+')].index, inplace=True)
df = df.reset_index(drop=True)

# Go through all values in the locations column to ensure any value that should be a list is a separate string
for i, x in enumerate(df['location']): 
    df.at[i, 'location'] = make_list(x)


# If YOE is, for example, '4+' or '1-3+' then it will change it to only '4' or '1-3' because that automatically assumes AT LEAST that amount YOE anyways
df['years_experience'] = df['years_experience'].str.replace(r'[a-zA-Z+]', '', regex=True)




# Go through all values in the tools column to ensure any value that should be a list is a separate string
# Ex: tools: "word, excel, powerpoint"  -->  tools: ["word", "excel", "powerpoint"]
for i, x in enumerate(df['tools']): 
    df.at[i, 'tools'] = make_list(x)
