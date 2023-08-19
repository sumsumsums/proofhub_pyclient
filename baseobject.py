"""
base object class
"""

import json
from pathlib import Path

from file_api import FileApi
from proofhub_api import ProofhubApi

class ProofHubObject(object):
    """
    base object class
    """
    
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
            if isinstance(json_data, list):
                for line in json_data:
                    json.dump(line, f)
                    f.write('\n')
            else:
                json.dump(json_data, f) 

    def saveJsonFileNotEmpty(self, filename):
        if not self.json_data or len(self.json_data) == 0:
            return
        
        dir = self.getFilePath()
        self.saveJsonFile(dir, filename, self.json_data)
    
    def getFilePath(self, no_sub=False) -> str:
        base = f"{self.proofhubApi.outputdir}"
        if no_sub == True:
            return base 

        sub = self.getSubPath()
        if len(sub) > 0:
            return f"{base}/{sub}"
        else:
            return base
    
    def getSubPath(self) -> str:
        return ""
    
    def archive(self):
        return

    def archiveItems(self, items):
        if self.proofhubApi.config.archive_deprecated == False:
            return 
        
        fileApi = FileApi(self.proofhubApi.config)
        subdirs = fileApi.getSubDirectories(directory=self.getFilePath())
        if not subdirs:
            return
        
        for key in subdirs:
            found = False
            if items and str(key) in items:
                continue 
            else:
                subdir = subdirs.get(key)
                fileApi.moveDirectoryArchive(subdir, self.getSubPath(), key)