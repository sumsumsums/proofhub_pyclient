
from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

# categories
#
# Endpoint GET
# GET v3/categories

#
# single category
#
class Category(ProofHubObject):
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)

#
# categories collection
#
class Categories(ProofHubObject):
    
    items = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        for jsonitem in self.json_data:
            objitem = Category(self.proofhubApi, jsonitem)
            self.items.append(objitem)

    def getCategories(self, save=True):
        self.json_data = self.proofhubApi.get_data_string('categories')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/categories/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("categories.json")