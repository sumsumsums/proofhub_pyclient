from proofhub_api import ProofhubApi
from proofhubobject import ProofHubObject

# topics and topic comments
#
# Endpoint GET
# GET v3/projects/<project_id>/topics

#
# single topic
#
class Topic(ProofHubObject):

    root_file_path = ""
    topic_id = None
    project_id = None

    def __init__(self, proofhubApi: ProofhubApi, project_id, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.project_id = project_id
        self.setTopicId()

    def setTopicId(self):
        self.topic_id = self.json_data["id"]
    
    def getFilePath(self) -> str:
        return f"{self.root_file_path}/{self.topic_id}"
    
    def getTopicComments(self):
        comments = TopicComments(self.proofhubApi, self.project_id, self.topic_id, self.getFilePath())
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
        dir = self.getFilePath( )
        
        if self.topics:
            self.topics.clear()
        else:
            self.topics = []
        
        for jsonitem in self.json_data:
            objitem = Topic(self.proofhubApi, self.project_id, dir, jsonitem)
            self.topics.append(objitem)

    def getTopics(self, save=True):
        url = f"/projects/{self.project_id}/topics"

        self.json_data = self.proofhubApi.get_data_string(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def saveJson(self):
        dir = self.getFilePath( )
        self.saveJsonFile(dir, "topics.json", self.json_data)
        
        for topic in self.topics:
            topic.getTopicComments()
    
    def getFilePath(self) -> str:
        return f"{self.proofhubApi.outputdir}/projects/{self.project_id}/topics"

#
# topic comment
#
class TopicComment(ProofHubObject):

    topic_id = None
    project_id = None
    root_file_path = ""

    def __init__(self, proofhubApi: ProofhubApi, project_id, topic_id, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.root_file_path = file_path
        self.topic_id = topic_id
        self.project_id = project_id

#
# topic comments collection
#
class TopicComments(ProofHubObject):
    
    topic_id = None
    project_id = None
    root_file_path = ""
    topiccom = []
    
    def __init__(self, proofhubApi: ProofhubApi, project_id, topic_id, file_path, json_data=""):
        super().__init__(json_data, proofhubApi)
        self.topic_id = topic_id
        self.project_id = project_id
        self.root_file_path = file_path
        
    def parseJsonResponse(self):
        dir = self.getFilePath( )
    
        comments = self.json_data["comments"]

        if self.topiccom:
            self.topiccom.clear()
        else:
            self.topiccom = []
            
        for jsonitem in comments:
            objitem = TopicComment(self.proofhubApi, self.project_id, self.topic_id, dir, jsonitem)
            self.topiccom.append(objitem)

    def getTopicComments(self, save=True):
        url = f"/projects/{self.project_id}/topics/{self.topic_id}/comments"

        self.json_data = self.proofhubApi.get_data_string(url)
        self.parseJsonResponse()
        if save == True:
            self.saveJson()

    def saveJson(self):
        self.saveJsonFile(self.getFilePath( ), "comments.json", self.json_data)
    
    def getFilePath(self) -> str:
        return f"{self.root_file_path}/"