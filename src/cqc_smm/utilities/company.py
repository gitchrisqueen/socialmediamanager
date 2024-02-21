from pprint import pprint
from typing import List, Optional, Annotated

from langchain import hub
from langchain.agents.structured_chat.output_parser import StructuredChatOutputParserWithRetries
from langchain.output_parsers import PydanticOutputParser, RetryWithErrorOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import (BaseModel, Field, StrictStr, StrictInt, StrictFloat, StrictBool)
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI

from cqc_smm.utilities.audience import List_Of_AudienceProfiles

# from pydantic import (BaseModel, Field, StrictStr, StrictInt, StrictFloat, PositiveInt, StrictBool)

# JSON Models
# gpt-4-1106-preview or gpt-3.5-turbo-1106

# model = 'gpt-3.5-turbo-16k-0613'
model = 'gpt-3.5-turbo-1106'
# model = 'gpt-4-1106-preview'
retry_model = 'gpt-4-1106-preview'
llm = ChatOpenAI(temperature=.5, model=model)
retry_llm = ChatOpenAI(temperature=0, model=retry_model)


class SMART_Goal(BaseModel):
    detail: Annotated[
        StrictBool | StrictStr,
        Field(
            description="The detail of the goal with all its SMART attributes included.")
    ]
    specific: Annotated[
        StrictBool | StrictStr,
        Field(
            description="Goal should be clear, concise, and well-defined. They answer the questions of who, what, where, when, and why.")
    ]
    measurable: Annotated[
        StrictBool | StrictStr,
        Field(
            description="Goal should be quantifiable and include criteria for tracking progress")
    ]
    achievable: Annotated[
        StrictBool | StrictStr,
        Field(
            description="Goal should be realistic and attainable")
    ]
    relevant: Annotated[
        StrictBool | StrictStr,
        Field(
            description="Goals should align with broader objectives and be relevant to the overall mission or purpose. They should contribute to the organization's or individual's larger strategy or vision.")
    ]
    time_bound: Annotated[
        StrictBool | StrictStr,
        Field(
            description="Goals should have a defined timeframe or deadline")
    ]


class KPIs(BaseModel):
    monthly_traffic: Annotated[
        StrictInt,
        Field(
            description="This refers to the number of people visiting your website or blog monthly as a result of your content marketing efforts.")
        # TODO: You can track other related metrics, such as referral source (where the traffic came from), whether it was paid or organic traffic, which campaign led the visitor to your website, etc.
    ]
    monthly_leads: Annotated[
        StrictInt,
        Field(description="This refers to the number of people")
    ]
    conversion_rates: Annotated[
        StrictFloat,
        Field(
            description="This is the percentage of visitors who become clients or convert in some other way")
    ]
    social_engagement_rates: Annotated[
        StrictInt | StrictFloat,
        Field(
            description="This shows the number or percentage of comments, likes, and shares on social media")
    ]
    onsite_engagement: Annotated[
        StrictInt,
        Field(
            description="How visitors engage with your website, the pathways they take from page to page, and the links they click.")
    ]
    cost_per_lead: Annotated[
        StrictInt,
        Field(
            description="How much money spent to generate each lead through the content marketing efforts")
    ]
    roi: Annotated[
        StrictFloat,
        Field(description="The profitability of your content marketing efforts")
    ]


def get_new_goals():
    # TODO: Update strategy type and smart formatting
    strategy_type = """
    1. Brand awareness: You want to create content that connects with a new audience.

    SMART format: By the end of the first quarter, we will achieve a 10% increase in website visitors. We’ll also see a 15% increase in social media followers through our new content campaign.
    
    2. Lead generation: You want to build a list of potential clients. That means your content should be oriented toward getting your website or social media visitors to sign up for your mailing list, download an ebook, or book a call. These leads can become paying customers down the line.
    
    SMART format: By December, we will have curated a mailing list of 250 new qualified leads. They will be interested in purchasing items from our home technology product range.
    
    3. Increase engagement: You want your audience to interact with your business through comments, likes, and shares to reach new audiences. You also want to build trust and a positive brand image because this can help your audience choose your product or service over those of a competitor.
    
    SMART format: By the end of Q3, our social media engagement rate will have increased by 25%. We will achieve this through interactive quiz content on our Instagram and LinkedIn channels.
    
    4. Client retention: You want your customers to come back again and again. You can do this when you produce valuable, actionable, or practical content. You can integrate sales-focused calls to action here or include discounts and referral codes to keep things aligned with your other marketing tactics.
    
    SMART format: We will increase our client retention by 40% through actionable content, upsells, and exclusive deals on our new product ranges. This will all be delivered through our segmented newsletters on a weekly basis.
    
    5. Lower customer acquisition costs: You want to drive more qualified leads to your website. SEO content in particular has a long life span and encourages organic traffic (website visitors you don’t pay for). As a result, you can lower your ad spend and convert more customers simply by being a valuable resource for them.
      
    SMART format: We will increase our client retention by TODO: ????      
    """

    return False


