import json
from pathlib import Path

from proofhub_api import ProofhubApi


##### base object
class ProofHubObject(object):
    
    proofhubApi: ProofhubApi = None
    json_data = ''

    def __init__(self, json_data, proofhubApi: ProofhubApi):
        self.proofhubApi = proofhubApi
        self.json_data = json_data
        
    def saveJsonFile(self, dirname, filename, json_string, mode='w'):
        directory = Path(dirname)
        directory.mkdir(exist_ok=True, parents=True)
        
        filename = f"{dirname}/{filename}"
        
        with open(f"{filename}", mode, encoding='utf-8') as f:
            json.dump(json_string, f) 
    
    def getResponseAsArray(self):
        records = []
        if not self.json_data:
            return records
        
        if isinstance(self.json_data, dict):
            records.append(self.json_data)
        else:
            records = self.json_data
        
        return records

    def saveJsonFileNotEmpty(self, filename):
        records = self.getResponseAsArray()
        if not records:
            return
        else:
            dir = self.getFilePath()
            self.saveJsonFile(dir, filename, self.json_data)  