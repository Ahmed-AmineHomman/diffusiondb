import json
import os
from argparse import ArgumentParser, Namespace

import pandas as pd
from sqlalchemy import create_engine

from wrappers import CivitaiWrapper
from diffusion_models.utils import WRITE_PARAMS


def load_parameters() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--folder",
        required=True,
        type=str,
        help="folder where the model information will be written"
    )
    parser.add_argument(
        "--data",
        required=False,
        type=str,
        help="path to the data file detailing model ids & filenames (overwrites all other params except folder)"
    )
    parser.add_argument(
        "--api-key",
        required=False,
        type=str,
        help="Civitai API key"
    )
    parser.add_argument(
        "--format",
        required=False,
        type=str,
        choices=WRITE_PARAMS.keys(),
        default="xlsx",
        help="format of the outputted file"
    )
    return parser.parse_args()


if __name__ == "__main__":
    params = load_parameters()

    # set-up parameters
    os.makedirs(params.folder, exist_ok=True)
    wrapper = CivitaiWrapper(api_key=params.api_key)
    with open(params.config, "r") as f:
        config = json.load(f)

    models = []
    versions = []
    for _, temp in config.items():
        for _, version_id in temp.items():
            print(f"Model: {version_id}")
            # get base model specs
            model_id = wrapper.get_version_specs(model_id=version_id).get("modelId")
            specs = wrapper.get_model_specs(model_id=model_id)
            models.append({
                **{key: specs.get(key) for key in ["id", "name", "type", "creator"]},
                "creator": specs.get("creator").get("username"),
                **{key: specs.get("stats").get(key) for key in specs.get("stats").keys()},
            })

            # get version specs
            versions += [
                {
                    **{key: e.get(key) for key in ["id", "name", "modelId", "baseModel", "nsfwLevel", "publishedAt", ]},
                    "files": len(e.get("files")),
                    **{key: e.get("stats").get(key) for key in e.get("stats").keys()}
                }
                for e in specs.get("modelVersions")
            ]

    # cast to pandas.DataFrame
    models = (
        pd.DataFrame(models)
        .rename(columns={"id": "modelId"})
        .drop_duplicates(subset="modelId")
        .set_index("modelId")
        .sort_index()
    )
    versions = (
        pd.DataFrame(versions)
        .rename(columns={"id": "versionId"})
        .drop_duplicates(subset="versionId")
        .set_index("versionId")
        .sort_values(by="modelId")
    )

    print(f"dumping data to {params.folder}")
    write_params = WRITE_PARAMS.get(params.format)
    if params.format == "sql":
        engine = create_engine(f"sqlite+pysqlite:///{os.path.join(params.folder, 'models.sqlite3')}", echo=False)
        with engine.connect() as connection:
            models.to_sql(name="models", con=connection, **write_params)
            versions.to_sql(name="versions", con=connection, **write_params)
    elif params.format == "json":
        with open(os.path.join(params.folder, "models_all.json"), "w") as f:
            json.dump(models.to_json(**write_params), f)
        with open(os.path.join(params.folder, "versions.json"), "w") as f:
            json.dump(versions.to_json(**write_params), f)
    elif params.format in ["csv", "xlsx"]:
        if params.format == "csv":
            models.to_csv(os.path.join(params.folder, "models.csv"), **write_params)
            versions.to_csv(os.path.join(params.folder, "versions.csv"), **write_params)
        else:
            with pd.ExcelWriter(path=os.path.join(params.folder, "models.xlsx"), engine="openpyxl", mode="w") as writer:
                models.to_excel(excel_writer=writer, sheet_name="models", **write_params)
                versions.to_excel(excel_writer=writer, sheet_name="versions", **write_params)
    else:
        raise ValueError(f"format {params.format} not supported")

    print("done")
