
from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

# people 
#
# Endpoint GET
# GET v3/people

#
# single people
#    
class People(ProofHubObject):
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)

#
# people collection
#
class Peoples(ProofHubObject):
    
    items = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        for jsonitem in self.json_data:
            objitem = People(self.proofhubApi, jsonitem)
            self.items.append(objitem)

    def getPeoples(self, save=True):
        self.json_data = self.proofhubApi.get_data_string('people')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/people/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("people.json")