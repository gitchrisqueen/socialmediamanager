import os
from typing import List
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import imageio
from PIL import Image
from moviepy import editor
from moviepy.audio.AudioClip import CompositeAudioClip
from mutagen.mp3 import MP3

audio_path = os.path.join(os.getcwd(), "audios")
video_path = os.path.join(os.getcwd(), "videos")
images_path = os.path.join(os.getcwd(), "images")

HEADERS = ({'User-Agent': \
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36', \
            'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5'})


def create_video_from_images(bg_audio: str, images: List[Image], file_output_path: str, overlay_audio=None):
    audio = MP3(bg_audio)
    audio_length = audio.info.length

    list_of_images = []

    for orig_image in images:
        # Resize to ideal tiktok resolution
        image = orig_image.resize((1080, 1920), Image.LANCZOS)
        list_of_images.append(image)

    # Add text to the images that represent the script

    duration = audio_length / len(list_of_images)
    images_gif = images_path + "/" + 'images.gif'
    imageio.mimsave(images_gif, list_of_images, fps=1 / duration)

    video = editor.VideoFileClip(images_gif)
    bg_audio_clip = editor.AudioFileClip(bg_audio)

    if overlay_audio is None:
        compo_audio = bg_audio_clip
    else:
        # Add text to speach audio over the video
        overlay_audio_clip = editor.AudioFileClip(overlay_audio)
        compo_audio = CompositeAudioClip([
            bg_audio_clip.volumex(0.5),
            overlay_audio_clip.set_start(5).volumex(1.2)  # TODO: use some logic on when to start this audio
        ])

    final_video = video.set_audio(compo_audio)
    os.chdir(video_path)
    final_video.write_videofile(
        fps=60, codec="libx264",
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        filename=file_output_path
    )


def create_video_from_urls(bg_audio: str, image_urls: List, file_output_path: str, overlay_audio=None):
    audio = MP3(bg_audio)
    audio_length = audio.info.length

    list_of_images = []

    for url in image_urls:
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

        # TODO: Determine video size. Currently 400 X 400
        image = Image.open(local_filename).resize((1080, 1920), Image.LANCZOS)
        list_of_images.append(image)

    # Add text to the images that represent the script

    duration = audio_length / len(list_of_images)
    images_gif = images_path + "/" + 'images.gif'
    imageio.mimsave(images_gif, list_of_images, fps=1 / duration)

    video = editor.VideoFileClip(images_gif)
    bg_audio_clip = editor.AudioFileClip(bg_audio)

    if overlay_audio is None:
        compo_audio = bg_audio_clip
    else:
        # Add text to speach audio over the video
        overlay_audio_clip = editor.AudioFileClip(overlay_audio)
        compo_audio = CompositeAudioClip([
            bg_audio_clip.volumex(0.5),
            overlay_audio_clip.set_start(5).volumex(1.2)  # TODO: use some logic on when to start this audio
        ])

    final_video = video.set_audio(compo_audio)
    os.chdir(video_path)
    final_video.write_videofile(
        fps=60, codec="libx264",
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        filename=file_output_path
    )
