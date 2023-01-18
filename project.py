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
    
    items = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        self.items.clear()
        
        for jsonitem in self.json_data:
            objitem = Project(self.proofhubApi, jsonitem)
            self.items.append(objitem)

    def getProjects(self, save=True):
        self.json_data = self.proofhubApi.get_data_array('projects')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
            
        self.archive()

    def saveJson(self):
        dir = self.getRootPath()
        self.saveJsonFile(dir, "projects.json", self.json_data)
        
        for item in self.items:
            item.getProjectData()
            
    def getRootPath(self):
        return f"{self.proofhubApi.outputdir}/projects"
            
    def archive(self):
        if self.proofhubApi.config.archive_deprecated == False:
            return 
        
        fileApi = FileApi(self.proofhubApi.config)
        subdirs = fileApi.getSubDirectories(directory=self.getRootPath())
        for key in subdirs:
            found = False
            for project in self.items:
                if str(key) == str(project.project_id):
                    found = True 
                    break
            
            if found == False:
                subdir = subdirs.get(key)
                fileApi.moveDirectoryArchive(subdir, 'projects', key)
                    
    
