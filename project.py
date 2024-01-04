"""
projects

Endpoint GET
GET v3/projects
"""

from proofhub_api import ProofhubApi
from baseobject import ProofHubObject 

from task import Todolists
from notes import Notebooks
from file import Folders
from topic import Topics

class Project(ProofHubObject):
    """
    single project
    """
    
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
        if len(self.proofhubApi.config.projects_whitelist) > 0 and \
            not str(self.project_id) in self.proofhubApi.config.projects_whitelist:
                return

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


class Projects(ProofHubObject):
    """
    projects collection
    """
    
    projects = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        self.projects.clear()
        
        for jsonitem in self.json_data:
            objitem = Project(self.proofhubApi, jsonitem)
            self.projects.append(objitem)

    def getProjects(self, save=True):
        self.json_data = self.proofhubApi.get_data_array('projects', package_requests=False)
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
    
