import os
from typing import Optional

from huggingface_hub import hf_hub_url

from .utils import urlget, urldownload


class BaseModelWrapper:
    api_token: str
    _env_key: str

    def __init__(self, api_key: Optional[str] = None):
        # get diffusiondb key
        self.api_token = api_key if api_key else os.environ.get("API_TOKEN")

    def download(
            self,
            model_id: str,
            folder: str,
            filename: str
    ) -> None:
        """
        Downloads the file corresponding to ``model_id`` to the path specified by ``folder`` and ``filepath``.

        **Important**: ``filename`` should be a file name without the file extension.
        """
        raise NotImplementedError()


class CivitaiWrapper(BaseModelWrapper):
    """
    Civitai API wrapper.
    """
    _env_key = "CIVITAI_API_KEY"
    _base_url = "https://civitai.com/api/v1"

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

        # build header
        self.headers = {"Content-Type": "application/json"}
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"

    def get_model_specs(self, model_id: str) -> dict:
        """Retrieve model specs from model id."""
        return (
            urlget(
                url=f"{self._base_url}/models/{model_id}",
                headers=self.headers
            )
            .json()
        )

    def get_version_specs(self, model_id: str) -> dict:
        """Retrieve model specs from model id."""
        return (
            urlget(
                url=f"{self._base_url}/model-versions/{model_id}",
                headers=self.headers
            )
            .json()
        )

    def download(
            self,
            model_id: str,
            folder: str,
            filename: str
    ) -> None:
        """See base class doc."""
        specs = self.get_version_specs(model_id=model_id)

        # build download url
        url = specs.get("downloadUrl")

        # build local file path
        remote_name = specs.get("files")[0].get("name")
        extension = remote_name.split(".")[-1]
        local_path = os.path.join(folder, f"{filename}.{extension}")

        # download file
        urldownload(url=url, filepath=local_path, headers=self.headers)


class HFHubWrapper(BaseModelWrapper):
    _env_key = "HF_API_KEY"

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.headers = {}
        if self.api_token:
            self.headers["Authorization"] = f"Bearer {self.api_token}"

    def download(
            self,
            model_id: str,
            folder: str,
            filename: str
    ) -> None:
        """See base class doc."""
        # build hf hub identifiers
        temp, remote_name = os.path.split(model_id)
        repo_id = "/".join(temp.split("/")[:2])
        subfolder = "/".join(temp.split("/")[2:])

        # build download url
        url = hf_hub_url(
            repo_id=repo_id,
            subfolder=subfolder,
            filename=remote_name,
            repo_type="model"
        )

        # build local filepath
        extension = remote_name.split(".")[-1]
        local_path = os.path.join(folder, f"{filename}.{extension}")

        # download file
        urldownload(url=url, filepath=local_path, headers=self.headers)
