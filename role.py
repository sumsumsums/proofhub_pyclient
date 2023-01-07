from proofhub_api import ProofhubApi
from proofhubobject import ProofHubObject

# roles 
#
# Endpoint GET
# GET v3/roles

#
# single role
#       
class Role(ProofHubObject):
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)

#
# roles collection
#
class Roles(ProofHubObject):
    
    items = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        for jsonitem in self.json_data:
            objitem = Role(self.proofhubApi, jsonitem)
            self.items.append(objitem)

    def getRoles(self, save=True):
        self.json_data = self.proofhubApi.get_data_string('roles')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/roles/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("roles.json")