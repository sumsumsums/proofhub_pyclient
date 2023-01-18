
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
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)

#
# people collection
#
class Peoples(ProofHubObject):
    
    people = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        if self.people:
            self.people.clear()
        else:
            self.people = []

        for jsonitem in self.json_data:
            objitem = People(self.proofhubApi, jsonitem)
            self.people.append(objitem)

    def getPeoples(self, save=True):
        self.json_data = self.proofhubApi.get_data_array('people')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
            
        self.archive()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/people/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("people.json")