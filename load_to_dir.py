import json
from pathlib import Path

from config import data_dir


def load_files_to_dir(data, page_id):
    with open(f"./data_store/top_usa_schools_{page_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"top_usa_schools_{page_id}.json successfully loaded to {data_dir}")

    return None
