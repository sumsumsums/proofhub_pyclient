#from seleniumwire import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.service import Service as ChromeService

#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.core.utils import ChromeType

from proofhub_api import ProofhubApi

class Browserrequest(object):

    proofhub_api: ProofhubApi = None

    def __init__(self, proofhub_api: ProofhubApi):
        self.proofhub_api = proofhub_api

    # def interceptor(self, request):
    #     del request.headers["User-Agent"]
    #     request.headers["User-Agent"] = self.proofhubApi.user_agent
    #     request.headers["X-API-KEY"] = self.proofhubApi.api_key

    # def newChromeBrowser(headless=True, download_path=None):
    #     # options = webdriver.ChromeOptions()
    #     # if headless:
    #     #     options.add_argument("headless")
    #     # if download_path is not None:
    #     #     prefs = {}
    #     #     prefs["profile.default_content_settings.popups"]=0
    #     #     prefs["download.default_directory"]=download_path
    #     #     options.add_experimental_option("prefs", prefs)

    #     # options.add_argument("start-maximized") # open Browser in maximized mode
    #     # options.add_argument("disable-infobars") # disabling infobars
    #     # options.add_argument("--disable-extensions") # disabling extensions
    #     # options.add_argument("--disable-dev-shm-usage")
    #     # options.add_argument("--no-sandbox"); # Bypass OS security model

    #     # service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    #     # browser = webdriver.Chrome(service=service, options=options)
    #     # return browser

    # def downloadFile(self, full_url, dirname, filename, forced_download=False):
    #     # check file already exists
    #     if forced_download == False and self.proofhub_api.check_file_exists(filename):
    #         return

    #     browser = newChromeBrowser(download_path=dirname)
    #     browser.request_interseptor = interceptor
    #     browser.get(full_url)