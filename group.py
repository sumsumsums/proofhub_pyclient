from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

# groups 
#
# Endpoint GET
# GET v3/groups

#
# single group
#
class Group(ProofHubObject):
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)

#
# groups collection
#
class Groups(ProofHubObject):
    
    groups = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponses(self):
        if self.groups:
            self.groups.clear()
        else:
            self.groups = []
            
        records = self.getResponseAsArray()
        
        for jsonitem in records:
            objitem = Group(self.proofhubApi, jsonitem)
            self.groups.append(objitem)
            
    def getGroups(self, save=True):
        self.json_data = self.proofhubApi.get_data_string('groups')
        self.parseJsonResponses()
 
        if save == True:
            self.saveJson()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/groups/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("groups.json")