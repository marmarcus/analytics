# Webscraper using Jobspy to grab job postings from Indeed based on various parameters and output into an Excel sheet
import os
import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed"],
    search_term="data analyst",
    location="Las Vegas, NV",
    distance=90,
    results_wanted=50,
    hours_old=168,
    country_indeed='USA',
)

# Column headers for each job
output = jobs[['id', 'job_url_direct', 'date_posted', 'location', 'title', 'description']]

print(f"Found {len(jobs)} jobs")

# Get file to check if it already exists
file_exists = os.path.isfile("jobs.csv")

output.to_csv("job_scraper/jobs.csv",
              mode = 'a',
              quoting=csv.QUOTE_NONNUMERIC,
              escapechar="\\", 
              index=False,
              header=not file_exists) 

