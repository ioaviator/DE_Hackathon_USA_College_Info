import logging
import os

from dotenv import load_dotenv

# from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

# Variables from .env file
url=os.getenv('URL')
api_key=os.getenv('API_KEY')

#create data_store folder for api response
# parent_dir = Path(__file__).resolve().parent
# data_dir = parent_dir / "data_store"
# data_dir.mkdir(exist_ok=True)


# API request parameters
params:dict = {
    "api_key": api_key,
    "_sort": "latest.admissions.admission_rate.overall:asc",
    "_per_page": 100,
    "fields": ("id,school.name,"
      "latest.school.state,"
        "latest.academics.sat_scores.average.overall,"
          "latest.school.degrees_awarded.predominant,"
            "latest.school.degrees_awarded.highest,"
              "latest.admissions.admission_rate.overall,"
                "latest.student.size,"
                "latest.cost.tuition.in_state,"
                "latest.cost.tuition.out_of_state,"
                "latest.aid.loan_principal,"
                "latest.school.ownership,latest.school.online_only"
    )
}