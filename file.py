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
    sub_file_path = ""
    files = None
    
    def __init__(self, proofhubApi: ProofhubApi, sub_file_path, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.sub_file_path = sub_file_path
        self.project_id = project_id
        self.setFolderId()

    def setFolderId(self):
        self.folder_id = self.json_data["id"]

    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/{self.folder_id}"

    def getFiles(self):
        if self.files:
            self.files = None

        self.files = Files(self.proofhubApi, self.project_id, self.folder_id, self.getSubPath())
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
        dir = self.getSubPath()
        
        if self.folders:
            self.folders.clear()
        else:
            self.folders = []
        
        for jsonitem in self.json_data:
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

        self.json_data = self.proofhubApi.get_data_array(url)
        self.parseJsonResponse()
        if save_lists == True:
            self.saveJson()

        self.archive()

    def saveJson(self):
        self.saveJsonFileNotEmpty("folders.json")
        
        for folder in self.folders:
            folder.getFiles()

    def getSubPath(self) -> str:
        return f"projects/{self.project_id}/folders"

    def archive(self):
        ids = []
        for item in self.folders:
            ids.append(str(item.folder_id))
        
        self.archiveItems(ids)

# files
#
# Endpoint GET
# 

#
# single file
#
class File(ProofHubObject):

    sub_file_path = ""
    file_id = None
    file_name = None

    def __init__(self, proofhubApi: ProofhubApi, sub_file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.sub_file_path = sub_file_path
        self.setFileId()

    def setFileId(self):
        self.file_id = self.json_data["id"]
        self.file_name = self.json_data["name"]

    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/{self.file_name}"

    def getFileUrl(self):
        urlfull = None

        if not "url" in self.json_data:
            return
        if not "file_type" in self.json_data:
            return

        urlbase = self.json_data["url"]

        if "full_image" in urlbase:
            urlfull = urlbase["full_image"]

        if self.json_data["file_type"] == "odt":
            urlfull = None
            return

    def downloadFile(self):
        filename = self.getFilePath()
        urlfull = self.getFileUrl()

        if urlfull == None:
            return

        dir = f"{super().getFilePath(no_sub=True)}/{self.sub_file_path}"
        self.proofhubApi.get_file(urlfull, dir, filename)

#
# files collection
#
class Files(ProofHubObject):

    project_id = None
    folder_id = None
    sub_file_path = ""
    files = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, folder_id, sub_file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.folder_id = folder_id
        self.project_id = project_id
        self.sub_file_path = sub_file_path
        
    def parseJsonResponse(self):
        if self.files:
            self.files.clear()
        else:
            self.files = []

        for jsonitem in self.json_data:
            objitem = File(self.proofhubApi, self.getSubPath(), jsonitem)
            self.files.append(objitem)

    def getFiles(self, save=True):
        url = f"projects/{self.project_id}/folders/{self.folder_id}/files"

        self.json_data = self.proofhubApi.get_data_array(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
    
        self.archive()

    def saveJson(self):
        self.saveJsonFileNotEmpty("files.json")
        
        for file in self.files:
            file.downloadFile()

    def getSubPath(self) -> str:
        return f"{self.sub_file_path}"

    def archive(self):
        ids = []
        for item in self.files:
            ids.append(str(item.file_id))
        
        self.archiveItems(ids)
