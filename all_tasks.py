"""
todolists / task collections and tasks

"""

from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

class AllTasks(ProofHubObject):
    """
    task collection
    GET v3/alltodo?projects=<projects separated by comma>'
    """
    
    projects = None
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.projects = ",".join(proofhubApi.config.projects_whitelist)

    def getAllTasks(self, save=True):
        url = f"alltodo?projects={self.projects}"

        self.json_data = self.proofhubApi.get_data_array(url)
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        self.saveJsonFileNotEmpty("all_tasks.json")
    
    def archive(self):
        # TODO
        pass
