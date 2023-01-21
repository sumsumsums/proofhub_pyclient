"""
notebooks and notes

Endpoint GET
GET v3/projects/<project_id>/notebooks
"""

from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

class Notebook(ProofHubObject):
    """
    single notebook
    """

    project_id = None
    notebook_id = None
    sub_file_path = ""
    notes = None
    
    def __init__(self, proofhubApi: ProofhubApi, sub_file_path, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.sub_file_path = sub_file_path
        self.project_id = project_id
        self.setNotebookId()

    def setNotebookId(self):
        self.notebook_id = self.json_data["id"]

    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/{self.notebook_id}"

    def getNotes(self):
        self.notes = Notes(self.proofhubApi, self.project_id, self.notebook_id)
        self.notes.getNotes()


class Notebooks(ProofHubObject):
    """
    notebooks collection
    """
    
    project_id = None
    notebooks = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.project_id = project_id
        
    def parseJsonResponse(self):
        dir = self.getSubPath()
        
        if self.notebooks:
            self.notebooks.clear()
        else:
            self.notebooks = []
        
        for jsonitem in self.json_data:
            objitem = Notebook(self.proofhubApi, dir, self.project_id, jsonitem)
            self.notebooks.append(objitem)

    def getNotebooks(self, save=True):
        url = f"projects/{self.project_id}/notebooks"

        self.json_data = self.proofhubApi.get_data_array(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        self.saveJsonFileNotEmpty("notebooks.json")
        
        for notebook in self.notebooks:
            notebook.getNotes()

    def getSubPath(self) -> str:
        return f"projects/{self.project_id}/notebooks" 

    def archive(self):
        ids = []
        for item in self.notebooks:
            ids.append(str(item.notebook_id))
        
        self.archiveItems(ids)

class Note(ProofHubObject):
    """
    single note
    """

    note_id = None
    notebook_id = None
    project_id = None
    sub_file_path = ""
    
    def __init__(self, proofhubApi: ProofhubApi, sub_file_path, project_id, notebook_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.sub_file_path = sub_file_path
        self.notebook_id = notebook_id 
        self.project_id = project_id
        self.setNoteId()

    def setNoteId(self):
        self.note_id = self.json_data["id"]

    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/" 

    def getNoteFromList(self, note):
        self.json_data = {}
        if not note:
            return
        elif isinstance(note, dict):
            self.json_data = note.copy()
        elif isinstance(note, list):
            if len(note) > 0:
                self.json_data = note.pop(0).copy()

    #v3/projects/23423233/notebooks/41246749/notes/80731708
    def getNote(self):
        url = f"projects/{self.project_id}/notebooks/{self.notebook_id}/notes/{self.note_id}"

        json_array = self.proofhubApi.get_data_array(url)
        self.getNoteFromList(json_array)
        filename = f"{self.note_id}_note.json"
        self.saveJsonFileNotEmpty(filename)
    
    #v3/projects/23423233/notebooks/41246749/notes/80731708/comments
    def getComments(self):
        if not self.json_data or not self.json_data["comments"] or self.json_data["comments"] == 0:
            return
        
        url = f"projects/{self.project_id}/notebooks/{self.notebook_id}/notes/{self.note_id}/comments"
        
        self.json_data = self.proofhubApi.get_data_array(url)
        filename = f"{self.note_id}_note_comments.json"
        self.saveJsonFileNotEmpty(filename)

class Notes(ProofHubObject):
    """
    notes collection
    """
    
    notebook_id = None
    project_id = None
    notes = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, notebook_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.notebook_id = notebook_id 
        self.project_id = project_id
        
    def parseJsonResponse(self):
        dir = self.getSubPath()
        
        if self.notes:
            self.notes.clear()
        else:
            self.notes = []
        
        for jsonitem in self.json_data:
            objitem = Note(self.proofhubApi, dir, self.project_id, self.notebook_id, jsonitem)
            self.notes.append(objitem)

    def getNotes(self, save=True):
        url = f"projects/{self.project_id}/notebooks/{self.notebook_id}/notes"

        self.json_data = self.proofhubApi.get_data_array(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        self.saveJsonFileNotEmpty("notes.json")
        
        for note in self.notes:
            note.getNote()
            note.getComments()

    def getSubPath(self) -> str:
        return f"projects/{self.project_id}/notebooks/{self.notebook_id}"

    def archive(self):
        ids = []
        for item in self.notes:
            ids.append(str(item.note_id))
        
        self.archiveItems(ids)
