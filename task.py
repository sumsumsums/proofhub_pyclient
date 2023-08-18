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

    def __init__(self, proofhubApi: ProofhubApi, project_id, sub_file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.sub_file_path = sub_file_path
        self.project_id = project_id
        self.setTodolistId()

    def setTodolistId(self):
        self.todolist_id = self.json_data["id"]
    
    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/{self.todolist_id}"
    
    def getTasks(self):
        if self.tasks:
            self.tasks = None

        self.tasks = Tasks(self.proofhubApi, self.project_id, self.todolist_id, self.getSubPath())
        self.tasks.getTasks()


class Todolists(ProofHubObject):
    """
    todolists collection
    """
    
    project_id = None
    todolists = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.project_id = project_id
        
    def parseJsonResponse(self):
        dir = self.getSubPath( )
        
        if self.todolists:
            self.todolists.clear()
        else:
            self.todolist = []
        
        for jsonitem in self.json_data:
            objitem = Todolist(self.proofhubApi, self.project_id, dir, jsonitem)
            self.todolists.append(objitem)

    def getTodolists(self, save=True):
        url = f"/projects/{self.project_id}/todolists"

        self.json_data = self.proofhubApi.get_data_array(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        dir = self.getFilePath( )
        self.saveJsonFile(dir, "todolists.json", self.json_data)
        
        for todolist in self.todolists:
            todolist.getTasks()

    def getSubPath(self) -> str:
        return f"projects/{self.project_id}/todolists"

    def archive(self):
        ids = []
        for item in self.todolists:
            ids.append(str(item.todolist_id))
        
        self.archiveItems(ids)


class Task(ProofHubObject):
    """
    single topic
    """

    task_id = None
    project_id = None 
    todolist_id = None
    sub_file_path = ""
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, todolist_id, sub_file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.sub_file_path = sub_file_path
        self.project_id = project_id
        self.todolist_id = todolist_id
        self.setTaskId()

    def setTaskId(self):
        self.task_id = self.json_data["id"]
    
    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/"

    #GET v3/projects/23423233/todolists/13964085/tasks/13966758/comments
    def getComments(self):
        if "comments" not in self.json_data:
            return
        comments_count = self.json_data["comments"]
        if comments_count == 0:
            return
        
        url = f"projects/{self.project_id}/todolists/{self.todolist_id}/tasks/{self.task_id}/comments"
        
        self.json_data = self.proofhubApi.get_data_array(url)
        filename = f"{self.task_id}_task_comments.json"
        self.saveJsonFileNotEmpty(filename)


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
        
    def parseJsonResponse(self):
        dir = self.getSubPath()
        
        if self.tasks:
            self.tasks.clear()
        else:
            self.tasks = []
        
        for jsonitem in self.json_data:
            objitem = Task(self.proofhubApi, self.project_id, self.todolist_id, dir, jsonitem)
            self.tasks.append(objitem)

    def getTasks(self, save=True):
        url = f"/projects/{self.project_id}/todolists/{self.todolist_id}/tasks"

        self.json_data = self.proofhubApi.get_data_array(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        self.saveJsonFileNotEmpty("tasks.json")

        for task in self.tasks:
            task.getComments()

    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/tasks"
    
    def archive(self):
        ids = []
        for item in self.tasks:
            ids.append(str(item.task_id))
        
        self.archiveItems(ids)
