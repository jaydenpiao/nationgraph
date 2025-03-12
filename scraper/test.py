from firecrawl import FirecrawlApp
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import csv

load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

class ExtractSchema(BaseModel):
    dataset_titles: list[str]
    doi_urls: list[str]
    number_of_datasets: int

class ExtractSchemaDataSet(BaseModel):
    description: str
    subject: list[str]
    keyword: str

all_titles = []
doi_urls = []

# loop through page 1 (adjust range as needed)
for page in range(1, 3):
    url = f'https://dataverse.harvard.edu/dataverse/harvard?q=&types=datasets&page={page}&sort=dateSort&order=desc'
    data = app.scrape_url(url, {
        'formats': ['json'],
        'jsonOptions': {
            'schema': ExtractSchema.model_json_schema(),
        }
    })
    json_data = data.get("json", {})
    print(f"Page {page} JSON: {json_data}")
    titles = json_data.get("dataset_titles", [])[:2] # capped at 2 per page
    dois = json_data.get("doi_urls", [])[:2]
    all_titles.extend(titles)
    doi_urls.extend(dois)

dataset_info = []
# all_titles = all_titles[:3]
# doi_urls = doi_urls[:3]


for title, doi in zip(all_titles, doi_urls):
    doi_part = doi.replace("https://doi.org/", "doi:")
    dataset_page_url = f"https://dataverse.harvard.edu/dataset.xhtml?persistentId={doi_part}"
    print(f"Scraping dataset page: {dataset_page_url}")
    
    ds_data = app.scrape_url(dataset_page_url, {
        'formats': ['json'],
        'jsonOptions': {
            'schema': ExtractSchemaDataSet.model_json_schema(),
        }
    })
    json_data = ds_data.get("json", {})
    
    description = json_data.get("description", "")
    subject = json_data.get("subject", [])
    keyword = json_data.get("keyword", "")
    
    dataset_info.append({
         "Title": title,
         "DOI URL": doi,
         "Description": description,
         "Subject": ", ".join(subject) if subject else "",
         "Keyword": keyword
    })

os.makedirs("data", exist_ok=True)
csv_file_path = os.path.join("data", "titles.csv")

with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["Title", "DOI URL", "Description", "Subject", "Keyword"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in dataset_info:
         writer.writerow(row)

print(f"Data written to {csv_file_path}")
