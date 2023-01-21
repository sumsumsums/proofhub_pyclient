"""
people

Endpoint GET
GET v3/people
"""

from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

class People(ProofHubObject):
    """
    single people
    """
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)


class Peoples(ProofHubObject):
    """
    people collection
    """
    
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

    def getSubPath(self) -> str:
        return f"people"

    def saveJson(self):
        self.saveJsonFileNotEmpty("people.json")