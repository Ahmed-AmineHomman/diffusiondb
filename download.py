import os
from argparse import ArgumentParser, Namespace

from diffusiondb.utils import get_model_db, get_supported_types, get_supported_models
from diffusiondb.wrappers import CivitaiWrapper, HFHubWrapper


def load_parameters() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--folder",
        required=False,
        type=str,
        help="folder where the downloaded models will be written (set to current folder if not provided)"
    )
    parser.add_argument(
        "--models",
        required=False,
        type=str,
        nargs="+",
        choices=get_supported_models(),
        help="if provided, only models whose label is provided will be downloaded"
    )
    parser.add_argument(
        "--types",
        required=False,
        type=str,
        nargs="+",
        choices=get_supported_types(),
        help="if set, only models whose type is provided will be downloaded"
    )
    parser.add_argument(
        "--civitai-key",
        required=False,
        type=str,
        help="Civitai API key (allows to download models whose author required identification)"
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
    output_folder = params.folder if params.folder else os.path.join(os.getcwd(), "database")
    os.makedirs(output_folder, exist_ok=True)

    # configure model list
    models = get_model_db()
    if params.models:
        models = {k: v for k, v in models.items() if k in params.models}
    if params.types:
        models = {k: v for k, v in models.items() if v.get("type") in params.types}

    # download every model
    for filename, specs in models.items():
        print(f". downloading {filename}")
        try:
            wrappers.get(specs.get("api")).download(
                model_id=specs.get("id"),
                folder=os.path.join(output_folder, specs.get("type").lower()),
                filename=filename
            )
        except Exception as e:
            print(f"### ERROR: {e}\n -> skipping {filename}")

    print("done")
