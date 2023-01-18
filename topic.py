from proofhub_api import ProofhubApi
from baseobject import ProofHubObject

# topics and topic comments
#
# Endpoint GET
# GET v3/projects/<project_id>/topics

#
# single topic
#
class Topic(ProofHubObject):

    sub_file_path = ""
    topic_id = None
    project_id = None

    def __init__(self, proofhubApi: ProofhubApi, project_id, sub_file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.sub_file_path = sub_file_path
        self.project_id = project_id
        self.setTopicId()

    def setTopicId(self):
        self.topic_id = self.json_data["id"]
    
    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/{self.topic_id}"
    
    def getTopicComments(self):
        if not self.json_data or not self.json_data ["comments"]:
            return
        
        comments_json = self.json_data["comments"]
        if not comments_json["count"] or comments_json["count"] == 0:
            return

        comments = TopicComments(self.proofhubApi, self.project_id, self.topic_id, self.getSubPath())
        comments.getTopicComments()

#
# topics collection
#
class Topics(ProofHubObject):
    
    project_id = None
    topics = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.project_id = project_id
        
    def parseJsonResponse(self):
        dir = self.getSubPath( )
        
        if self.topics:
            self.topics.clear()
        else:
            self.topics = []

        for jsonitem in self.json_data:
            objitem = Topic(self.proofhubApi, self.project_id, dir, jsonitem)
            self.topics.append(objitem)

    def getTopics(self, save=True):
        url = f"/projects/{self.project_id}/topics"

        self.json_data = self.proofhubApi.get_data_array(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        dir = self.getFilePath( )
        self.saveJsonFile(dir, "topics.json", self.json_data)
        
        for topic in self.topics:
            topic.getTopicComments()

    def getSubPath(self) -> str:
        return f"projects/{self.project_id}/topics"

    def archive(self):
        ids = []
        for item in self.topics:
            ids.append(str(item.topic_id))
        
        self.archiveItems(ids)

#
# topic comment
#
class TopicComment(ProofHubObject):

    topic_id = None
    project_id = None
    sub_file_path = ""

    def __init__(self, proofhubApi: ProofhubApi, project_id, topic_id, sub_file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.sub_file_path = sub_file_path
        self.topic_id = topic_id
        self.project_id = project_id

#
# topic comments collection
#
class TopicComments(ProofHubObject):
    
    topic_id = None
    project_id = None
    sub_file_path = ""
    topiccom = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, topic_id, sub_file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.topic_id = topic_id
        self.project_id = project_id
        self.sub_file_path = sub_file_path
        
    def parseJsonResponse(self):
        dir = self.getSubPath( )

        if self.topiccom:
            self.topiccom.clear()
        else:
            self.topiccom = []
            
        for jsonitem in self.json_data:
            if not jsonitem["comments"]:
                continue
            
            comments = jsonitem["comments"]
            for comment in comments:
                objitem = TopicComment(self.proofhubApi, self.project_id, self.topic_id, dir, comment)
                self.topiccom.append(objitem)

    def getTopicComments(self, save=True):
        url = f"/projects/{self.project_id}/topics/{self.topic_id}/comments"

        self.json_data = self.proofhubApi.get_data_array(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()
        
        self.archive()

    def saveJson(self):
        self.saveJsonFile(self.getFilePath( ), "comments.json", self.json_data)

    def getSubPath(self) -> str:
        return f"{self.sub_file_path}/"

    def archive(self):
        return
        #ids = []
        #for item in self.topiccom:
        #    ids.append(str(item.topic_id))
        #
        #self.archive(ids)