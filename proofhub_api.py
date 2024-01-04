"""
Handles Requests to ProofHub API
"""

import requests
import time
import sys
from pathlib import Path
from config import Config
from requests.models import PreparedRequest

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
        """
        GET Request to ProofHub API, returning the Response object of the request
        """

        self.config.logger.info(url)
        api_response = requests.get(url, headers=self.headers_json)
        return api_response
    
    def send_request_check(self, url, file_request=False) -> requests.Response:
        """
        Requests to ProofHub API, returning the Response object of the request. As ProofHub has a rate limit based on calls per second, 
        it will repeat the requests until it gets a valid response (e.g. not a return code 429)
        """
        
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
                self.config.logger.error(api_response.headers)
                logmsg = f"Exit program after failed request"
                self.config.logger.error(logmsg)
                sys.exit(1)

    def get_data_array(self, prefix, package_requests=True):
        """
        JSON GET request to given URL prefix (without base URL to proofhub instance). Result is returned as array
    
        The ProofHub API just returns up to 100 objects for each request, which is not clearly documented. 
        This method will download all with multiple requests if needed, filling parameters for start and number of objects. It stops, if the request result is empty.
        """

        url_base = self.urlbase + prefix
        
        result = []
        result_request = []
        
        do_request=True
        start = 0
        limit = 90
        
        while do_request == True:
            url = url_base
            
            if package_requests == True:
                params = {'start':str(start),'limit':str(limit)}
                req = PreparedRequest()
                req.prepare_url(url, params)
                url = req.url
                # url = url + "?start=" + str(start) + "&limit=" + str(limit)
            
            api_response = self.send_request_check(url)
            start = start + limit
            
            if not api_response:
                do_request = False
            else:
                result_request.clear()
                
                json_data = api_response.json()
                result_request = self.getResponseAsArray(json_data)
                if len(result_request) > 0:
                    result.extend(result_request)
                
                if package_requests == False or len(result_request) < limit:
                    do_request = False 
        
        return result

    def get_file(self, full_url, dirname, filename, forced_download=False):
        """
        Request for file from ProofHub. It saves the file in a given directory with a give filename.
        If the file exists already, it will not download it again, if forced flag is not set
        """
        
        # check file already exists
        if forced_download == False and self.check_file_exists(filename):
            return
        
        self.config.logger.info("Download file " + dirname + " " + filename + " from " + full_url)
        
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

    def getResponseAsArray(self, json_data):
        records = []
        if not json_data:
            return records
        
        if isinstance(json_data, dict):
            records.append(json_data)
        else:
            records = json_data
        
        return records


                    
