import gradio as gr
import requests
from PIL import Image
import qrcode
import io
import base64


# URL of stable diffusion API endpoint
URL = 'http://127.0.0.1:7861'
NEGATIVE_PROMT = 'ugly, disfigured, low quality, blurry, nsfw'
SD_MODEL = 'AnythingV5Ink_v5PrtRE.safetensors [7f96a1a9ca]'
SAMPLER = 'DPM++ 2M Karras'
BATCH_SIZE = 1
STEPS = 22
CFG_SCALE = 7

CONTROLNET_MODULE = 'none'
CONTROLNET_MODEL = 'controlnetQRPatternQR_v2Sd15 [2d8d5750]'
CONTROLNET_WEIGHT = 1.3
CONTROLNET_PIXEL_PERFECT = True
CONTROLNET_CONTROL_MODE = 'Balanced'

NUMBER_OF_IMAGES = 4


def request_image(qr_code, promt):
    payload = {
        'prompt': promt,
        'negative_prompt': NEGATIVE_PROMT,
        'sd_model_name': SD_MODEL,
        'sampler_name': SAMPLER,
        'batch_size': BATCH_SIZE,
        'steps': STEPS,
        'cfg_scale': CFG_SCALE,
        'alwayson_scripts': {
            'controlnet': {
                'args': [
                    {
                        'input_image': qr_code,
                        'module': CONTROLNET_MODULE,
                        'model': CONTROLNET_MODEL,
                        'weight': CONTROLNET_WEIGHT,
                        'pixel_perfect': CONTROLNET_PIXEL_PERFECT,
                        'control_mode': CONTROLNET_CONTROL_MODE,
                    }
                ]
            }
        }
    }
    response = requests.post(url=f'{URL}/sdapi/v1/txt2img', json=payload)
    result = response.json()['images'][0]
    return Image.open(io.BytesIO(base64.b64decode(result.split(',', 1)[0])))


def generate_qr_code(url, logo):
    basewidth = 100
    
    # adjust image size
    if logo:
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(url)
    QRcode.make()
    QRcolor = 'Black'
    
    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor,
        back_color='white',
    ).convert('RGB')

    if logo:
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
            (QRimg.size[1] - logo.size[1]) // 2)
        QRimg.paste(logo, pos)

    buffered = io.BytesIO()
    QRimg.save(buffered, format='PNG')

    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def get_images(url, text, logo):
    qr_code = generate_qr_code(url, logo)
    return [request_image(qr_code, text) for _ in range(NUMBER_OF_IMAGES)]


with gr.Blocks() as web:
    gr.Markdown('Image Generator')
    with gr.Row():
        inp = [
            gr.Textbox(placeholder='Some Link', label='Tracker link'),
            gr.Textbox(placeholder='Artistic, Pakistani Art, Mountains', label='How should the logo look?'),
            gr.Pil(),
        ]
    btn = gr.Button('Submit')
    with gr.Row():
        out = [gr.Pil() for _ in range(NUMBER_OF_IMAGES)]

    btn.click(fn=get_images, inputs=inp, outputs=out)

web.launch()
