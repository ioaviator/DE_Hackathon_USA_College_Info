import requests

from .config import params, url


def api_connect():
  responses = []
  for page in range(1, 6):  # 10 pages for 1000 results
      params["page"] = page
      
      try:
        response = requests.get(url, params=params, timeout=10)
        # Raise an error for HTTP error codes (like 4xx or 5xx)
        response.raise_for_status()
        data = response.json()
        responses.append(data)
        
        print(f"top_usa_schools_{page}.json successfully loaded")

      except requests.exceptions.RequestException as e:
        print(f"Error on page {page}: {e}")
        break

  return responses