class CompanyProfile(BaseModel):
    name: Annotated[
        StrictStr,
        Field(description="Name of the company")
    ]
    description: Annotated[
        StrictStr,
        Field(description="Description of the company")
    ]
    goals: Optional[
        Annotated[
            List[SMART_Goal],
            Field(description="List of the company goals")
        ]
    ] = None
    mission: Optional[
        Annotated[
            StrictStr,
            Field(description="The mission of the company")
        ]
    ] = None
    current_KPIs: Optional[
        Annotated[
            KPIs,
            Field(description="The current Key Performance Indicators (KPIS) of the company")
        ]
    ] = None
    goal_KPIS: Optional[
        Annotated[
            KPIs,
            Field(description="The goal Key Performance Indicators (KPIS) of the company for the next period")
        ]
    ] = None
    target_audience: Optional[
        Annotated[
            List_Of_AudienceProfiles,
            Field(description="Target audience profiles that company provides services to")
        ]
    ] = None

    def get_current_KPIs(self):
        if self.current_KPIs is None:
            parser = PydanticOutputParser(pydantic_object=KPIs)
            format_instructions = parser.get_format_instructions()

            prompt = PromptTemplate(
                template="""Based on the Company Profile given determine the ideal key performance indicators (KPIs) the company should track.
                IMPORTANT: Your response must follow the Output Instructions exactly.
                --- Company Profile:
                {company_profile}
                ---
                Output Instructions:
                {format_instructions}
                """,
                input_variables=["company_profile"],
                partial_variables={"format_instructions": format_instructions},
            )

            completion_chain = prompt | llm

            retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=retry_llm,
                                                               max_retries=3
                                                               )

            output = completion_chain.invoke({
                "company_profile": self,
                "response_format": {"type": "json_object"}
            })

            try:
                finalOutput = parser.parse(output.content)
            except Exception as e:
                print(e)
                prompt_value = prompt.format_prompt(company_profile=self, )
                finalOutput = retry_parser.parse_with_prompt(output.content, prompt_value)

            # print("\n\nOutput:")
            # pprint(finalOutput)

            self.current_KPIs = KPIs.parse_obj(finalOutput)

        # TODO: convert to KPI class
        KPIS = """
        1. Traffic: This refers to the number of people visiting your website or blog as a result of your content marketing efforts.

        You can track other related metrics, such as referral source (where the traffic came from), whether it was paid or organic traffic, which campaign led the visitor to your website, etc.
        2. Leads: These are your potential customers; visitors tend to become leads when they sign up for a mailing list, provide their email address in exchange for a download, fill in a form, use a chat box, etc.

        Your content tactics will determine how people become leads, and your metrics will show you what’s working and what’s not.
        3. Conversion rates: This is the percentage of visitors who become clients (or convert in some other way). It’s sometimes more interesting to know this than simply the number of leads you get.

        A conversion rate can tell you which types of content get lots of traffic (and no clients) and, in contrast, the types of content that convert at a higher rate.

        4. Social media engagement rates: This shows the number or percentage of comments, likes, and shares on social media. You can use it to determine which type of content performs best—and on which channel.
        5. Onsite engagement: Here you look at how visitors engage with your website, the pathways they take from page to page, and the links they click. Understanding this can help you optimize your website and digital sales funnels.
        6. Cost per lead: This answers the big question: How much money are you spending to generate each lead through your content marketing efforts? You can find it by dividing content marketing spend by the number of leads generated.
        7. Return on investment (ROI): Finally, we have ROI. Simply put, it measures the profitability of your content marketing efforts. It takes into account the costs of creating and distributing your content as compared to the revenue it generates.
        """

        return self.current_KPIs

    def get_audience(self, audience_count: int) -> List_Of_AudienceProfiles:
        if self.target_audience is None:
            # TODO: Determine an audience profile from LLM if one is not on record
            parser = PydanticOutputParser(pydantic_object=List_Of_AudienceProfiles)

            prompt = hub.pull("cqc/target_profile")

            format_instructions = parser.get_format_instructions()

            # print("Format Instructions:\n%s" % format_instructions)

            # prompt.format(profile_count=profile_count, company_profile=company_profile,
            #             format_instructions=format_instructions)

            # print("Audience Prompt: %s" % prompt)

            # completion_chain = LLMChain(
            #    llm=llm,
            #    prompt=prompt
            # )

            completion_chain = prompt | llm

            retry_parser = RetryWithErrorOutputParser.from_llm(parser=parser, llm=retry_llm,
                                                               max_retries=3
                                                               )


            # print("Chain Input Schema:")
            # pprint(main_chain.input_schema.schema())

            # print("Prompt Input Schema:")
            # pprint(prompt.input_schema.schema())

            output = completion_chain.invoke({
                "profile_count": audience_count,
                "company_profile": self,
                "format_instructions": format_instructions
            })

            try:
                finalOutput = parser.parse(output.content)
            except Exception as e:
                print(e)
                prompt_value = prompt.format_prompt(company_profile=self, profile_count=audience_count, format_instructions=format_instructions)
                finalOutput = retry_parser.parse_with_prompt(output.content, prompt_value)

            """
            finalOutput = []
            async for output in main_chain.astream(
                    {
                        "profile_count": profile_count,
                        "company_profile": company_profile,
                        "format_instructions": format_instructions
                    }
            ):
                print(output, end="|", flush=True)
                finalOutput.append(output)
            """

            print("\n\nOutput:\n%s" % finalOutput)

            self.target_audience = List_Of_AudienceProfiles.parse_obj(finalOutput)

        return self.target_audience


if __name__ == '__main__':
    company_profile = CompanyProfile(
        name="Chris Queen USA",
        description="An online identity to create content to motivate users and sell corresponding affiliate products",
        goals=[
            SMART_Goal(
                detail="Generate 1000 new followers on tiktok each month",
                specific=True,
                measurable=True,
                achievable=True,
                relevant=True,
                time_bound=True

            ),
            SMART_Goal(
                detail='Generate $1,000,000 in annual profits',
                specific=True,
                measurable=True,
                achievable=True,
                relevant=True,
                time_bound=True
            )],
        mission="Be an authority figure online for all things  motivational"

    )
    print("Company Profile")
    pprint(company_profile)
    kpis = company_profile.get_current_KPIs()
    print("KPIs:")
    pprint(kpis)
    #exit(0)
    targets_list = company_profile.get_audience(2)
    print("Target Profile(s):")
    pprint(targets_list)
