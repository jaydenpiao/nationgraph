import os
from dotenv import load_dotenv
from firecrawl import FirecrawlApp  

load_dotenv()

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

# first page
page_url = "https://dataverse.harvard.edu/dataverse/harvard?page=1"
result = app.scrape_url(page_url, params={'formats': ['html']})
html_content = result.get('html', '')  

# print the first 500 characters of the HTML content
print(html_content[:500])