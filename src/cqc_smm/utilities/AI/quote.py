import gc

from PIL import ImageFont
from langchain_community.chat_models import ChatOpenAI
from rich import print

from cqc_smm.utilities.image.footer import Footer
from cqc_smm.utilities.image.image import ImageGenerator
from cqc_smm.utilities.AI.llm import load_llm, generate_quote, generate_photo_query, generate_story
import cqc_smm.utilities.pexels_helper as PH




class QuoteGenerator:
    def __init__(self, topic, size):
        self.width, self.height = size
        self.font = ImageFont.truetype("fonts/BebasNeue.otf", 115)
        model = 'gpt-3.5-turbo-16k-0613'
        self.llm = ChatOpenAI(temperature=.7, model=model) # load_llm()
        self.quote = generate_quote(self.llm, topic)
        self.photo_query = generate_photo_query(self.llm, self.quote)
        self.story = generate_story(self.llm, self.quote)
        self.unload()

        print({
            "quote": self.quote,
            "photo_query": self.photo_query,
            "story": self.story
        })

        # Replace image with a random one from pexel_helpers.py
        photo = PH.get_photo(self.photo_query)
        photo_url = photo.original

        self.image = ImageGenerator(self.quote, size, photo_url)
        self.footer = Footer(self.height)

    def unload(self):
        del self.llm
        gc.collect()

    def make(self):
        image = self.image.prepare()
        self.image.add_quote(image, self.quote, self.font)
        self.footer.add(image)
        #image.show() # USe to show the image
        return image