# ArtisitcQrCodes
An Artist's approach to QR codes

## Stable Diffusion WebUI
For this repository to work we need to run https://github.com/AUTOMATIC1111/stable-diffusion-webui locally and install https://github.com/Mikubill/sd-webui-controlnet extension.

Then we need to add models to it, for this project we used:
checkpoint: https://huggingface.co/wsj1995/stable-diffusion-models/blob/main/AnythingV5Ink_v5PrtRE.safetensors
controlnet model: https://civitai.com/models/90940/controlnet-qr-pattern-qr-codes

Run Stable diffusion in API only mode: "python webui.py --no-half --nowebui"

## Creating QR Codes
1. Create a Virtual Environment with Python 3.10.12
2. Install requirements
3. python webui.py
