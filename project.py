from proofhub_api import ProofhubApi
from baseobject import ProofHubObject 
from file_api import FileApi

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
        if self.proofhubApi.config.get_tasklists:
            self.todolists = Todolists(self.proofhubApi, self.project_id)
            self.todolists.getTodolists()
        
        # topics / discussions
        if self.proofhubApi.config.get_topics:
            self.topics = Topics(self.proofhubApi, self.project_id)
            self.topics.getTopics()
        
        # folders and files
        if self.proofhubApi.config.get_folders:
            self.folders = Folders(self.proofhubApi, self.project_id)
            self.folders.getFolders()
        
        # notebooks and notes
        if self.proofhubApi.config.get_notebooks:
            self.notebooks = Notebooks(self.proofhubApi, self.project_id)
            self.notebooks.getNotebooks()

#
# projects collection
#
class Projects(ProofHubObject):
    
    projects = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        self.projects.clear()
        
        for jsonitem in self.json_data:
            objitem = Project(self.proofhubApi, jsonitem)
            self.projects.append(objitem)

    def getProjects(self, save=True):
        self.json_data = self.proofhubApi.get_data_array('projects')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        dir = self.getFilePath()
        self.saveJsonFile(dir, "projects.json", self.json_data)
        
        for item in self.projects:
            item.getProjectData()
    
    def getSubPath(self) -> str:
        return "projects"
            
    def archive(self):
        ids = []
        for item in self.projects:
            ids.append(str(item.project_id))
        
        self.archiveItems(ids)
    
