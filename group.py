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
    
    items = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponses(self):
        for jsonitem in self.json_data:
            objitem = Group(self.proofhubApi, jsonitem)
            self.items.append(objitem)
            
    def getGroups(self, save=True):
        self.json_data = self.proofhubApi.get_data_string('groups')
        self.parseJsonResponses()
 
        if save == True:
            self.saveJson()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/groups/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("groups.json")