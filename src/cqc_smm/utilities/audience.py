from enum import Enum
from typing import List

# from pydantic import BaseModel, Field, constr
from langchain_core.pydantic_v1 import BaseModel, constr, Field


class AudienceChannels(str, Enum):
    SOCIAL_MEDIA = "Social Media Platforms"
    ONLINE_FORUMS = "Online Forums and Communities"
    BLOGS = "Blogs and Blog Comments"
    VIDEO_PLATFORMS = "Video Platforms"
    MESSAGING_APPS = "Messaging Apps"
    EMAIL = "Email"
    PODCASTS = "Podcasts"
    REVIEW_SITES = "Review Sites"
    ECOMMERCE_PLATFORMS = "E-commerce Platforms"
    WEBINARS_EVENTS = "Webinars and Virtual Events"
    LIVE_STREAMING = "Live Streaming Platforms"
    COLLABORATION_PLATFORMS = "Collaboration Platforms"
    GAMING_COMMUNITIES = "Gaming Communities"
    NEWS_AGGREGATION = "News Aggregation Platforms"
    EDUCATIONAL_PLATFORMS = "Educational Platforms"
    PROFESSIONAL_NETWORKS = "Professional Networks"
    CUSTOMER_SUPPORT = "Customer Support Portals"
    CROWDFUNDING = "Crowdfunding Platforms"
    CROWDSOURCED_CONTENT = "Crowdsourced Content Platforms"
    AR_VR_PLATFORMS = "Augmented Reality/Virtual Reality (AR/VR) Platforms"

    class SOCIAL_MEDIA_SUB(str, Enum):
        FACEBOOK = "Facebook"
        TWITTER = "Twitter"
        INSTAGRAM = "Instagram"
        LINKEDIN = "LinkedIn"
        PINTEREST = "Pinterest"
        SNAPCHAT = "Snapchat"
        TIKTOK = "TikTok"

    class ONLINE_FORUMS_SUB(str, Enum):
        REDDIT = "Reddit"
        QUORA = "Quora"
        STACK_EXCHANGE = "Stack Exchange"

    class BLOGS_SUB(str, Enum):
        PERSONAL_BLOGS = "Personal Blogs"
        BUSINESS_BLOGS = "Business Blogs"
        NEWS_WEBSITES = "News Websites"

    class VIDEO_PLATFORMS_SUB(str, Enum):
        YOUTUBE = "YouTube"
        VIMEO = "Vimeo"

    class MESSAGING_APPS_SUB(str, Enum):
        WHATSAPP = "WhatsApp"
        MESSENGER = "Facebook Messenger"
        TELEGRAM = "Telegram"
        SIGNAL = "Signal"

    class EMAIL_SUB(str, Enum):
        NEWSLETTERS = "Newsletters"
        DIRECT_EMAIL = "Direct Email"

    class PODCASTS_SUB(str, Enum):
        PODCAST_PLATFORMS = "Podcast Platforms"
        PODCAST_COMMUNITIES = "Podcast Communities"

    class REVIEW_SITES_SUB(str, Enum):
        YELP = "Yelp"
        GOOGLE_REVIEWS = "Google Reviews"
        TRIPADVISOR = "TripAdvisor"

    class ECOMMERCE_PLATFORMS_SUB(str, Enum):
        CUSTOMER_REVIEWS = "Customer Reviews"
        ECOMMERCE_WEBSITES = "E-commerce Websites"

    class WEBINARS_EVENTS_SUB(str, Enum):
        WEBINAR_PLATFORMS = "Webinar Platforms"
        VIRTUAL_EVENT_CHAT = "Virtual Event Chat Rooms"

    class LIVE_STREAMING_SUB(str, Enum):
        TWITCH = "Twitch"
        YOUTUBE_LIVE = "YouTube Live"
        FACEBOOK_LIVE = "Facebook Live"

    class COLLABORATION_PLATFORMS_SUB(str, Enum):
        SLACK_CHANNELS = "Slack Channels"
        MICROSOFT_TEAMS = "Microsoft Teams"

    class GAMING_COMMUNITIES_SUB(str, Enum):
        ONLINE_GAMING_FORUMS = "Online Gaming Forums"
        GAMING_CHAT_ROOMS = "Gaming Chat Rooms"

    class NEWS_AGGREGATION_SUB(str, Enum):
        REDDIT_NEWS = "Reddit News Subreddits"
        NEWS_FORUMS = "News Discussion Forums"

    class EDUCATIONAL_PLATFORMS_SUB(str, Enum):
        ONLINE_LEARNING_FORUMS = "Online Learning Forums"
        EDUCATIONAL_WEBSITE_BOARDS = "Educational Website Boards"

    class PROFESSIONAL_NETWORKS_SUB(str, Enum):
        INDUSTRY_SPECIFIC_NETWORKS = "Industry-specific Networks"
        PROFESSIONAL_ASSOCIATION_FORUMS = "Professional Association Forums"

    class CUSTOMER_SUPPORT_SUB(str, Enum):
        HELPDESK_SYSTEMS = "Helpdesk Systems"
        CUSTOMER_SUPPORT_CHAT = "Customer Support Chat"

    class CROWDFUNDING_SUB(str, Enum):
        BACKER_COMMENTS = "Backer Comments"
        CROWDFUNDING_CAMPAIGNS = "Crowdfunding Campaigns"

    class CROWDSOURCED_CONTENT_SUB(str, Enum):
        WIKIPEDIA = "Wikipedia"
        WIKIS = "Wikis"

    class AR_VR_PLATFORMS_SUB(str, Enum):
        VR_CHAT_ROOMS = "VR Chat Rooms"
        AR_VR_COMMUNITY_FORUMS = "AR/VR Community Forums"


