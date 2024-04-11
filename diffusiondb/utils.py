import json
import os

import requests


def get_model_db() -> dict:
    """Returns the model database as a dictionary."""
    with open(os.path.join(os.path.dirname(__file__), "data", "models.json"), 'r') as fh:
        database = json.load(fh)
    return database


def get_supported_types() -> list:
    """Returns the model types supported by the database"""
    db = get_model_db()
    return list(set([m.get("type") for m in db.values()]))


def get_supported_models() -> list:
    """Returns the model types supported by the database"""
    db = get_model_db()
    return list(db.keys())


def urlget(**kwargs):
    """Simple wrapper around ``requests.get`` raising exception if status code is not equal to 200."""
    response = requests.get(**kwargs)
    if response.status_code != 200:
        raise Exception(f"### ERROR {response.status_code}: {response.json().get('message')}")
    return response


def urldownload(url: str, filepath: str, headers) -> None:
    """Downloads the file located at the provided ``url`` to the provided ``filepath``."""
    if os.path.exists(filepath):
        print(f"file exists at {filepath} -> skipping download")
    else:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)  # create output directory
        try:
            response = urlget(url=url, headers=headers, stream=True)
            with open(filepath, "wb") as fh:
                for chunk in response.iter_content(chunk_size=1024):
                    fh.write(chunk)
        except Exception as error:
            raise Exception(f"### ERROR ### : {error}")
    return
