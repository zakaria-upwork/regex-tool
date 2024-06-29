from fastapi import FastAPI, HTTPException
from utils import create_web_page_soup
import re
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    filename='logs/logs.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = FastAPI()


@app.post("/search_regex")
def search_regex(pattern: str, url: str):
    logging.info(f"Received search request with pattern: {pattern} and URL: {url}")
    
    try:
        soup = create_web_page_soup(url)
    except Exception as e:
        logging.error(f"Error creating soup object: {e}")
        raise HTTPException(status_code=500, detail="Error processing the URL")

    try:
        regex = re.compile(pattern)
    except re.error as e:
        logging.error(f"Invalid regex pattern: {e}")
        raise HTTPException(status_code=400, detail="Invalid regex pattern")
    
    links = []
    matches = soup.find_all('a', href=regex)
    for match in matches:
        links.append(match.get('href'))
    
    logging.info(f"Found {len(links)} matches for pattern: {pattern}")
    
    return {"matches": links}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
