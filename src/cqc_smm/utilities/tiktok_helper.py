from cqc_smm.utilities.selenium_util import *


# Return a list of the top trending tags (by category if passed)
def get_tiktok_trending_tags(category: str = None) -> list[str]:
    driver, wait = get_session_driver()

    driver.get(TIKTOK_TRENDS_URL)
    # Wait for title to change
    wait.until(EC.title_is(TIKTOK_TRENDS_TITLE))

    original_window = driver.current_window_handle

    top_tags = [];

    # TODO: Login to see more than first 20 results

    if category is None:
        # TODO: Change category based on passed parameter
        do_nothing = ""

    # Get top tags in this category
    hashtag_spans = wait.until(
        lambda d: d.find_elements(By.XPATH, '//span[@class="CardPc_titleText__RYOWo"]'),
        "Waiting for auth buttons")
    top_tags = list(map(lambda x: x.text.replace("#", "").strip(), hashtag_spans))

    # Close the window
    driver.close()

    return top_tags
