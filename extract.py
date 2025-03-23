import requests

from config import params, url
from load_to_dir import load_files_to_dir


def api_connect():
  for page in range(1, 3):  # 10 pages for 1000 results
      params["page"] = page
      
      try:
        response = requests.get(url, params=params, timeout=10)
        # Raise an error for HTTP error codes (like 4xx or 5xx)
        response.raise_for_status()
        data = response.json()
        load_to_dir = load_files_to_dir(data, page)

      except requests.exceptions.RequestException as e:
        print(f"Error on page {page}: {e}")
        break
  return None
