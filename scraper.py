import requests
from bs4 import BeautifulSoup

def get_job_description(url):
    """Fetches and extracts job description text from a given URL."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    job_desc = ""

    # Try a set of common selectors found on job pages
    selectors = [
        'div.job-description',
        'div.description',
        'div#jobDescriptionText',
        'section.job-details',
        'div.job-detail',
        'article'
    ]
    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            job_desc = element.get_text(separator=" ", strip=True)
            # Heuristic: consider this valid if it has a reasonable word count.
            if len(job_desc.split()) > 50:
                return job_desc

    # Fallback: extract text from all <p> and <div> tags.
    paragraphs = soup.find_all(['p', 'div'])
    job_desc = " ".join([p.get_text(separator=" ", strip=True) for p in paragraphs])
    return job_desc
