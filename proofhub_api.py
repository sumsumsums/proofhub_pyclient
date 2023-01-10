import requests
import time
import sys
from pathlib import Path
from config import Config

class ProofhubApi(object):
    
    urlbase = ''
    headers_json = { }
    outputdir = ''
    api_key = None
    user_agent = None
    
    config: Config = None

    def __init__(self, config: Config):
        self.config = config
        
        self.urlbase = config.urlbase
        self.api_key = config.api_key
        self.user_agent = config.user_agent
        self.outputdir = config.outputdir
        
        self.headers_json = config.headers
        self.headers_json['Content-Type'] =  'application/json'

    def send_request(self, url) -> requests.Response:
        self.config.logger.info(url)
        api_response = requests.get(url, headers=self.headers_json)
        return api_response
    
    def send_request_check(self, url, file_request=False) -> requests.Response:
        
        send_request = True
        
        while send_request == True:
            api_response = self.send_request(url)
            
            response_error = f"Error during ProofHub request - Response code: {api_response.status_code}"
        
            if api_response.status_code == 200:
                send_request = False
                return api_response
            elif file_request == True and api_response.status_code == 400:
                send_request = False
                logmsg = f"File request returned status {api_response.status_code} for url {url}"
                self.config.logger.error(logmsg)
                return api_response
            elif api_response.status_code == 429:
                # Rate Limits
                # API calls are subject to rate limiting. Exceeding any rate limits will result in requests returning a status code of 429 (Too Many Requests). 
                # Rate limits are 25 requests per 10 second for the same account from the same IP. Check the Retry-After header to learn how many seconds to wait before retrying the request.
                # sleep 11 seconds
                
                sleep_time = 11
                if api_response.headers["Retry-After"]:
                    sleep_time_header = api_response.headers.get("Retry-After")
                    if type(sleep_time_header) == int and sleep_time_header > 0:
                        sleep_time = sleep_time_header

                send_request = True
                time.sleep(sleep_time)
            else:
                send_request = False
                logmsg = f"Request returned status {api_response.status_code} for url {url}"
                self.config.logger.error(logmsg)

    def get_data_string(self, prefix):
        url = self.urlbase + prefix
        
        api_response = self.send_request_check(url)
        if not api_response:
            return []
        else:
            return api_response.json()
        
    def get_file(self, full_url, dirname, filename, forced_download=False):
        # check file already exists
        if forced_download == False and self.check_file_exists(filename):
            return
        
        api_response = self.send_request_check(full_url, file_request=True)
        if not api_response:
            return
        elif api_response.status_code == 400:
            # not supported file type, continue
            return
        elif api_response.status_code == 200:
            directory = Path(dirname)
            directory.mkdir(exist_ok=True, parents=True)
            
            with open(filename, 'wb') as f:
                f.write(api_response.content)
        else:
            return
    
    def check_file_exists(self, filename):
        fileos = Path(filename)
        return fileos.is_file()

                    
