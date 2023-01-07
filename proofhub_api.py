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

    def get_data_string(self, prefix):
        url = self.urlbase + prefix
        send_request = True
        
        while send_request == True:
            api_response = self.send_request(url)
            send_request = False
            json_response = api_response.json()
            
            response_error = f"Error during ProofHub request - Response code: {api_response.status_code} ### Response text: {json_response}"
            
            if api_response.status_code == 200:
                return json_response
            elif json_response:
                if isinstance(json_response, dict):
                    error = json_response['error']
                    if not error:
                        sys.exit(response_error)
                    elif 'Rate limit exceeded' in error:
                        # sleep 11 seconds
                        send_request = True
                        time.sleep(11)
                    else:
                        sys.exit(response_error)
                else:
                    sys.exit(response_error)
        
    def get_file(self, full_url, dirname, filename, forced_download=False):
        if forced_download == False:
            fileos = Path(filename)
            if fileos.is_file() == True:
                return
        
        totalbits = 0
        url = full_url
        
        headers_file = self.headers
        headers_file['stream'] = 'True'
        
        api_response = requests.get(url, headers=headers_file)
        
        if api_response.status_code == 200:
            directory = Path(dirname)
            directory.mkdir(exist_ok=True, parents=True)
            
            with open(filename, 'wb') as f:
                for chunk in api_response.iter_content(chunk_size=1024):
                    if chunk:
                        totalbits += 1024
                        print("Downloaded",totalbits*1025,"KB...")
                        f.write(chunk)

                    
