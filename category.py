
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
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)

#
# categories collection
#
class Categories(ProofHubObject):
    
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

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/categories/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("categories.json")