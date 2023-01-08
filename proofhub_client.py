
from config import Config
from proofhub_api import ProofhubApi
from announcement import Announcements
from people import Peoples
from category import Categories
from role import Roles
from group import Groups
from project import Projects

#
# API: https://github.com/ProofHub/api_v3
#

config = Config()
config.parseInput()


# TODO
# Files: falls nicht full_image gegeben, über download versuchen?

ph = ProofhubApi(config=config)

groups = Groups(proofhubApi=ph)
groups.getGroups()

people = Peoples(proofhubApi=ph)
people.getPeoples()

roles = Roles(proofhubApi=ph)
roles.getRoles()

categories = Categories(proofhubApi=ph)
categories.getCategories()

announcements = Announcements(proofhubApi=ph)
announcements.getAnnouncements()

projects = Projects(proofhubApi=ph)
projects.getProjects()