class PreferredContentTypes(str, Enum):
    TEXTUAL_CONTENT = "Textual Content"
    VISUAL_CONTENT = "Visual Content"
    VIDEO_CONTENT = "Video Content"
    AUDIO_CONTENT = "Audio Content"
    INTERACTIVE_CONTENT = "Interactive Content"
    LIVE_CONTENT = "Live Content"
    USER_GENERATED_CONTENT = "User-Generated Content"
    SOCIAL_MEDIA_CONTENT = "Social Media Content"
    EMAIL_CONTENT = "Email Content"
    VISUAL_STORYTELLING = "Visual Storytelling"
    VR_AR_CONTENT = "VR and AR Content"
    EDUCATIONAL_CONTENT = "Educational Content"
    DATA_VISUALIZATIONS = "Data Visualizations"
    INFOTAINMENT = "Infotainment"
    LONG_FORM_CONTENT = "Long-Form Content"
    MICRO_CONTENT = "Micro-Content"
    DOCUMENTARIES = "Documentaries"
    CASE_STUDIES_SUCCESS_STORIES = "Case Studies and Success Stories"
    GIFS_ANIMATED_CONTENT = "GIFs and Animated Content"
    EPHEMERAL_CONTENT = "Ephemeral Content"

    class TEXTUAL_CONTENT_SUB(str, Enum):
        BLOG_POSTS = "Blog Posts"
        ARTICLES = "Articles"
        WHITEPAPERS = "Whitepapers"
        EBOOKS = "Ebooks"
        NEWSLETTERS = "Newsletters"
        CASE_STUDIES = "Case Studies"

    class VISUAL_CONTENT_SUB(str, Enum):
        INFOGRAPHICS = "Infographics"
        IMAGES_GRAPHICS = "Images and Graphics"
        MEMES = "Memes"
        SLIDE_DECKS = "Slide Decks"
        VISUAL_QUOTES = "Visual Quotes"

    class VIDEO_CONTENT_SUB(str, Enum):
        EXPLAINER_VIDEOS = "Explainer Videos"
        TUTORIALS = "Tutorials"
        VLOGS = "Vlogs"
        WEBINARS = "Webinars"
        PRODUCT_DEMOS = "Product Demos"
        SHORT_FORM_VIDEOS = "Short-form Videos"

    class AUDIO_CONTENT_SUB(str, Enum):
        PODCASTS = "Podcasts"
        AUDIOBOOKS = "Audiobooks"
        INTERVIEWS = "Interviews"
        MUSIC = "Music"

    class INTERACTIVE_CONTENT_SUB(str, Enum):
        QUIZZES = "Quizzes"
        POLLS = "Polls"
        SURVEYS = "Surveys"
        INTERACTIVE_INFOGRAPHICS = "Interactive Infographics"
        AR_EXPERIENCES = "Augmented Reality Experiences"

    class LIVE_CONTENT_SUB(str, Enum):
        LIVE_STREAMING = "Live Streaming"
        WEBINARS = "Webinars"
        Q_AND_A_SESSIONS = "Q&A Sessions"
        LIVE_CHATS = "Live Chats"

    class USER_GENERATED_CONTENT_SUB(str, Enum):
        REVIEWS_TESTIMONIALS = "Reviews and Testimonials"
        USER_STORIES = "User Stories"
        CONTESTS = "Contests"
        CHALLENGES = "Challenges"

    class SOCIAL_MEDIA_CONTENT_SUB(str, Enum):
        SOCIAL_MEDIA_POSTS = "Social Media Posts"
        STORIES = "Stories"
        REELS = "Reels"
        IGTV = "IGTV"
        LINKEDIN_ARTICLES = "LinkedIn Articles"

    class EMAIL_CONTENT_SUB(str, Enum):
        NEWSLETTERS = "Newsletters"
        DRIP_CAMPAIGNS = "Drip Campaigns"
        PERSONALIZED_EMAILS = "Personalized Emails"
        UPDATES_ANNOUNCEMENTS = "Updates and Announcements"

    class VISUAL_STORYTELLING_SUB(str, Enum):
        COMICS = "Comics"
        STORYBOARDS = "Storyboards"
        VISUAL_NARRATIVES = "Visual Narratives"

    class VR_AR_CONTENT_SUB(str, Enum):
        VR_EXPERIENCES = "VR Experiences"
        AR_FILTERS_LENSES = "AR Filters and Lenses"
        INTERACTIVE_AR_CONTENT = "Interactive AR Content"

    class EDUCATIONAL_CONTENT_SUB(str, Enum):
        ONLINE_COURSES = "Online Courses"
        HOW_TO_GUIDES = "How-to Guides"
        EDUCATIONAL_WEBINARS = "Educational Webinars"
        LEARNING_MODULES = "Learning Modules"

    class DATA_VISUALIZATIONS_SUB(str, Enum):
        CHARTS_GRAPHS = "Charts and Graphs"
        INTERACTIVE_DATA_DASHBOARDS = "Interactive Data Dashboards"

    class INFOTAINMENT_SUB(str, Enum):
        EDUTAINMENT_VIDEOS = "Edutainment Videos"
        FUN_FACTS = "Fun Facts"
        ENTERTAINING_CONTENT = "Entertaining Content with Educational Value"

    class LONG_FORM_CONTENT_SUB(str, Enum):
        IN_DEPTH_ARTICLES = "In-depth Articles"
        LONG_FORM_VIDEOS = "Long-Form Videos"
        EXTENDED_PODCAST_EPISODES = "Extended Podcast Episodes"

    class MICRO_CONTENT_SUB(str, Enum):
        SHORT_SOCIAL_MEDIA_POSTS = "Short Social Media Posts"
        MICROBLOGS = "Microblogs"
        SNACKABLE_CONTENT = "Snackable Content"

    class DOCUMENTARIES_SUB(str, Enum):
        LONG_FORM_VIDEO_DOCUMENTARIES = "Long-form Video Documentaries"
        PODCAST_SERIES = "Podcast Series"

    class CASE_STUDIES_SUCCESS_STORIES_SUB(str, Enum):
        SUCCESS_CASE_ANALYSES = "Success Case Analyses"
        CUSTOMER_SUCCESS_STORIES = "Customer Success Stories"

    class GIFS_ANIMATED_CONTENT_SUB(str, Enum):
        ANIMATED_GIFS = "Animated GIFs"
        SHORT_ANIMATIONS = "Short Animations"

    class EPHEMERAL_CONTENT_SUB(str, Enum):
        STORIES = "Stories"
        TEMPORARY_POSTS_UPDATES = "Temporary Posts and Updates"


