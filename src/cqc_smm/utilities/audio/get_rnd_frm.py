import requests
import json
from bs4 import BeautifulSoup
import random
import os
from os.path import exists
from mutagen.mp3 import MP3
import feedparser
from pytube import YouTube
from pytube import Playlist
import subprocess
import multiprocessing
from urllib.request import urlopen
import urllib

HEADERS = ({'User-Agent': \
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36', \
            'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5'})


def get_length(filename):
    # Unfortunately ffprobe is required
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def load_soup(wikiurl):
    # table_class="wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    del response
    return (soup)


def get_rndm_BenSound_rfmp3_link():
    # 1. Get mp3 download links from BenSound.com
    mp3_links_bensound = []

    for i in range(5):
        query_url = 'https://www.bensound.com/free-music-for-videos/' + str(i + 1)
        soup = load_soup(query_url)
        free_mp3_files = json.loads(
            str(soup.find_all('script')).split('amplitudeSongs = ')[1].split('var currentFilters')[0].replace(";", ""))
        for mp3 in free_mp3_files:
            mp3_links_bensound.append(mp3['url'])
        # removing the new line characters

    # making this part multiprocessing doesn't speed up
    """
    page_i = [0,1,2,3,4]
    pool = multiprocessing.Pool(processes=16)
    mp3_links_bensound_pages=pool.starmap(get_url_from_BenSound_page, zip(page_i))
    pool.close()
    #print(mp3_links_bensound_pages)
    for i in range(len(mp3_links_bensound_pages)):
        mp3_links_bensound = mp3_links_bensound + mp3_links_bensound_pages[i]
    #print(mp3_links_bensound)
    """
    return (random.choice(mp3_links_bensound))


def get_rndm_mixkit_rfmp3_link():
    # 3. Read mp3 links from https://mixkit.co/free-stock-music/
    query_url = 'https://mixkit.co/free-stock-music/'
    soup = load_soup(query_url)
    div_list = soup.find_all('div', {"data-controller": "audio-player"})
    mp3_links_mixkit = []
    for link in div_list:
        mp3_links_mixkit.append(link['data-audio-player-preview-url-value'])
    return (random.choice(mp3_links_mixkit))


def get_rndm_mp3_link_cctrax_url(page_url):
    soup_page = load_soup(page_url)
    links = soup_page.find_all('a', {"data-original-title": "Download this track"}, href=True)
    mp3_links_cctrax_page = []
    for url in links:
        if ".mp3" in url['href']:
            mp3_links_cctrax_page.append(url['href'])
    if len(mp3_links_cctrax_page) == 0:
        return ("")
    else:
        return (random.choice(mp3_links_cctrax_page))


def get_rndm_cctrax_rfmp3_link():
    # 4. Read mp3 links from cctrax
    query_url = 'https://cctrax.com/indexed-releases?format_id=10'
    soup = load_soup(query_url)
    page_links = soup.find_all('a', {"class": "https://creativecommons.org/licenses/by/4.0"}, href=True)
    page_urls = []
    for link in page_links:
        page_urls.append("https://cctrax.com" + link['href'])
    """
    mp3_links_cctrax=[]
    for page_url in page_urls:
        mp3_link_cctrax_page = get_rndm_mp3_link_cctrax_url(page_url)
        if mp3_link_cctrax_page!="":
            mp3_links_cctrax.append(mp3_link_cctrax_page)
    """
    pool = multiprocessing.Pool(processes=16)
    mp3_links_cctrax = pool.map(get_rndm_mp3_link_cctrax_url, page_urls)
    pool.close()

    return (random.choice(mp3_links_cctrax))


def get_rndm_incompetech_rfmp3_link():
    # 5. Read mp3 links from incompetech
    query_url = 'https://incompetech.com/music/royalty-free/pieces.json'
    response = urlopen(query_url)
    data_json = json.loads(response.read())
    rndm_item = random.choice(data_json)
    mp3_link_incompetech = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + rndm_item[
        'filename'].replace(" ", "%20")
    return (mp3_link_incompetech)


def get_rndm_jamendo_rfmp3_link(query_rows):
    # 6. Read mp3 links from incompetech
    query_url = 'https://solrcloud.jamendo.com/solr/jamcom?rows=' + str(query_rows) + '&q=*&by=bestseller'
    req = urllib.request.Request(query_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36')
    req.add_header('Accept-Language', 'en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja;q=0.5')
    response = urlopen(req)
    data_json = json.loads(response.read())
    return ("https://storage.jamendo.com/download/track/" + random.choice(data_json['response']['docs'])['id'])


def get_rndm_page_link_pacdv_url(page_url):
    soup_page = load_soup(page_url)
    page_links = soup_page.find_all('a', href=True)
    page_urls = []
    for link in page_links:
        if "free-music-" in link['href']:
            page_urls.append("https://www.pacdv.com/sounds/" + link['href'])
    return (random.choice(page_urls))


def get_rndm_pacdv_rfmp3_link():
    query_urls = ['https://www.pacdv.com/sounds/free-music.html', \
                  'https://www.pacdv.com/sounds/free-music-2.html', \
                  'https://www.pacdv.com/sounds/free-music-3.html', \
                  'https://www.pacdv.com/sounds/free-music-4.html']
    pool = multiprocessing.Pool(processes=16)
    page_links = pool.map(get_rndm_page_link_pacdv_url, query_urls)
    pool.close()
    soup = load_soup(random.choice(page_links))
    # print(random.choice(page_links)+"\n")
    a_links = soup.find_all('a', href=True)
    for link in a_links:
        if ".mp3" in link['href']:
            return ("https://www.pacdv.com/sounds/" + link['href'])


def get_rndm_danosongs_rfmp3_link():
    query_url = 'https://danosongs.com/'
    soup_page = load_soup(query_url)
    a_links = soup_page.find_all('a', href=True)
    page_links = []
    for link in a_links:
        if "trackship" in link['href']:
            page_links.append("https://danosongs.com" + link['href'])

    page_url = random.choice(page_links)
    soup_page = load_soup(page_url)
    return (str(soup_page).split('attr("href", "')[1].split("?response")[0])


def get_rndm_page_link_freepd_url(page_url):
    soup_page = load_soup(page_url)
    page_links = soup_page.find_all('a', href=True)
    page_urls = []
    for link in page_links:
        if ".mp3" in link['href']:
            page_urls.append("https://freepd.com/" + link['href'])
    rndm_link = random.choice(page_urls).replace(" ", "%20")
    return (rndm_link)


def get_rndm_freepd_rfmp3_link():
    query_urls = ['https://freepd.com/upbeat.php', \
                  'https://freepd.com/epic.php', \
                  'https://freepd.com/horror.php', \
                  'https://freepd.com/romantic.php', \
                  'https://freepd.com/comedy.php', \
                  'https://freepd.com/world.php', \
                  'https://freepd.com/scoring.php', \
                  'https://freepd.com/electronic.php', \
                  'https://freepd.com/misc.php', \
                  'https://freepd.com/Page2/']

    return (get_rndm_page_link_freepd_url(random.choice(query_urls)))


def get_rndm_teknoaxe_rfmp3_link():
    query_url = random.choice(
        [
            "https://teknoaxe.com/Link_Code_3.php?q=1875&amp;genre=Techno", \
            "https://teknoaxe.com/Link_Code_3.php?q=1834&amp;genre=Dubstep", \
            "https://teknoaxe.com/Link_Code_3.php?q=1858&amp;genre=Electro", \
            "https://teknoaxe.com/Link_Code_3.php?q=1865&amp;genre=Drum_and_Bass", \
            "https://teknoaxe.com/Link_Code_3.php?q=1875&amp;genre=Breakbeats", \
            "https://teknoaxe.com/Link_Code_3.php?q=1874&amp;genre=Downtempo", \
            "https://teknoaxe.com/Link_Code_3.php?q=1602&amp;genre=Urban", \
            "https://teknoaxe.com/Link_Code_3.php?q=1872&amp;genre=Rock", \
            "https://teknoaxe.com/Link_Code_3.php?q=1872&amp;genre=Metal", \
            "https://teknoaxe.com/Link_Code_3.php?q=1860&amp;genre=Hard", \
            "https://teknoaxe.com/Link_Code_3.php?q=1868&amp;genre=Soft", \
            "https://teknoaxe.com/Link_Code_3.php?q=1838&amp;genre=Funk", \
            "https://teknoaxe.com/Link_Code_3.php?q=1828&amp;genre=Retro", \
            "https://teknoaxe.com/Link_Code_3.php?q=1869&amp;genre=Eight", \
            "https://teknoaxe.com/Link_Code_3.php?q=1871&amp;genre=Orchestra", \
            "https://teknoaxe.com/Link_Code_3.php?q=1873&amp;genre=Action", \
            "https://teknoaxe.com/Link_Code_3.php?q=1875&amp;genre=Suspense", \
            "https://teknoaxe.com/Link_Code_3.php?q=1693&amp;genre=Horror", \
            "https://teknoaxe.com/Link_Code_3.php?q=1842&amp;genre=Drama", \
            "https://teknoaxe.com/Link_Code_3.php?q=1836&amp;genre=Comedy", \
            "https://teknoaxe.com/Link_Code_3.php?q=1873&amp;genre=World", \
            "https://teknoaxe.com/Link_Code_3.php?q=1824&amp;genre=Percussion", \
            "https://teknoaxe.com/Link_Code_3.php?q=1540&amp;genre=Piano", \
            "https://teknoaxe.com/Link_Code_3.php?q=1524&amp;genre=Loop", \
            "https://teknoaxe.com/Link_Code_3.php?q=1638&amp;genre=Trailer", \
            "https://teknoaxe.com/Link_Code_3.php?q=1784&amp;genre=Halloween", \
            "https://teknoaxe.com/Link_Code_3.php?q=1353&amp;genre=Holiday"])

    soup_page = load_soup(query_url)
    a_links = soup_page.find_all('a', href=True)
    page_links = []
    for link in a_links:
        if "Link_Code_3.php" in link['href']:
            page_links.append("https://teknoaxe.com/" + link['href'])
    page_url = random.choice(page_links)
    soup_page = load_soup(page_url)
    a_links = soup_page.find_all('a', href=True)
    for link in a_links:
        if "direct_download.php" in link['href']:
            return ("https://teknoaxe.com/" + link['href'])


def get_rndm_amachamusic_rfmp3_link():
    url = 'https://amachamusic.chagasi.com/'
    soup_page = load_soup(url)
    page_links = soup_page.find_all('a', href=True)
    page_urls = []
    for link in page_links:
        if any(ext in link['href'] for ext in ['image_', 'genre_']):
            page_urls.append(link['href'])
    rndn_page_url = url + random.choice(page_urls)
    del soup_page
    soup_page = load_soup(rndn_page_url)
    page_links = soup_page.find_all('a', href=True)
    mp3_link_urls = []
    for link in page_links:
        if '.mp3' in link['href']:
            mp3_link_urls.append(link['href'])
    return (url + random.choice(mp3_link_urls))


def get_rndmfiftysounds_rfmp3_link():
    url = random.choice([
        'https://www.fiftysounds.com/royalty-free-music/most-popular-music.html', \
        'https://www.fiftysounds.com/royalty-free-music/audio-logos.html', \
        'https://www.fiftysounds.com/royalty-free-music/audio-logos-2.html', \
        'https://www.fiftysounds.com/royalty-free-music/pop-corporate.html', \
        'https://www.fiftysounds.com/royalty-free-music/pop-corporate-2.html', \
        'https://www.fiftysounds.com/royalty-free-music/cinematic.html', \
        'https://www.fiftysounds.com/royalty-free-music/cinematic-epic.html', \
        'https://www.fiftysounds.com/royalty-free-music/cinematic-comedy.html', \
        'https://www.fiftysounds.com/royalty-free-music/cinematic-drama.html', \
        'https://www.fiftysounds.com/royalty-free-music/cinematic-romantic.html', \
        'https://www.fiftysounds.com/royalty-free-music/cinematic-fantasy.html', \
        'https://www.fiftysounds.com/royalty-free-music/cinematic-horror.html', \
        'https://www.fiftysounds.com/royalty-free-music/vocal.html', \
        'https://www.fiftysounds.com/royalty-free-music/piano.html', \
        'https://www.fiftysounds.com/royalty-free-music/ambient.html', \
        'https://www.fiftysounds.com/royalty-free-music/electronic.html', \
        'https://www.fiftysounds.com/royalty-free-music/children.html', \
        'https://www.fiftysounds.com/royalty-free-music/classical.html', \
        'https://www.fiftysounds.com/royalty-free-music/world-beat.html', \
        'https://www.fiftysounds.com/royalty-free-music/christmas.html', \
        'https://www.fiftysounds.com/royalty-free-music/crazy-music.html', \
        'https://www.fiftysounds.com/royalty-free-music/short-edits.html', \
        'https://www.fiftysounds.com/royalty-free-music/short-edits-2.html', \
        'https://www.fiftysounds.com/royalty-free-music/short-edits-3.html', \
        'https://www.fiftysounds.com/royalty-free-music/pop-loops.html', \
        'https://www.fiftysounds.com/royalty-free-music/electronic-loops.html', \
        'https://www.fiftysounds.com/royalty-free-music/ambient-loops.html', \
        'https://www.fiftysounds.com/royalty-free-music/cinematic-loops.html', \
        'https://www.fiftysounds.com/royalty-free-music/children-loops.html', \
        'https://www.fiftysounds.com/royalty-free-music/ethnic-loops.html', \
        'https://www.fiftysounds.com/royalty-free-music/beds.html', \
        'https://www.fiftysounds.com/royalty-free-music/beds-2.html', \
        'https://www.fiftysounds.com/royalty-free-music/happy.html', \
        'https://www.fiftysounds.com/royalty-free-music/happy-2.html', \
        'https://www.fiftysounds.com/royalty-free-music/dreamy.html', \
        'https://www.fiftysounds.com/royalty-free-music/epic.html', \
        'https://www.fiftysounds.com/royalty-free-music/relaxing.html', \
        'https://www.fiftysounds.com/royalty-free-music/romantic.html', \
        'https://www.fiftysounds.com/royalty-free-music/sad.html'])
    soup = load_soup(url)
    page_links = soup.find_all('div', {'class': 'image'})
    mp3_links = []
    for link in page_links:
        if ".mp3" in link['data-audio']:
            mp3_links.append(link['data-audio'][2:])
    return ("https://www.fiftysounds.com" + random.choice(mp3_links))


def get_rndm_rfmp3(min_length_in_sec):
    if not os.path.isdir('.//audios'):
        os.makedirs('.//audios')

    too_short = 1
    while (too_short):
        random_mp3_url_valid = 0
        while (random_mp3_url_valid == 0):
            method = random.choice([1, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            # print("method no. = "+str(method))

            if (method == 1):
                # 1. Get mp3 download links from BenSound.com
                random_mp3_url = get_rndm_BenSound_rfmp3_link()
            elif (method == 3):
                # 3. Read mp3 links from https://mixkit.co/free-stock-music/
                random_mp3_url = get_rndm_mixkit_rfmp3_link()
            elif (method == 4):
                # 4. Read mp3 links from cctrax
                random_mp3_url = get_rndm_cctrax_rfmp3_link()
            elif (method == 5):
                random_mp3_url = get_rndm_incompetech_rfmp3_link()
            elif (method == 6):
                random_mp3_url = get_rndm_jamendo_rfmp3_link(50)
            elif (method == 7):
                random_mp3_url = get_rndm_pacdv_rfmp3_link()
            elif (method == 8):
                random_mp3_url = get_rndm_danosongs_rfmp3_link()
            elif (method == 9):
                random_mp3_url = get_rndm_freepd_rfmp3_link()
            elif (method == 10):
                random_mp3_url = get_rndm_amachamusic_rfmp3_link()
            elif (method == 11):
                random_mp3_url = get_rndmfiftysounds_rfmp3_link()

            if (random_mp3_url is None):
                random_mp3_url_valid = 0
            else:
                random_mp3_url_valid = 1

        mp3_file = './audios/' + random_mp3_url.split("/")[-1]
        if ".mp3" not in mp3_file:
            mp3_file = mp3_file + ".mp3"
        file_exists = exists(mp3_file)
        if (file_exists == False):
            response = requests.get(random_mp3_url)
            open(mp3_file, "wb").write(response.content)
        else:
            pass
        try:
            if (MP3(mp3_file).info.length > min_length_in_sec):
                too_short = 0
        except:
            too_short = 1
            os.remove(mp3_file)
    print("Source : " + random_mp3_url)
    #print("Save as " + mp3_file)
    print("Music length is " + str(MP3(mp3_file).info.length) + " seconds")

    audio_info = {
        "source_url": random_mp3_url,
        # "file": mp3_file,
        "length": str(MP3(mp3_file).info)}
    os.remove(mp3_file)
    return audio_info


def get_rndm_yt_rfm(min_length_in_sec):
    # Find a random royalty-free-music (RFM) from YouTube
    too_short = 1
    while (too_short):
        method = random.choice([1, 2])
        # print("method no. = "+str(method))
        if (method == 1):
            yt_chan_id = random.choice(['UCQsBfyc5eOobgCzeY8bBzFg', \
                                        'UCht8qITGkBvXKsR1Byln-wA', \
                                        'UCqn1V54Y8IwTsjPrQHKtzGw', \
                                        'UCyytiQuL-5S59OX1opqG-bQ', \
                                        'UCUFDNffZtBGisDliMx12fYw', \
                                        'UC4wUSUO1aZ_NyibCqIjpt0g', \
                                        'UC_aEa8K-EOJ3D6gOs7HcyNg', \
                                        'UCEickjZj99-JJIU8_IJ7J-Q', \
                                        'UCxQri31wIz6_pOIwekUOgHw' \
                                        ])
            channel_url = feedparser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=" + yt_chan_id)
            video_link = random.choice(channel_url.entries)['link']
        elif (method == 2):
            yt_playlist = random.choice([
                'https://www.youtube.com/playlist?list=PLHEabrqpFr0PlkzCTrgZ6ChhrtKSAgqyj', \
                'https://www.youtube.com/playlist?list=PLZ1emuJ65jC2_9dyfHqVwff3Am3H1JKSz', \
                'https://www.youtube.com/playlist?list=PLZ1emuJ65jC2BwjgMqbQfKKYwtAtrKTwX'])
            playlist_urls = Playlist(yt_playlist)
            video_link = random.choice(playlist_urls)

        # extract only audio
        yt = YouTube(video_link)
        video = yt.streams.filter(only_audio=True).first()

        # download the file
        out_filename = video.download(output_path="./audios/")
        out_filename = "./audios/" + out_filename.split("./audios/")[1]
        new_filename = "./audios/" + video_link.split("watch?v=")[1] + ".mp4"
        os.rename(out_filename, new_filename)
        mp4_audio_length = get_length(new_filename)
        if (mp4_audio_length > min_length_in_sec):
            too_short = 0
        else:
            too_short = 1
            os.remove(new_filename)
    print("Source : " + video_link)
    print("Save as " + new_filename)
    print("Music length is " + str(mp4_audio_length) + " seconds")
    return ()