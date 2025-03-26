from typing import Any, Dict, List

import requests

from .config import logger, params, url


def api_connect()->List[Dict[str, Any]]:
  """
    Returns a list of JSON responses from the API.

    Returns:
      responses (List[Dict[str, Any]]): List of JSON responses from the API.
    """

  responses:List = []
  for page in range(1, 11):  # 10 pages for 1000 results
      params["page"] = page
      
      try:
        response:requests.Response = requests.get(url, params=params, timeout=10)
        # Raise an error for HTTP error codes (like 4xx or 5xx)
        response.raise_for_status()
        data:Dict[str, Any] = response.json()
        responses.append(data)
        
        logger.info(f"top_usa_schools_{page}.json successfully loaded")

      except requests.exceptions.RequestException as e:
        logger.error(f"Error on page {page}: {e}")
        break

  return responses