class DemographicAttributes(BaseModel):
    age: constr(strip_whitespace=True, min_length=1) = Field(description="Age of the individual.")
    gender: str = Field(description="Gender identity of the individual.")
    marital_status: str = Field(description="Marital status of the individual (e.g., Single, Married, Divorced).")
    income: str = Field(description="Income level of the individual (e.g., Low-income, Middle-income, High-income).")
    education_level: str = Field(description="Highest education level attained by the individual.")
    occupation: str = Field(description="Occupation or job role of the individual.")
    ethnicity_race: str = Field(description="Ethnicity or race of the individual.")
    religion: str = Field(description="Religious affiliation or belief system of the individual.")
    geographic_location: str = Field(
        description="Geographic location or residence of the individual (e.g., Urban, Suburban, Rural).")
    family_size: str = Field(description="Number of individuals in the individual's family.")
    household_type: str = Field(
        description="Type of household the individual resides in (e.g., Single-person, Nuclear family).")
    homeownership: str = Field(description="Homeownership status of the individual (e.g., Homeowner, Renter).")
    language_spoken_at_home: str = Field(description="Primary language spoken at home by the individual.")
    health_status: str = Field(
        description="General health status of the individual (e.g., Excellent, Good, Fair, Poor).")
    disabilities: str = Field(description="Presence of any disabilities experienced by the individual.")
    lifestyle: str = Field(description="Overall lifestyle and daily habits of the individual.")
    interests_hobbies: str = Field(description="Interests and hobbies pursued by the individual.")
    technology_adoption: str = Field(description="Attitude towards and adoption of new technologies.")
    political_affiliation: str = Field(description="Political affiliation or ideological leaning of the individual.")
    social_media_usage: str = Field(description="Frequency and extent of social media usage by the individual.")


