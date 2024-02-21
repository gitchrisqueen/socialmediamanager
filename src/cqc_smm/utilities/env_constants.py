import os

# Get constants from .env file
HEADLESS_BROWSER = os.environ['HEADLESS_BROWSER'] == 'True'
WAIT_DEFAULT_TIMEOUT = float(os.environ['WAIT_DEFAULT_TIMEOUT'])
MAX_WAIT_RETRY = int(os.environ['MAX_WAIT_RETRY'])

# Set other constants
TIKTOK_TRENDS_URL = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
TIKTOK_TRENDS_TITLE = 'Trend Discovery: Popular Hashtags On TikTok'



