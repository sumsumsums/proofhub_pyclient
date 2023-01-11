from proofhub_api import ProofhubApi
from baseobject import ProofHubObject


# notebooks
#
# Endpoint GET
# GET v3/announcements

#
# single notebook
#
class Notebook(ProofHubObject):

    project_id = None
    notebook_id = None
    root_file_path = ""
    notes = None
    
    def __init__(self, proofhubApi: ProofhubApi, file_path, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.project_id = project_id
        self.setNotebookId()

    def setNotebookId(self):
        self.notebook_id = self.json_data["id"]
    
    def getFilePath(self) -> str:
        return f"{self.root_file_path}/{self.notebook_id}"

    def getNotes(self):
        self.notes = Notes(self.proofhubApi, self.project_id, self.notebook_id)
        self.notes.getNotes()

#
# notebooks collection
#
class Notebooks(ProofHubObject):
    
    project_id = None
    notebooks = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.project_id = project_id
        
    def parseJsonResponse(self):
        dir = self.getFilePath()
        
        if self.notebooks:
            self.notebooks.clear()
        else:
            self.notebooks = []
        
        records = self.getResponseAsArray()
        for jsonitem in records:
            objitem = Notebook(self.proofhubApi, dir, self.project_id, jsonitem)
            self.notebooks.append(objitem)

    def getNotebooks(self, save=True):
        url = f"projects/{self.project_id}/notebooks"

        self.json_data = self.proofhubApi.get_data_string(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def saveJson(self):
        self.saveJsonFileNotEmpty("notebooks.json")
        
        for notebook in self.notebooks:
            notebook.getNotes()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/projects/{self.project_id}/notebooks"

#
# single note
#
class Note(ProofHubObject):

    note_id = None
    notebook_id = None
    project_id = None
    root_file_path = ""
    
    def __init__(self, proofhubApi: ProofhubApi, file_path, project_id, notebook_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.notebook_id = notebook_id 
        self.project_id = project_id
        self.setNoteId()

    def setNoteId(self):
        self.note_id = self.json_data["id"]
    
    def getFilePath(self) -> str:
        return f"{self.root_file_path}/" 

    #v3/projects/23423233/notebooks/41246749/notes/80731708
    def getNote(self):
        url = f"projects/{self.project_id}/notebooks/{self.notebook_id}/notes/{self.note_id}"

        self.json_data = self.proofhubApi.get_data_string(url)
        filename = f"{self.note_id}_note.json"
        self.saveJsonFileNotEmpty(filename)
    
    #v3/projects/23423233/notebooks/41246749/notes/80731708/comments
    def getComments(self):
        if not self.json_data or not self.json_data["comments"] or self.json_data["comments"] == 0:
            return
        
        url = f"projects/{self.project_id}/notebooks/{self.notebook_id}/notes/{self.note_id}/comments"
        
        self.json_data = self.proofhubApi.get_data_string(url)
        filename = f"{self.note_id}_note_comments.json"
        self.saveJsonFileNotEmpty(filename)

#
# notes collection
#
class Notes(ProofHubObject):
    
    notebook_id = None
    project_id = None
    notes = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, notebook_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.notebook_id = notebook_id 
        self.project_id = project_id
        
    def parseJsonResponse(self):
        dir = self.getFilePath()
        
        if self.notes:
            self.notes.clear()
        else:
            self.notes = []
        
        records = self.getResponseAsArray()
        for jsonitem in records:
            objitem = Note(self.proofhubApi, dir, self.project_id, self.notebook_id, jsonitem)
            self.notes.append(objitem)

    def getNotes(self, save=True):
        url = f"projects/{self.project_id}/notebooks/{self.notebook_id}/notes"

        self.json_data = self.proofhubApi.get_data_string(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def saveJson(self):
        self.saveJsonFileNotEmpty("notes.json")
        
        for note in self.notes:
            note.getNote()
            note.getComments()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/projects/{self.project_id}/notebooks/{self.notebook_id}"