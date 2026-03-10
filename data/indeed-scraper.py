# Webscraper using Jobspy to grab job postings from Indeed based on various parameters and output into an Excel sheet

import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed"],
    search_term="data analyst",
    location="Santa Ana, CA",
    distance=90,
    results_wanted=30,
    hours_old=168,
    country_indeed='USA',
)

output = jobs[['id', 'job_url_direct', 'date_posted', 'location', 'title', 'description']]

print(f"Found {len(jobs)} jobs")
output.to_csv("jobs.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) 

