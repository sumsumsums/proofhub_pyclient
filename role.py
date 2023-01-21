"""
roles 

Endpoint GET
GET v3/roles
"""

from proofhub_api import ProofhubApi
from baseobject import ProofHubObject
   
class Role(ProofHubObject):
    """
    single role
    """
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)


class Roles(ProofHubObject):
    """
    roles collection
    """
    
    roles = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        if self.roles:
            self.roles.clear()
        else:
            self.roles = []
        
        for jsonitem in self.json_data:
            objitem = Role(self.proofhubApi, jsonitem)
            self.roles.append(objitem)

    def getRoles(self, save=True):
        self.json_data = self.proofhubApi.get_data_array('roles')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
            
        self.archive()

    def getSubPath(self) -> str:
        return f"roles"

    def saveJson(self):
        self.saveJsonFileNotEmpty("roles.json")