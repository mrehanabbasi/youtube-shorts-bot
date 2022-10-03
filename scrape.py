"""This file downloads videos from pexels.com and adds random audio to them.

This file will grab the videos in the link provided in the URL variable,
download them, and add random audio from the songs folder to those videos.

License:
    MIT License

    Copyright (c) 2012-2022 M. Rehan Abbasi

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Usage:
    ./scrape.py
"""

import time
import os
import glob
import random
from itertools import islice
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import moviepy.editor as mymovie

# specify the URL of the archive here
URL = "https://www.pexels.com/search/videos/nature/?orientation=portrait"
video_links = []


def get_video_links():
    """This function will get video links from the link in URL variable.

    Returns:
        A list of all the video links available on the link provided in the
        URL variable.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                               options=options)
    browser.maximize_window()
    time.sleep(2)
    browser.get(URL)
    time.sleep(5)

    vids = input("How many videos do you want to download? ")

    soup = BeautifulSoup(browser.page_source, 'lxml')
    links = soup.findAll("source")
    for link in islice(links, int(vids)):
        video_links.append(link.get("src"))

    return video_links


def download_video_series(vid_links):
    """This function will download and add audio to all the videos from links.

    All the videos whose links are provided to this function will be downloaded
    and any random audio for from the songs folder will be added to those
    videos.

    Args:
        vid_links: List of video URL links.
    """
    songs = input("How many songs do you have? ")
    i = 1
    for link in vid_links:
        # iterate through all links in video_links
        # and download them one by one
        # Obtain filename by splitting url and getting last string
        split_link = link.split('/')[-1]
        file_name = split_link.split("?")[0]
        print(f"Downloading video: {file_name}")

        #create response object
        get_request = requests.get(link, stream=True, timeout=None)

        #download started
        with open(file_name, 'wb') as vid_file:
            for chunk in get_request.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    vid_file.write(chunk)

        print(f"{file_name} downloaded!")

        #editing the video
        song_list = random.choice(range(1, int(songs)))
        clip = mymovie.VideoFileClip(file_name)
        clip_duration = clip.duration
        audioclip = mymovie.AudioFileClip(
            f"songs/audio{song_list}.mp3").set_duration(clip_duration)
        new_audioclip = mymovie.CompositeAudioClip([audioclip])
        finalclip = clip.set_audio(new_audioclip)
        finalclip.write_videofile(f"videos/vid{i}.mp4", fps=60)
        print(f"{file_name} has been edited!\n")
        i += 1

    for file in glob.glob("*.mp4"):
        time.sleep(3)
        os.remove(file)
    print("All videos set up successfully!")
    return


if __name__ == "__main__":
    #getting all video links
    video_links = get_video_links()

    #download all videos
    download_video_series(video_links)
