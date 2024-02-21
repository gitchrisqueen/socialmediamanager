import gc
import os
import textwrap
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import torch
from PIL import Image, ImageDraw, ImageChops, ImageEnhance
from PIL.ImageFont import FreeTypeFont
from diffusers import StableDiffusionPipeline

HEADERS = ({'User-Agent': \
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36', \
            'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5'})

images_path = os.path.join(os.getcwd(), "images")

class ImageGenerator:
    def __init__(self, prompt: str, size: tuple, url: str):
        self.prompt = prompt.strip()
        self.size = size
        self.width, self.height = size
        self.url = url

    def prepare_stablediff(self):
        """
        Prepares the background image
        """

        bg_image = self.generate_image()
        image = Image.open(bg_image)
        image = self.resize_and_crop(image, self.width, self.height)
        image = self.apply_tint(image, (200, 200, 200))
        ImageDraw.Draw(image)
        return image

    def prepare(self):
        """
        Prepares the background image
        """

        bg_image = self.get_image_from_url(self.url)
        image = Image.open(bg_image)
        image = self.resize_and_crop(image, self.width, self.height)
        image = self.apply_tint(image, (200, 200, 200))
        ImageDraw.Draw(image)
        return image

    def get_image_from_url(self, url) -> str:
        print("Retrieving image: %s" % url)
        req = Request(
            url=url,
            headers=HEADERS
        )
        content = urlopen(req).read()
        # Get file name and file type from url
        a = urlparse(url)
        local_filename = images_path + "/" + os.path.basename(a.path)
        with open(local_filename, mode='w+b') as f:
            f.write(content)

        print("URL: %s |  Retrieved to: %s" % (url, local_filename))
        return local_filename

    @staticmethod
    def resize_and_crop(image, target_width, target_height):
        """
        Resize and crop the image to fit the specified size.
        """
        original_width, original_height = image.size
        ratio = max(target_width / original_width, target_height / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        image = image.resize(new_size, Image.LANCZOS)
        crop_x0 = (new_size[0] - target_width) // 2 if new_size[0] > target_width else 0
        crop_y0 = (new_size[1] - target_height) // 2 if new_size[1] > target_height else 0
        crop_x1 = crop_x0 + target_width if new_size[0] > target_width else new_size[0]
        crop_y1 = crop_y0 + target_height if new_size[1] > target_height else new_size[1]
        return image.crop((crop_x0, crop_y0, crop_x1, crop_y1))

    def generate_image(self) -> str:
        """
        Runs inference to generate an image
        """
        args = {
            "prompt": self.prompt,
            "width": 512,
            "height": 512,
            "negative_prompt": ["text", "bad anatomy", "bad hands", "unrealistic", "bad pose", "bad lighting"],
            "num_inference_steps": 100,
            "guidance_scale": 1,
        }

        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16,
            use_safetensors=True,
        )

        if torch.cuda.is_available():
            print("Using CUDA")
            pipe = pipe.to("cuda")
            pipe.enable_vae_slicing()
            pipe.enable_xformers_memory_efficient_attention()
        else:
            print("Using CPU")
            pipe.enable_sequential_cpu_offload()

        image = pipe(**args).images[0]

        del pipe
        torch.cuda.empty_cache()
        gc.collect()

        # Return the path to the saved image
        return self.save_image(image)

    @staticmethod
    def save_image(image):
        image_path = os.path.join(os.getcwd(), "images")+"/" + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"
        image.save(image_path)
        return image_path

    @staticmethod
    def apply_tint(image, tint_color):
        """
        Applies a tint to the image
        """
        ImageChops.multiply(image, Image.new('RGB', image.size, tint_color))
        return ImageEnhance.Brightness(image).enhance(.6)

    @staticmethod
    def add_quote(image, quote: str, font: FreeTypeFont, wrap_width=24, line_padding=-10):
        """
        Puts the quote in the centre of the image.
        """
        draw = ImageDraw.Draw(image)
        width, height = image.size

        left, top, font_width, font_height = font.getbbox(quote)

        lines = textwrap.wrap(quote, width=wrap_width)
        text_height_total = (font_height + line_padding) * (len(lines) - 1)
        y = (height - text_height_total) / 2

        for line in lines:
            line_width = draw.textlength(line, font=font)
            x = (width - line_width) / 2
            draw.text((x, y), line, font=font)
            y += font_height + line_padding