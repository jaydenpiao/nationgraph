from firecrawl import FirecrawlApp
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
import csv

load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

class ExtractSchema(BaseModel):
    dataset_titles: list[str]
    number_of_datasets: int

data = app.scrape_url('https://dataverse.harvard.edu/dataverse/harvard?q=&types=datasets&page=1&sort=dateSort&order=desc', {
    'formats': ['json'],
    'jsonOptions': {
        'schema': ExtractSchema.model_json_schema(),
    }
})
print(data["json"])

titles = data["json"]["dataset_titles"]

os.makedirs("data", exist_ok=True)
csv_file_path = os.path.join("data", "titles.csv")

with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title"])
    for title in titles:
         writer.writerow([title])

print(f"titles written to {csv_file_path}")