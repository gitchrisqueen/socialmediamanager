import os


def isTrue(s: str) -> bool:
    return s.lower() in ['true', '1', 't', 'y', 'yes']


# Get constants from GitHub Actions
try:
    IS_GITHUB_ACTION = isTrue(os.environ['GITHUB_ACTION_TRUE'])
except KeyError:
    IS_GITHUB_ACTION = False

# Get constants from .env file
HEADLESS_BROWSER = isTrue(os.environ['HEADLESS_BROWSER'])
WAIT_DEFAULT_TIMEOUT = float(os.environ['WAIT_DEFAULT_TIMEOUT'])
MAX_WAIT_RETRY = int(os.environ['MAX_WAIT_RETRY'])

# Set other constants
TIKTOK_TRENDS_URL = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
TIKTOK_TRENDS_TITLE = 'Trend Discovery: Popular Hashtags On TikTok'
