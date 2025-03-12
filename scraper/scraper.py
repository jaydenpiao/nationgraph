from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import Any, Optional, List
import os
import csv
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from utils import extract_dataset_titles

load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

scrape_result = app.scrape_url('https://dataverse.harvard.edu/dataverse/harvard?q=&types=datasets&page=1&sort=dateSort&order=desc', params={'formats': ['markdown', 'html']})
print(scrape_result)