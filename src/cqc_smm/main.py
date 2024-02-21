import os
from datetime import datetime

import requests
from elevenlabs import RateLimitError

import utilities.audio.elevenlabs_helper as EL
import utilities.audio.get_rnd_frm as FRM
import utilities.pexels_helper as PH
import utilities.video.video_creator as VC
from cqc_smm.utilities.AI import QuoteGenerator
from cqc_smm.utilities.AI.csv_agent import get_top_n_question
from cqc_smm.utilities.tiktok_helper import get_tiktok_trending_tags

audio_path = os.path.join(os.getcwd(), "audios")
video_path = os.path.join(os.getcwd(), "videos")
images_path = os.path.join(os.getcwd(), "images")


# Login to Tiktok

# Auto-reply to comments
# - Like comments
# - respond to comments


# Create motivation video
def create_video():
    # Get Image
    print("Getting Images")
    list_of_photos = PH.get_photos("Luxury real estate", 4)
    list_of_urls = list(map(lambda x: x.original, list_of_photos))
    print("Received Images: %s" % str(list_of_urls))

    # Get Audio
    print("Getting Audio")
    audio_json = FRM.get_rndm_rfmp3(60)
    random_mp3_url = audio_json.get("source_url")
    response = requests.get(random_mp3_url)
    bg_audio = audio_path + "/test_2.mp3"
    open(bg_audio, "w+b").write(response.content)
    print("Received Audio: %s | Saved to: %s" % (random_mp3_url, bg_audio))

    # Get Text from ChatGPT
    motivation_text = "Get up early... That way, the worms dont eat you!"
    print("Motivation Text is: %s" % str(motivation_text))

    # Text to speach audio
    print("Converting Text to Speech Audio (ElevenLabs)")
    audio_bytes = EL.get_text_to_speech(motivation_text)
    overlay_file = audio_path + '/overlay_audio.mp3'
    with open(overlay_file, mode='w+b') as f:
        f.write(audio_bytes)
    print("Audio Converted: %s" % overlay_file)

    # Merge together
    output_file = video_path + "/tikitok_sample.mp4"
    VC.create_video_from_urls(bg_audio, list_of_urls, output_file, overlay_file)

    print("Video Created: %s" % output_file)


def post_tiktok_video():
    # Post to TikTOK

    # Trending topics for content guide

    # Stitch / Duo other content ???
    return False


def test():
    bg_audio = audio_path + "/test.mp3"
    overlay_file = audio_path + '/overlay_audio.mp3'

    # Get Image
    print("Getting Images")
    list_of_photos = PH.get_photos("Luxury real estate", 4)
    list_of_urls = list(map(lambda x: x.original, list_of_photos))
    print("Received Images: %s" % str(list_of_urls))

    # Merge together
    output_file = video_path + "/tikitok_sample.mp4"
    VC.create_video_from_urls(bg_audio, list_of_urls, output_file, overlay_file)

    print("Video Created: %s" % output_file)


class App:
    def __init__(self):
        self.size = (1080, 1350)

        # TODO: Create chain to develop content strategy
        # TODO: Create chain to define, review, and utilize metrics and goals to new content

        # Content Ideas
        # TODO: Create chain to generate content ideas
        # TODO: Get Hashtag from Tiktok trending topics
        tiktok_trending_hashtags = get_tiktok_trending_tags()
        print("Tiktok trending hashtags:\n%s" % "\n".join(tiktok_trending_hashtags))


        # TODO: Find ClickBank product to promote
        # TODO: Get content topics from Answer The Public
        csv_file_path = '//downloads/hair growth-en-us-suggestions-30-01-2024.csv'  # TODO: Write code to download csv file or use directory of files
        topics = get_top_n_question(csv_file_path, 5)
        self.topic = ", ".join(topics)

    def run(self):


        # TODO: Should create enough for the week

        # TODO: Create loop for how many to create. Should store links and files in spreadsheet


        time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # Get Audio
        print("Getting Audio")
        audio_json = FRM.get_rndm_rfmp3(60)
        random_mp3_url = audio_json.get("source_url")
        response = requests.get(random_mp3_url)
        bg_audio = audio_path + "/test_" + time_stamp + ".mp3"
        open(bg_audio, "w+b").write(response.content)
        print("Received Audio: %s | Saved to: %s" % (random_mp3_url, bg_audio))

        # Generate Quote
        print("Generating Quote for Topic(s): %s" % self.topic)
        quote = QuoteGenerator(self.topic, self.size)
        image = quote.make()

        try:
            # Text to speach audio
            print("Converting Text to Speech Audio (ElevenLabs)")
            audio_bytes = EL.get_text_to_speech(quote.story)
            overlay_file = audio_path + '/overlay_audio_' + time_stamp + '.mp3'
            with open(overlay_file, mode='w+b') as f:
                f.write(audio_bytes)
            print("Audio Converted: %s" % overlay_file)
        except RateLimitError as e:
            overlay_file = None
            print("RateLimitError while creating overlay_audio | %s" % e)

        # Merge together
        output_file = video_path + "/tikitok_sample_" + time_stamp + ".mp4"
        VC.create_video_from_images(bg_audio, [image], output_file, overlay_file)

        # TODO: Post to tiktok finished videos from Google spreadsheet according to optimal schedule (from spreadsheed???)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create_video()

    app = App()
    app.run()

    # test()
