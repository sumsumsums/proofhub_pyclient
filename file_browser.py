from seleniumwire import webdriver

from selenium.webdriver.chrome.service import Service as ChromeService

from selenium.webdriver.common.by import By

# Used to introduce a waiting mechanism.
from selenium.webdriver.support.ui import WebDriverWait

# Library of useful functions.
from selenium.webdriver.support import expected_conditions as EC


from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.common.exceptions import TimeoutException

from proofhub_api import ProofhubApi

import os
import time
from pathlib import Path
import shutil

proofhub_api: ProofhubApi
user_agent = ""
api_key = ""

file_url = ""
file_name = ""
download_dir = ""
temporary_dir = ""

def getFile(proofhub_access: ProofhubApi, target_dir, filename, url):
    global proofhub_api
    proofhub_api = proofhub_access
    
    global user_agent 
    user_agent = proofhub_api.user_agent
    global api_key 
    api_key = proofhub_api.api_key
    global file_url
    file_url = url
    global file_name
    file_name = filename
    global download_dir
    download_dir = target_dir
    global temporary_dir
    temporary_dir = proofhub_api.config.files_temporary_dir

    if checkFile(False) == False:
        return    

    checkDirectories()
    getFileByChrome(file_url)
    
def checkFile(forced_download=False) -> bool:
    if proofhub_api.config.files_download_browser == False:
        return False

    # check file already exists
    filename = os.path.join(download_dir, file_name)
    if forced_download == False and proofhub_api.check_file_exists(filename):
        return False
    
    return True

def checkDirectories():
    dir_download = Path(download_dir)
    dir_download.mkdir(exist_ok=True, parents=True)
    
    dir_temporary = Path(temporary_dir)
    dir_temporary.mkdir(exist_ok=True, parents=True)

    for file_name in os.listdir(dir_temporary):
        file = os.path.join(temporary_dir, file_name)
        if os.path.isfile(file):
            os.remove(file)


def interceptor(request):
    request.headers["X-API-KEY"] = api_key

def newChromeBrowser() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()

    options.add_argument("headless")
    prefs = {}
    prefs["profile.default_content_settings.popups"]=0
    prefs["download.default_directory"]=temporary_dir
    options.add_experimental_option("prefs", prefs)

    options.add_argument("start-maximized") # open Browser in maximized mode
    options.add_argument("disable-infobars") # disabling infobars
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox"); # Bypass OS security model
    options.add_argument("safebrowsing-disable-download-protection")

    service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    return webdriver.Chrome(service=service, options=options)

def getFileByChrome(full_url):
    browser = newChromeBrowser()
    browser.request_interceptor = interceptor

    try:
        browser.implicitly_wait(20)
        browser.set_page_load_timeout(20)
        browser.delete_all_cookies()
        browser.get(full_url)
    except TimeoutException:
        print("timeout")
    finally:
        time.sleep(3) # for renaming file

        # Access requests via the `requests` attribute
        # for request in browser.requests:
        #     if request.response:
        #         print(
        #             request.url,
        #             request.headers,
        #             request.response.headers
        # )
        
        browser.quit()
        renameFile()

def renameFile():
    for tmp_file in os.listdir(temporary_dir):
        if tmp_file[0].isnumeric() == True:
            filename_new = tmp_file[9:]
        else:
            filename_new = tmp_file[10:]
        new_filename = os.path.join(download_dir, filename_new)
        old_filename = os.path.join(temporary_dir, tmp_file)
        #print(new_filename)
        #print(old_filename)
        shutil.move(old_filename, new_filename)

