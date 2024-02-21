from langchain import hub
from langchain.chains import LLMChain
from langchain.llms.base import LLM
from langchain_community.chat_models import ChatOpenAI

from cqc_smm.utilities.AI.llm.prompts import *


def generate_quote(llm: LLM, topic: str) -> str:
    """
    Generates a quote based on the given topic using the LLM model.
    """

    # pull a chat prompt
    prompt = hub.pull("cqc/inspirational_quote")

    chain = LLMChain(
        llm=llm,
        prompt=prompt  # QUOTE_PROMPT
    )

    return chain.run({
        "topic": topic,
    }).strip()


def generate_photo_query(llm: LLM, topic: str) -> str:
    """
    Generates a query using the LLM model.
    """
    chain = LLMChain(
        llm=llm,
        prompt=PHOTO_QUERY_PROMPT
    )
    return chain.run({
        "quote": topic
    }).strip()


def generate_story(llm: LLM, quote: str) -> str:
    prompt = hub.pull("cqc/speech_quote_type")

    """
    Generates a story based on the quote using the LLM model.
    """
    chain = LLMChain(
        llm=llm,
        prompt=prompt  # STORY_PROMPT
    )
    return chain.run({
        "quote": quote
    }).strip()


if __name__ == "__main__":
    model = 'gpt-3.5-turbo-16k-0613'
    llm = ChatOpenAI(temperature=1, model=model)
    quote = generate_quote(
        llm=llm,
        topic="how hair growth faster,how hair growth fast,what make hair grow faster,what vitamins for hair growth,what make hair grow")

    print(quote)
