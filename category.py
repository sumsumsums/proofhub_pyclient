"""
categories

Endpoint GET
GET v3/categories
"""
from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

class Category(ProofHubObject):
    """
    single category
    """
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)

class Categories(ProofHubObject):
    """
    categories collection
    """
    
    categories = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        if self.categories:
            self.categories.clear()
        else:
            self.categories = []
        
        for jsonitem in self.json_data:
            objitem = Category(self.proofhubApi, jsonitem)
            self.categories.append(objitem)

    def getCategories(self, save=True):
        self.json_data = self.proofhubApi.get_data_array('categories')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
            
        self.archive()

    def getSubPath(self) -> str:
        return f"categories"

    def saveJson(self):
        self.saveJsonFileNotEmpty("categories.json")