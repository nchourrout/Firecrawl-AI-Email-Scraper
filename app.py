from typing import List
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from urllib.parse import urlparse
from unidecode import unidecode
import pandas as pd
import os

crawler = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

class MemberSchema(BaseModel):
    firstname: str
    lastname: str
    position: str
    email: str
    location: str
    imageUrl: str = Field(..., description="Absolute URL of the member's profile image")
    isKeyPerson: bool

class TeamPageSchema(BaseModel):
    list: List[MemberSchema] = Field(..., description="Team members")

def llm_scrape(url):
    print("Scraping URL:", url)
    try:
        data = crawler.scrape_url(url, {
            'extractorOptions': {
                'extractionSchema': TeamPageSchema,
                'mode': 'llm-extraction'
            }
        })
        return data.get('llm_extraction')
    except Exception as e:
        print(f"Exception occurred while scraping {url}: {e}")
        return None
    
def guess_email(firstname, lastname, pageURL):
    domain = urlparse(pageURL).netloc
    name = unidecode(f'{firstname}.{lastname}').lower()
    return f'{name}@{domain}'
    
if __name__ == "__main__":
    query = '"meet the team" real estate agency london'
    people_data = []
    results = crawler.search(query)
    for result in results:
        url = result['metadata']['sourceURL']
        page_data = llm_scrape(url)
        if page_data and 'list' in page_data:
            for member in page_data['list']:
                if member.get('isKeyPerson'):
                    if not member.get('email'):
                        member['email'] = guess_email(member['firstname'], member['lastname'], url)
                    people_data.append(member)

    df = pd.DataFrame(people_data)
    df.to_csv("output.csv", index=False)
