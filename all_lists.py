"""
todolists / task collections and tasks

Endpoint GET
GET v3/projects/<project_id>/todolists
"""

from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

class Todolist(ProofHubObject):
    """
    single todolist
    """
    
    project_id = None
    todolist_id = None
    sub_file_path = ""
    tasks = None

    def __init__(self, proofhubApi: ProofhubApi, project_id, sub_file_path, list_id):
        super().__init__("", proofhubApi)
        self.sub_file_path = sub_file_path
        self.project_id = project_id
        self.todolist_id = list_id
    
    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/{self.todolist_id}"
    
    def getTasks(self):
        if self.tasks:
            self.tasks = None

        self.tasks = Tasks(self.proofhubApi, self.project_id, self.todolist_id, self.getSubPath())
        self.tasks.getTasks()


class AllLists(ProofHubObject):
    """
    todolists collection
    """
    
    project_id = None
    todolists = []
    
    def __init__(self, proofhubApi: ProofhubApi):
        super().__init__("", proofhubApi)
        self.project_id = proofhubApi.config.projects_whitelist[0]
        self.list_ids = proofhubApi.config.list_ids

    def getAllLists(self, save=True):
        dir = self.getSubPath()
        for list_id in self.list_ids:
            todolist = Todolist(self.proofhubApi, self.project_id, dir, list_id)
            todolist.getTasks()

    def getSubPath(self) -> str:
        return f"projects/{self.project_id}/todolists"


class Tasks(ProofHubObject):
    """
    task collection
    GET v3/projects/<project_id>/todolists/<todolist_id>/tasks
    """
    
    todolist_id = None
    project_id = None
    sub_file_path = ""
    tasks = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, todolist_id, sub_file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.todolist_id = todolist_id
        self.project_id = project_id
        self.sub_file_path = sub_file_path

    def getTasks(self, save=True):
        url = f"/projects/{self.project_id}/todolists/{self.todolist_id}/tasks"

        self.json_data = self.proofhubApi.get_data_array(url)
        # self.parseJsonResponse()
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        self.saveJsonFileNotEmpty("tasks.json")

        # if self.proofhubApi.config.get_comments:
        #     for task in self.tasks:
        #         task.getComments()

    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/tasks"
