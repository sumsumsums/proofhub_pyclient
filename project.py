from proofhub_api import ProofhubApi
from proofhubobject import ProofHubObject 

from task import Todolists
from notes import Notebooks
from file import Folders
from topic import Topics

# projects
#
# Endpoint GET
# GET v3/projects

#
# single project
#
class Project(ProofHubObject):
    
    project_id = ""
    todolists = None 
    topics = None 
    folders = None 
    notebooks = None
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.setProjectId()
    
    def setProjectId(self):
        self.project_id = self.json_data["id"]
        
    def getProjectData(self):
        # todolists / task lists
        self.todolists = Todolists(self.proofhubApi, self.project_id)
        self.todolists.getTodolists()
        
        # topics / discussions
        self.topics = Topics(self.proofhubApi, self.project_id)
        self.topics.getTopics()
        
        # folders and files
        self.folders = Folders(self.proofhubApi, self.project_id)
        self.folders.getFolders()
        
        # notebooks and notes
        self.notebooks = Notebooks(self.proofhubApi, self.project_id)
        self.notebooks.getNotebooks()

#
# projects collection
#
class Projects(ProofHubObject):
    
    items = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        self.items.clear()
        
        for jsonitem in self.json_data:
            objitem = Project(self.proofhubApi, jsonitem)
            self.items.append(objitem)

    def getProjects(self, save=True):
        self.json_data = self.proofhubApi.get_data_string('projects')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def saveJson(self):
        dir = f"{self.proofhubApi.outputdir}/projects"
        self.saveJsonFile(dir, "projects.json", self.json_data)
        
        for item in self.items:
            item.getProjectData()