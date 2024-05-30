# Firecrawl AI Email Scraper
Using [firecrawl.dev](https://firecrawl.dev), this script can search the web and scrape public pages to extract email addresses.


## Blog Post
For more insights on Firecrawl and on how this scraper was developed, read this [detailed blog post](https://medium.com/@nchourrout/build-an-ai-scraper-in-50-lines-of-code-with-firecrawl-a811d4cdf7d1).

## Installation

Install required libraries
```
pip install firecrawl-py pydantic pandas unidecode
```

Set up your Firecrawl API Key (first 300 credits are free)
```
export FIRECRAWL_API_KEY='your_api_key_here'
```
Add this line to your `.bash_profile` or `.zshrc` to make the setting persist across sessions.

## Usage
Update the `query` var to target the desired industry/location and run the script 
```
python app.py
```