from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

# annoucements 
#
# Endpoint GET
# GET v3/announcements

#
# single announcement
#
class Announcement(ProofHubObject):
    
    announcement_id = ""
    root_file_path = ""
    
    def __init__(self, proofhubApi: ProofhubApi, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.setAnnouncementtId()

    def setAnnouncementtId(self):
        self.announcement_id  = self.json_data["id"]
    
    # comments
    # GET v3/announcements/3628560/comments
    def getComments(self):
        if not self.json_data or not self.json_data["comments"]:
            return
        comments_in = self.json_data["comments"]
        
        if not comments_in["count"] or comments_in["count"] == 0:
            return
        
        url = f"announcements/{self.announcement_id}/comments"

        comments = self.proofhubApi.get_data_string(url)
        if comments:
            filename = f"{self.announcement_id}_announcement_comments.json"
            self.saveJsonFile(self.root_file_path, filename, comments) 

#
# announcements collection
#
class Announcements(ProofHubObject):
    
    announcements = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=""):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        dir = self.getFilePath()
        
        if self.announcements:
            self.announcements.clear()
        else:
            self.announcements = []
        
        if isinstance(self.json_data, dict):
            records = self.json_data["announcements"]
        
            for jsonitem in records:
                objitem = Announcement(self.proofhubApi, dir, jsonitem)
                self.announcements.append(objitem)

    def getAnnouncements(self, save=True):
        self.json_data = self.proofhubApi.get_data_string('announcements')
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/announcements/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("announcements.json")
        
        for announcement in self.announcements:
            announcement.getComments()