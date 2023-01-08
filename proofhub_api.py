import requests
import time
import sys
from pathlib import Path

class ProofhubApi(object):
    
    urlbase = ''
    headers = { }
    outputdir = ''

    def __init__(self, urlbase, api_key, user_agent, outputdir=""):
        self.urlbase = urlbase
        self.headers =  {
            'X-API-KEY': api_key,
            'User-Agent': user_agent, 
            'Content-Type': 'application/json'
        }
        
        self.outputdir = outputdir

    def send_request(self, url) -> requests.Response:
        print(url)
        api_response = requests.get(url, headers=self.headers)
        return api_response
    
    def send_request_check(self, url) -> requests.Response:
        
        send_request = True
        
        while send_request == True:
            api_response = self.send_request(url)
            
            json_response = api_response.json()
            if json_response:
                response_error = f"Error during ProofHub request - Response code: {api_response.status_code} ### Response text: {json_response}"
            else:
                response_error = f"Error during ProofHub request - Response code: {api_response.status_code}"
        
            if api_response.status_code == 200:
                send_request = False
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
                sys.exit(response_error)
        

    def get_data_string(self, prefix):
        url = self.urlbase + prefix
        
        api_response = self.send_request_check(url)
        if not api_response:
            sys.exit(1)
        else:
            return api_response.json()
        
    def get_file(self, full_url, dirname, filename, forced_download=False):
        # check file already exists
        if forced_download == False and self.check_file_exists(filename):
            return
        
        api_response = self.send_request_check(full_url)
        if not api_response:
            sys.exit(1)
        elif api_response.status_code == 200:
            directory = Path(dirname)
            directory.mkdir(exist_ok=True, parents=True)
            
            with open(filename, 'wb') as f:
                f.write(api_response.content)
        else:
            sys.exit(1)
    
    def check_file_exists(self, filename):
        fileos = Path(filename)
        return fileos.is_file()

                    
