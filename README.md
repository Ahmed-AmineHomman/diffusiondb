# diffusiondb

A commandline solution allowing you to set up a diffusion model database compatible with mainstream webuis applications for stable-diffusion (comfyUI, automatic1111's stable-diffusion-webui, etc.).

## Installation

Clone this deposit on the folder of your choice on your system:

```shell
git clone git+https://github.com/Ahmed-AmineHomman/diffusiondb.git
```

Then go to the cloned folder and install the dependencies specified in [requirements.txt](requirements.txt):

```shell
cd diffusiondb
python -m pip install -r requirements.txt
```

**Remark**: it is advised to create a [virtual environment](https://docs.python.org/3/library/venv.html) on which to install the dependencies.

You're ready to download! Just call the [download.py](download.py) script with your python env:

```shell
python download.py [...]
```

Please see the next section for details about the script parameters or just call it with the ``--help`` parameter:

```shell
python download.py --help
```

## Quickstart

You can control the location of the downloaded files with the ``--folder`` parameter:

```shell
python download.py --folder C:/Users/jdupont/database
```

The above command will download & organize all the model files in the `C:/Users/jdupont/database` folder.

### Download control

You can restrict the download to a certain type of models when requiring the download:

```shell
python download.py --type loras vae
```

The above command will ONLY download LORAs and VAEs from the internal model database. If you want even more control, you can provide the labels of the models you wish to download:

```shell
python download.py --models cyberrealistic dreamshaper
```

The above command will ONLY download the [CyberRealistic](https://civitai.com/models/15003/cyberrealistic) and [Dreamshaper](https://civitai.com/models/4384/dreamshaper) models to the output folder. Be careful though, as it is the intersection of ``--models`` and ``--type`` that will be downloaded. Therefore, the following command will download absolutely nothing:

```shell
python download.py --models cyberrealistic dreamshaper --type vaes loras
```

since both CyberRealistic and Dreamshaper are checkpoints rather than LORAs or VAEs. For more information about the supported types & labels, check the help with ``--help```:

```shell
python download.py --help
```

### API keys

Models are taken from [Civitai](https://civitai.com) and [HuggingFace](https://huggingface.co/), and are downloaded from the two previous websites respectively using the [Civitai API](https://github.com/civitai/civitai/wiki/REST-API-Reference) and the [huggingface_hub](https://huggingface.co/docs/huggingface_hub/index) python library.

The Civitai API can require an API token for some models. Indeed, some authors require users to be authenticated in order to allow them to download their models. The identification is therefore done with a Civitai API token that you can generate for free once you are registered. Simply go to your [account settings](https://civitai.com/user/account) and generate an API token. You can then provide it with the ``--civitai-key``.

There is currently no use to providing a HuggingFace token since the hub does not require you to provide any token when downloading public models. However, or consistency purposes, you can provide one with the ``--hfhub-key`` parameter.
