#from seleniumwire import webdriver

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireFoxService

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from webdriver_manager.firefox import GeckoDriverManager

from proofhub_api import ProofhubApi

import os
import time

def interceptor(request):
    del request.headers["User-Agent"]
    request.headers["User-Agent"] = "ProofClient (proofhub-client@fmey.org)"
    request.headers["X-API-KEY"] = "4c58546494ba3ee4436696c701d45e7a02a944c2"
    print(request.url)

def interceptor_resp(request, response):  # A response interceptor takes two args
    print(request.url)
    print(request.response.status_code)

class Browserrequest(object):

    proofhub_api: ProofhubApi = None

    def __init__(self, proofhub_api: ProofhubApi=None):
        self.proofhub_api = proofhub_api

    # def newChromeBrowser(self, headless=True, download_path=None):
    #     options = webdriver.ChromeOptions()
    #     if headless:
    #         options.add_argument("headless")
    #     if download_path is not None:
    #         prefs = {}
    #         prefs["profile.default_content_settings.popups"]=0
    #         prefs["download.default_directory"]=download_path
    #         options.add_experimental_option("prefs", prefs)

    #     options.add_argument("start-maximized") # open Browser in maximized mode
    #     options.add_argument("disable-infobars") # disabling infobars
    #     options.add_argument("--disable-extensions") # disabling extensions
    #     options.add_argument("--disable-dev-shm-usage")
    #     options.add_argument("--no-sandbox"); # Bypass OS security model

    #     service = ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    #     browser = webdriver.Chrome(service=service, options=options)
    #     return browser

    # def newFirefoxBrowser(self, download_dir):
    #     options = webdriver.FirefoxOptions()
    #     options.headless = True

    #     options.set_preference("pdfjs.disabled", True)
    #     options.set_preference("browser.download.folderList", 2)
    #     options.set_preference("browser.download.manager.useWindow", False)
    #     options.set_preference("browser.download.dir", download_dir)
    #     options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf, application/force-download")
    #     options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/xlsx, application/force-download")
    #     options.add_argument("--headless")
    #     options.add_argument('--disable-gpu')

    #     service = FireFoxService(GeckoDriverManager().install())
    #     browser = webdriver.Firefox(service=service, options=options)
    #     return browser

    def newFirefoxBrowserProfile(self, download_dir):
        
        extend = "/opt/local/lib/proofhub/scripts/modify_header_value-0.1.8.xpi"
        fp = webdriver.FirefoxProfile()
        fp.add_extension(extend)

        fp.set_preference("modifyheaders.headers.count", 1)
        fp.set_preference("modifyheaders.headers.action0", "Add")
        fp.set_preference("modifyheaders.headers.name0", "X-API-KEY") # Set here the name of the header
        fp.set_preference("modifyheaders.headers.value0", "4c58546494ba3ee4436696c701d45e7a02a944c2") # Set here the value of the header
        fp.set_preference("modifyheaders.headers.enabled0", True)
        fp.set_preference("modifyheaders.config.active", True)
        fp.set_preference("modifyheaders.config.alwaysOn", True)

        options = webdriver.FirefoxOptions()
        options.headless = True
        options.set_preference("pdfjs.disabled", True)
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.useWindow", False)
        options.set_preference("browser.download.dir", download_dir)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf, application/force-download")
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/xlsx, application/force-download")
        options.add_argument("--headless")
        options.add_argument('--disable-gpu')
        
        options.set_preference("browser.safebrowsing.phishing.enabled", False)
        options.set_preference("browser.safebrowsing.malware.enabled", False)
        options.set_preference("browser.safebrowsing.blockedURIs.enabled", False)
        options.set_preference("browser.safebrowsing.downloads.enabled", False)
        options.set_preference("browser.safebrowsing.downloads.remote.enabled", False)
        options.set_preference("browser.safebrowsing.downloads.remote.block_dangerous", False)
        options.set_preference("browser.safebrowsing.downloads.remote.block_dangerous_host", False)
        options.set_preference("browser.safebrowsing.downloads.remote.block_potentially_unwanted", False)
        options.set_preference("browser.safebrowsing.downloads.remote.block_uncommon", False)
        options.set_preference("browser.safebrowsing.downloads.remote.url", "")
        options.set_preference("browser.safebrowsing.provider.*.gethashURL", "")
        options.set_preference("browser.safebrowsing.provider.*.updateURL", "")

        options.set_preference("datareporting.policy.dataSubmissionEnabled", False)
        options.set_preference("toolkit.telemetry.unified", False)
        options.set_preference("toolkit.telemetry.updatePing.enabled", False)
        options.set_preference("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.addons", False)
        options.set_preference("browser.newtabpage.activity-stream.asrouter.userprefs.cfr.features", False)

        options.set_preference("browser.region.update.enabled", False)
        options.set_preference("browser.region.network.url", "")

        options.set_preference("network.connectivity-service.enabled", False)
        options.set_preference("security.family_safety.mode", 0)
        
        options.set_preference("extensions.systemAddon.update.enabled", False)
        options.set_preference("app.update.auto", False)
        options.set_preference("app.update.service.enabled", False)

        service = FireFoxService(GeckoDriverManager().install())
        browser = webdriver.Firefox(service=service, options=options, firefox_profile=fp)
        return browser

    def downloadFile(self, full_url, dirname, filename, forced_download=False):
        # check file already exists
        #if forced_download == False and self.proofhub_api.check_file_exists(filename):
        #    return

        browser = self.newFirefoxBrowserProfile(download_dir=dirname)
        #browser.request_interseptor = interceptor
        #browser.response_interceptor = interceptor_resp
        browser.implicitly_wait(3)
        browser.set_page_load_timeout(3)
        browser.get(full_url)

        for request in browser.requests:
            if request.response:
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type']
        )
            
        self.renameFile(filename, dirname)  
                
        browser.quit()

    def renameFile(self, filename_new, dirname):  
        filename = max([f for f in os.listdir(dirname)])
        if filename:
            time.sleep(2)
            os.rename(os.path.join(dirname, filename), os.path.join(dirname, filename_new))


br = Browserrequest()
# url = "https://aaverify.proofhub.com/files/download/?1665076918/7245590592/d3bc85fb10ee006ced2fd0084ccee16c1673158642mh/fc11af943a47bf6186df0d39488facb8/scammer.xlsx"
url = "https://aaverify.proofhub.com/files/view/doc/?1665076918/7237150852/1f906b0a5b7eb627d479e6e2891ee8ca16734284883v/99061666d7a574634a85706421b4ff5d/Platform+list.docx"
br.downloadFile(url, "/opt/local_data/lib/proofhub/data/tmp", "Platform+list.docx")
        
# browser.get("https://aaverify.proofhub.com/files/download/?1665076918/7245590592/d3bc85fb10ee006ced2fd0084ccee16c1673158642mh/fc11af943a47bf6186df0d39488facb8/scammer.xlsx/dc7941bd86da588d15926d278b3cfac81996494a")
