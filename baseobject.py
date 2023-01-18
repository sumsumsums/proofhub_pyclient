import json
from pathlib import Path

from proofhub_api import ProofhubApi


##### base object
class ProofHubObject(object):
    
    proofhubApi: ProofhubApi = None
    json_data = None

    def __init__(self, json_data, proofhubApi: ProofhubApi):
        self.proofhubApi = proofhubApi
        if not json_data:
            self.json_data = []
        elif isinstance(json_data, list):
            self.json_data = []
            self.json_data.extend(json_data)
        elif isinstance(json_data, dict):
            self.json_data = json_data
        else:
            self.json_data = []
        
    def saveJsonFile(self, dirname, filename, json_data, mode='w'):
        directory = Path(dirname)
        directory.mkdir(exist_ok=True, parents=True)
        
        filename = f"{dirname}/{filename}"
        
        with open(f"{filename}", mode, encoding='utf-8') as f:
            json.dump(json_data, f) 

    def saveJsonFileNotEmpty(self, filename):
        if not self.json_data or len(self.json_data) == 0:
            return
        
        dir = self.getFilePath()
        self.saveJsonFile(dir, filename, self.json_data)
    
    def getFilePath(self) -> str:
        base = f"{self.proofhubApi.outputdir}"
        sub = self.getSubPath()
        if len(sub) > 0:
            return f"{base}/sub"
        else:
            return base
    
    def getSubPath(self) -> str:
        return ""
    
    def archive(self):
        return