class PsychographicAttributes(BaseModel):
    interests: str = Field(description="Hobbies and activities individuals enjoy in their free time.")
    activities: str = Field(description="Specific actions or events individuals participate in regularly.")
    values: str = Field(description="Core beliefs and principles that guide decision-making.")
    attitudes: str = Field(description="General outlook or disposition towards various aspects of life.")
    lifestyle: str = Field(description="The way individuals live their lives, including daily routines and habits.")
    personality_traits: str = Field(description="Enduring characteristics that define an individual's personality.")
    opinions: str = Field(description="Personal viewpoints on specific topics or issues.")
    social_class: str = Field(description="Economic and social status within a society.")
    social_activities: str = Field(description="Participation in social events and gatherings.")
    innovativeness: str = Field(description="Willingness to adopt new ideas, products, or technologies.")
    leisure_time_activities: str = Field(description="How individuals spend their leisure hours.")
    cultural_preferences: str = Field(
        description="Preferences for specific cultural elements like music, art, or literature.")
    motivations: str = Field(description="Underlying factors that drive individuals to take certain actions.")
    buying_motivations: str = Field(description="Factors influencing purchasing decisions.")
    product_preferences: str = Field(description="Preferred brands, products, or services.")
    brand_loyalty: str = Field(description="Degree of attachment or loyalty to specific brands.")
    media_consumption_habits: str = Field(
        description="Preferences for types of media, such as TV, radio, or online platforms.")
    information_sources: str = Field(description="Preferred channels for obtaining information.")
    online_behavior: str = Field(description="Activities and engagement patterns on the internet.")
    technology_adoption: str = Field(description="Willingness to embrace and use new technologies.")
    environmental_concerns: str = Field(description="Attitudes towards environmental issues and sustainability.")
    health_and_wellness: str = Field(description="Interest in maintaining a healthy lifestyle.")
    travel_preferences: str = Field(description="Preferences for travel destinations and styles.")
    social_media_engagement: str = Field(description="Level of involvement and interaction on social media platforms.")
    cultural_influences: str = Field(description="Impact of cultural factors on individual preferences.")
    fashion_and_style: str = Field(description="Personal choices in clothing and overall style.")
    food_preferences: str = Field(description="Dietary choices and preferences for certain cuisines.")
    relationships: str = Field(description="Attitudes towards friendships, family, and romantic relationships.")
    education_and_learning: str = Field(description="Attitudes towards learning and acquiring new knowledge.")
    personal_values: str = Field(description="Fundamental principles that guide ethical and moral decisions.")


class AudienceProfile(BaseModel):
    profile_name: str = Field(
        description='a concise, alliterative name for the target audience, like "Marketing Mary."')
    demographic_info: DemographicAttributes = Field(description="Demographic information about the target audience.")
    psychographic_info: PsychographicAttributes = Field(
        description="Psychographic information, capturing the lifestyle and interests of the target audience.")
    goals: List[str] = Field(description="Goals and aspirations of the target audience.")
    challenges: List[str] = Field(description="Challenges faced by the target audience.")
    pain_points: List[str] = Field(description="Pain points or difficulties experienced by the target audience.")
    values: List[str] = Field(description="Core values and beliefs important to the target audience.")
    preferred_channels: List[AudienceChannels] = Field(
        description="Preferred communication channels for the target audience.")
    preferred_content_types: List[PreferredContentTypes] = Field(
        description="Preferred types of content for the target audience.")
    buying_behavior: str = Field(description="Buying behavior and patterns exhibited by the target audience.")


class List_Of_AudienceProfiles(BaseModel):
    profile_list: List[AudienceProfile]
