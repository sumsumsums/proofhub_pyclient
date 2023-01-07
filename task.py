from proofhub_api import ProofhubApi
from proofhubobject import ProofHubObject


# todolists 
#
# Endpoint GET
# GET v3/projects/<project_id>/todolists

#
# single todolist
#
class Todolist(ProofHubObject):
    
    project_id = None
    todolist_id = None
    root_file_path = ""

    def __init__(self, proofhubApi: ProofhubApi, project_id, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.project_id = project_id
        self.setTodolistId()

    def setTodolistId(self):
        self.todolist_id = self.json_data["id"]
    
    def getFilePath(self) -> str:
        return f"{self.root_file_path}/{self.todolist_id}"
    
    def getTasks(self):
        tasks = Tasks(self.proofhubApi, self.project_id, self.todolist_id, self.getFilePath())
        tasks.getTasks()

#
# todolists collection
#
class Todolists(ProofHubObject):
    
    project_id = None
    todolists = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.project_id = project_id
        
    def parseJsonResponse(self):
        dir = self.getFilePath( )
        
        if self.todolists:
            self.todolists.clear()
        else:
            self.todolist = []
        
        for jsonitem in self.json_data:
            objitem = Todolist(self.proofhubApi, self.project_id, dir, jsonitem)
            self.todolists.append(objitem)

    def getTodolists(self, save=True):
        url = f"/projects/{self.project_id}/todolists"

        self.json_data = self.proofhubApi.get_data_string(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def saveJson(self):
        dir = self.getFilePath( )
        self.saveJsonFile(dir, "todolists.json", self.json_data)
        
        for todolist in self.todolists:
            todolist.getTasks()
    
    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/projects/{self.project_id}/todolists"

# tasks
#
# Endpoint GET
# GET v3/projects/<project_id>/todolists/<todolist_id>/tasks

#
# single task
#
class Task(ProofHubObject):

    task_id = None
    root_file_path = ""
    
    def __init__(self, proofhubApi: ProofhubApi, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.setTaskId()

    def setTaskId(self):
        self.task_id = self.json_data["id"]
    
    def getFilePath(self) -> str:
        return f"{self.root_file_path}/{self.task_id}"

#
# task collection
#
class Tasks(ProofHubObject):
    
    todolist_id = None
    project_id = None
    root_file_path = ""
    tasks = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, todolist_id, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.todolist_id = todolist_id
        self.project_id = project_id
        self.root_file_path = file_path
        
    def parseJsonResponse(self):
        dir = self.getFilePath()
        
        if self.tasks:
            self.tasks.clear()
        else:
            self.tasks = []
        
        for jsonitem in self.json_data:
            objitem = Task(self.proofhubApi, dir, jsonitem)
            self.tasks.append(objitem)

    def getTasks(self, save=True):
        url = f"/projects/{self.project_id}/todolists/{self.todolist_id}/tasks"

        self.json_data = self.proofhubApi.get_data_string(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def saveJson(self):
        self.saveJsonFileNotEmpty("tasks.json")

    def getFilePath(self) -> str:
        return f"{self.root_file_path}/tasks"