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
    
    def __init__(self, proofhubApi: ProofhubApi, file_path, json_data=None):
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

        comments = self.proofhubApi.get_data_array(url)
        if len(comments) > 0:
            filename = f"{self.announcement_id}_announcement_comments.json"
            self.saveJsonFile(self.root_file_path, filename, comments) 

#
# announcements collection
#
class Announcements(ProofHubObject):
    
    announcements = []
    
    def __init__(self, proofhubApi: ProofhubApi, json_data=None):
        super().__init__(json_data, proofhubApi)
        
    def parseJsonResponse(self):
        dir = self.getFilePath()
        
        for jsonitem in self.json_data:
            objitem = Announcement(self.proofhubApi, dir, jsonitem)
            self.announcements.append(objitem)

    def getAnnouncements(self, save=True):
        resp_list = self.proofhubApi.get_data_array('announcements')
        self.json_data = []
        
        for resp_record in resp_list:
            if not resp_record["announcements"]:
                continue
            ann_record = resp_record["announcements"]
            self.json_data.extend(ann_record)

        self.parseJsonResponse()
        if save == True:
            self.saveJson()
            
        self.archive()

    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/announcements/"

    def saveJson(self):
        self.saveJsonFileNotEmpty("announcements.json")
        
        for announcement in self.announcements:
            announcement.getComments()