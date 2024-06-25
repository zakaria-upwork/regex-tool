from fastapi import FastAPI
from utils import create_local_web_page
import re
app = FastAPI()

@app.post("/search_regex")
def search_regex(pattern: str, url: str):
    links = []
    soup = create_local_web_page(url)
    matches = soup.find_all('a', href=re.compile(pattern))
    for match in matches:
        links.append(match.get('href'))
    return {"matches": links}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)