from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

# folders
#
# Endpoint GET
# GET v3/projects/<project_id>/folders

#
# single folder
#
class Folder(ProofHubObject):

    project_id = None
    folder_id = None
    root_file_path = ""
    files = None
    
    def __init__(self, proofhubApi: ProofhubApi, file_path, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.project_id = project_id
        self.setFolderId()

    def setFolderId(self):
        self.folder_id = self.json_data["id"]
    
    def getFilePath(self) -> str:
        return f"{self.root_file_path}/{self.folder_id}"

    def getFiles(self):
        if self.files:
            self.files = None

        self.files = Files(self.proofhubApi, self.project_id, self.folder_id, self.getFilePath())
        self.files.getFiles()

#
# folders collection
#
class Folders(ProofHubObject):
    
    project_id = None
    folders = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.project_id= project_id
        
    def parseJsonResponse(self):
        dir = self.getFilePath()
        
        if self.folders:
            self.folders.clear()
        else:
            self.folders = []
        
        records = self.getResponseAsArray()
        for jsonitem in records:
            objitem = Folder(self.proofhubApi, dir, self.project_id, jsonitem)
            self.folders.append(objitem)
            self.getSubFolder(dir, jsonitem)

    def getSubFolder(self, dir, jsonitem):
        if "children" not in jsonitem:
            return
        
        children = jsonitem["children"]
        for child in children:
            objitem = Folder(self.proofhubApi, dir, self.project_id, child)
            self.folders.append(objitem)
            self.getSubFolder(dir, child)

    def getFolders(self, save_lists=True):
        url = f"projects/{self.project_id}/folders"

        self.json_data = self.proofhubApi.get_data_string(url)
        self.parseJsonResponse()
        if save_lists == True:
            self.saveJson()

    def saveJson(self):
        self.saveJsonFileNotEmpty("folders.json")
        
        for folder in self.folders:
            folder.getFiles()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/projects/{self.project_id}/folders"

# files
#
# Endpoint GET
# 

#
# single file
#
class File(ProofHubObject):

    root_file_path = ""
    file_id = None
    file_name = None
    
    def __init__(self, proofhubApi: ProofhubApi, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.setFileId()

    def setFileId(self):
        self.file_id = self.json_data["id"]
        self.file_name = self.json_data["name"]
    
    def getFilePath(self) -> str:
        return f"{self.root_file_path}/{self.file_name}"
    
    def downloadFile(self):
        filename = self.getFilePath()
        
        if "url" not in self.json_data:
            print("file")
            print(self.json_data)
            return
        urlbase = self.json_data["url"]
        
        if "full_image" in urlbase:
            urlfull = urlbase["full_image"]
       # elif "download" in urlbase:
       #     urlfull = urlbase["download"]
        
        if not urlfull:
            print("file")
            print(self.json_data)
            return
        
        #Files: falls nicht full_image gegeben, über download versuchen?
        
        self.proofhubApi.get_file(urlfull, self.root_file_path, filename)

#
# files collection
#
class Files(ProofHubObject):
    
    project_id = None
    folder_id = None
    root_file_path = ""
    files = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, folder_id, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.folder_id = folder_id
        self.project_id = project_id
        self.root_file_path = file_path
        
    def parseJsonResponse(self):
        dir = self.getFilePath()

        if self.files:
            self.files.clear()
        else:
            self.files = []

        records = self.getResponseAsArray()
        for jsonitem in records:
            objitem = File(self.proofhubApi, dir, jsonitem)
            self.files.append(objitem)

    def getFiles(self, save=True):
        url = f"projects/{self.project_id}/folders/{self.folder_id}/files"

        self.json_data = self.proofhubApi.get_data_string(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def saveJson(self):
        self.saveJsonFileNotEmpty("files.json")
        
        for file in self.files:
            file.downloadFile()

    def getFilePath(self) -> str:
        return f"{self.root_file_path}"