import json
import os
from argparse import ArgumentParser, Namespace

from api.wrappers import CivitaiWrapper, HFHubWrapper


def load_parameters() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        required=True,
        type=str,
        help="Path to the config file"
    )
    parser.add_argument(
        "--database",
        required=False,
        type=str,
        help="folder where the downloaded models will be written (set to current folder if not provided)"
    )
    parser.add_argument(
        "--civitai-key",
        required=False,
        type=str,
        help="Civitai API key"
    )
    parser.add_argument(
        "--hfhub-key",
        required=False,
        type=str,
        help="HuggingFace Hub API key"
    )
    return parser.parse_args()


if __name__ == "__main__":
    params = load_parameters()
    wrappers = dict(
        civitai=CivitaiWrapper(api_key=params.civitai_key),
        hfhub=HFHubWrapper(api_key=params.hfhub_key)
    )

    # configure output
    output_folder = params.database if params.database else os.path.join(os.getcwd(), "database")
    os.makedirs(output_folder, exist_ok=True)

    # get db config
    with open(params.config, "r") as fh:
        config = json.load(fh)

    # download every model
    for filename, specs in config.items():
        print(f". downloading {filename}")
        wrappers.get(specs.get("api")).download(
            model_id=specs.get("id"),
            folder=os.path.join(output_folder, specs.get("type").lower()),
            filename=filename
        )

    print("done")
