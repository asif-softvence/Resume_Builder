import requests
from core.config import JSEARCH_API_KEY, JSEARCH_API_HOST


def fetch_job(query, location, page=1):
    url="https://jsearch.p.rapidapi.com/search"

    headers= {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": JSEARCH_API_HOST
    }

    params={
        "query": f"{query} in {location}",
        "page": page,
        "num_page":1
    }

    response= requests.get(url, headers= headers, params= params)

    if response.status_code== 200:
        return response.json()
    return {"erro": response.text}