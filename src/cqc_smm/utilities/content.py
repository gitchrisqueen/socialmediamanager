from pprint import pprint

from langchain_core.pydantic_v1 import BaseModel

from cqc_smm.utilities.company import CompanyProfile, SMART_Goal, get_audience


# from pydantic import BaseModel


class ContentStrategy(BaseModel):
    # business_goals: list[str, int] = None
    # audience_profile: AudienceProfile = None
    # content_management = None  # TODO: ? Location of files (assets) spreadsheet calendar
    # brand_voice: str = None  # See: https://www.semrush.com/blog/how-to-define-your-tone-of-voice/
    # topics: list[str] = None  # TODO: Get from AI LLM ???

    pass




    # TODO: Get KPIS based on goals

    # Return new goals based on current KPIS and business goals


class ContentIdea:

    def generate_ideas(self, num=1):
        ideas = []
        for i in range(0, num):
            ideas.append(self.generate_idea())
        return ideas

    def generate_idea(self, num=1):
        # TODO: Use LLM to go through steps to generate ideas
        """
        1. Look at competitors using organic research tool
        2. Scrub relevant Reddit subreddits and filter by top discussions for ideas

        :param num:
        :return:
        """
        return []

    def curate_articles(self, num=1):
        # TODO: Use Feedly API to get articles then use LLM to give summary and insight in the business brand voice. Return currated list with references
        # https://feedly.com/market-intelligence
        return ""

    def curate_product_promotion(self):
        # TODO: Use API to access product hunt and LLM to summarize top reviews about new products in the same topic space
        # https://api.producthunt.com/v2/docs
        return ""


if __name__ == '__main__':
    cs = ContentStrategy()


