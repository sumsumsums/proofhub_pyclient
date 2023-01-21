"""
groups

Endpoint GET
GET v3/groups
"""

from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

class Group(ProofHubObject):
    """
    single group
    """
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)

class Groups(ProofHubObject):
    """
    groups collection
    """
    
    groups = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponses(self):
        if self.groups:
            self.groups.clear()
        else:
            self.groups = []
        
        for jsonitem in self.json_data:
            objitem = Group(self.proofhubApi, jsonitem)
            self.groups.append(objitem)
            
    def getGroups(self, save=True):
        self.json_data = self.proofhubApi.get_data_array('groups')
        self.parseJsonResponses()
 
        if save == True:
            self.saveJson()
            
        self.archive()

    def getSubPath(self) -> str:
        return f"groups"

    def saveJson(self):
        self.saveJsonFileNotEmpty("groups.json")