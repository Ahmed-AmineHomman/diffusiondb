import requests
import os


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


WRITE_PARAMS = {
    "json": dict(orient="records"),
    "csv": dict(sep=";", header=True, index=True, decimal=".", encoding="utf8"),
    "xlsx": dict(header=True, index=True),
    "sql": dict(index=True, if_exists="replace")
}
READ_PARAMS = {
    "json": dict(orient="records"),
    "csv": dict(sep=";", header=0, index_col=0, decimal=".", encoding="utf8"),
    "xlsx": dict(header=0, index_col=0),
    "sql": dict(index_col=0)
}
