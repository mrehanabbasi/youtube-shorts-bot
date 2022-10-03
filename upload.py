"""This file will upload the videos to YouTube.

This file will upload the videos in the videos folder to YouTube via the
Chrome browser referenced. The YouTube account which is needed for this needs
to be logged into that browser and all of the browser windows should be closed.

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
    ./upload.py
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")
options.add_argument(
    "user-data-dir=C:\\Users\\xFlow\\AppData\\Local\\Google\\Chrome Beta\\User Data"
)
options.add_argument("--no-sandbox")
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
print(
    # pylint: disable-next=line-too-long
    "\033[1;31;40m IMPORTANT: Put one or more videos in the *videos* folder in the bot directory. Please make sure to name the video files like this --> Ex: vid1.mp4 vid2.mp4 vid3.mp4 etc.."
)
time.sleep(6)
answer = input(
    # pylint: disable-next=line-too-long
    "\033[1;32;40m Press 1 if you want to spam same video or Press 2 if you want to upload multiple videos: "
)

if int(answer) == 1:
    nameofvid = input(
        # pylint: disable-next=line-too-long
        "\033[1;33;40m Put the name of the video you want to upload (Ex: vid.mp4 or myshort.mp4 etc..) ---> "
    )
    howmany = input(
        "\033[1;33;40m How many times you want to upload this video ---> ")

    for i in range(int(howmany)):
        bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                               options=options)

        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(5)

        file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
        SIMP_PATH = f"videos/{str(nameofvid)}"
        abs_path = os.path.abspath(SIMP_PATH)
        file_input.send_keys(abs_path)

        time.sleep(7)

        next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
        for i in range(3):
            next_button.click()
            time.sleep(5)

        DONE_BUTTON = bot.find_element(By.XPATH, '//*[@id="done-button"]')
        DONE_BUTTON.click()
        time.sleep(5)
        bot.quit()

elif int(answer) == 2:
    print(
        # pylint: disable-next=line-too-long
        "\033[1;31;40m IMPORTANT: Please make sure the name of the videos are like this: vid1.mp4, vid2.mp4, vid3.mp4 ...  etc"
    )
    DIR_PATH = '.\\videos'
    COUNT = 0

    for path in os.listdir(DIR_PATH):
        if os.path.isfile(os.path.join(DIR_PATH, path)):
            COUNT += 1
    print("   ", COUNT,
          " Videos found in the videos folder, ready to upload...")
    time.sleep(6)

    for i in range(COUNT):
        bot = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                               options=options)

        bot.get("https://studio.youtube.com")
        time.sleep(3)
        upload_button = bot.find_element(By.XPATH, '//*[@id="upload-icon"]')
        upload_button.click()
        time.sleep(5)

        file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
        SIMP_PATH = f"videos/vid{str(i + 1)}.mp4"
        abs_path = os.path.abspath(SIMP_PATH)

        file_input.send_keys(abs_path)

        time.sleep(7)

        next_button = bot.find_element(By.XPATH, '//*[@id="next-button"]')
        for i in range(3):
            next_button.click()
            time.sleep(5)

        DONE_BUTTON = bot.find_element(By.XPATH, '//*[@id="done-button"]')
        DONE_BUTTON.click()
        time.sleep(5)
        bot.quit()
