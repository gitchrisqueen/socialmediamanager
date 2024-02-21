from textwrap import dedent

from langchain.prompts import PromptTemplate

QUOTE_PROMPT = PromptTemplate(
    template_format="jinja2",
    input_variables=["topic"],
    template=dedent(
        """
        Using 100 inspirational quotes that are the closely related to the Topics provided generate an original, motivational quote.
        It should be brief, concise, and easy to understand.
        It has the potential of changing someone's life.
        Use abstraction instead of the actual Topics.
        Use maximum 20 words in your quote.
                
        ---
        Topics: { topic }
        Quote:
        """
    ).strip(),
)

PHOTO_QUERY_PROMPT = PromptTemplate(
    template_format="jinja2",
    input_variables=["quote"],
    template=dedent(
        """
        Use the quote provided to imagine a background image that would go with it.
        Formulate a query that has keywords from your imagined image.
        
        Use maximum 4 words in your query.
        ---
        Quote: {{ quote }}
        Query:
        """
    ).strip(),
)

STORY_PROMPT = PromptTemplate(
    template_format="jinja2",
    input_variables=["quote"],
    template=dedent(
        """
        Use the quote provided to write a motivational speech to go with the quote.
        The speech should have a clear purpose.
        The speech should be written for a specific audience you decide is the ideal target audience for the quote provided.
        Formulate the speech using as many great speech elements as possible.
        You can use the following great speech elements:
        - Ask a question 
        - Tell a personal, professional, or historical story that relates to the quote topic
        - Engaging opening
        - Compelling content
        - Emotional appeal
        - Passion
        - Inspiration to make a positive change
        - A challenge to think differently 
        - Conclusion with a call to action
        Use a maximum 3 paragraphs 
        Use a maximum 2000 characters including spaces
        ---
        Quote: {{ quote }}
        Speech:
        """
    ).strip(),
)


#TODO: Create prompt for 30 days of social media content ideas using trending hashtags and answer the public questions with high searches

SOCIAL_MEDIA_PROMPTS = """
1.	List [X] objectives and goals for building a social media strategy for the topic [Topic].
2.	Generate a detailed social media plan for the topic [Topic]. Include the type of social media content to post, the topics to cover, and the right times to post.
3.	Identify [X] types of social media content on the topic [Topic] that [audience segment] would like to engage with.
4.	Generate X social media posts for Facebook on the topic [Topic], using the tone [assertive, conversational, casual, etc]. Add hashtags and CTA wherever possible. Make sure to create it keeping in mind the [target audience].
5.	Write a Monday Motivation post for LinkedIn. The target audience is [define target audience] Keep the post [define tone]. Include CTA and hashtags where possible.
6.	Generate [X] engaging questions related to the topic [Topic] for posting in a Facebook Group.
7.	Write an informative Twitter post on the topic [Topic]. Also include relevant hashtags.
8.	Write a Twitter thread comprising of X tweets summarizing this blog post: <link to blog post/ add text>
9.	Generate [X] captions for an Instagram post on the topic [topic]. Craft the captions for [target audience] and keep a [specify tone] tone. Include quotes and any other elements to make it more interesting.
10.	Generate [X] options for social media giveaway posts on [holiday name].
11.	Write a long-form LinkedIn post on the topic [Topic] using the tone [assertive, conversational, casual, etc]. Add hashtags and CTA wherever possible.
12.	Suggest [X] ideas for a social media poll on the topic [topic].
13.	Generate a list of ideal click-through rates for social media posts targeting [target audience].
14.	What metrics should I track when creating social media content on the topic [topic]? Include metrics like bounce rate, page views, etc.
15.	Create a monthly social media calendar for this project [Project name and details] in a tabular format. Include post ideas, post timing, post frequency, and engagement strategies in the calendar.


"""
