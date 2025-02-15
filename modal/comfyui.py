import modal

import json
import subprocess
import uuid
from pathlib import Path
from typing import Dict

import modal

image = (  # build up a Modal Image to run ComfyUI, step by step
    modal.Image.debian_slim(  # start from basic Linux with Python
        python_version="3.11"
    )
    .apt_install("git")  # install git to clone ComfyUI
    .pip_install("fastapi[standard]==0.115.4")  # install web dependencies
    .pip_install("comfy-cli==1.3.5")  # install comfy-cli
    .run_commands(  # use comfy-cli to install ComfyUI and its dependencies
        "comfy --skip-prompt install --nvidia --version 0.3.10"
    )
)

# ## Downloading custom nodes
# We'll also use `comfy-cli` to download custom nodes, in this case the popular [WAS Node Suite](https://github.com/WASasquatch/was-node-suite-comfyui).
#
# Use the [ComfyUI Registry](https://registry.comfy.org/) to find the specific custom node name to use with this command.

# See [this post](/blog/comfyui-custom-nodes) for more examples on how to install popular custom nodes like [ComfyUI Impact Pack](/blog/comfyui-custom-nodes#2-comfyui-impact-pack) and [ComfyUI IPAdapter Plus](/blog/comfyui-custom-nodes#3-comfyui-ipadapater-plus).
# ## Downloading models

# `comfy-cli` also supports downloading models, but we've found it's faster to use [hf_hub_download](https://huggingface.co/docs/huggingface_hub/en/guides/download#download-a-single-file) directly by:
# 1. Enabling [faster downloads](https://huggingface.co/docs/huggingface_hub/en/guides/download#faster-downloads)
# 2. Mounting the cache directory to a [Volume](/docs/guide/volumes)
#
# By persisting the cache to a Volume, we avoid re-downloading the models every time you rebuild your image.

def hf_download():
    from huggingface_hub import hf_hub_download, login

    downloads = [
        {
            "repo_id":"Comfy-Org/flux1-dev",
            "filename":"flux1-dev-fp8.safetensors",
            "path": "/root/comfy/ComfyUI/models/checkpoints/"
        },
        # {
        #     "repo_id": "comfyanonymous/flux_text_encoders",
        #     "filename": "clip_l.safetensors",
        #     "path": "/root/comfy/ComfyUI/models/clip/"
        # },
        # {
        #     "repo_id": "comfyanonymous/flux_text_encoders",
        #     "filename": "t5xxl_fp8_e4m3fn_scaled.safetensors",
        #     "path": "/root/comfy/ComfyUI/models/clip/"
        # },
        # {
        #     "repo_id": "black-forest-labs/FLUX.1-dev",
        #     "filename": "ae.safetensors",
        #     "path": "/root/comfy/ComfyUI/models/vae/"
        # }
    ]

    for download in downloads:

        flux_model = hf_hub_download(
            repo_id=download["repo_id"],
            filename=download["filename"],
            cache_dir="/cache",
        )

        # symlink the model to the right ComfyUI directory
        subprocess.run(
            f"ln -s {flux_model} {download['path']}{download['filename']}",
            shell=True,
            check=True,
        )


vol = modal.Volume.from_name("hf-hub-cache", create_if_missing=True)

image = (
    # install huggingface_hub with hf_transfer support to speed up downloads
    image.pip_install("huggingface_hub[hf_transfer]==0.26.2")
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .run_function(
        hf_download,
        # persist the HF cache to a Modal Volume so future runs don't re-download models
        volumes={"/cache": vol},
    )
)


# Lastly, we copy the ComfyUI workflow JSON to the container.
image = image.add_local_file(
    Path(__file__).parent / "workflow_api.json", "/root/workflow_api.json"
)

vol = modal.Volume.from_name("hf-hub-cache", create_if_missing=True)
app = modal.App(name="comfy-flux1-dev", image=image)


@app.function(
    allow_concurrent_inputs=10,  # required for UI startup process which runs several API calls concurrently
    concurrency_limit=1,  # limit interactive session to 1 container
    gpu="L4",  # or L40S for good starter GPU for inference
    volumes={"/cache": vol},  # mounts our cached models
)
@modal.web_server(8000, startup_timeout=60)
def ui():
    subprocess.Popen("comfy launch -- --listen 0.0.0.0 --port 8000", shell=True)

