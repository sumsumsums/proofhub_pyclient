
from datetime import date

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

config.logger.info("----------------------")
today = f"Starting program - date: {date.today()}"
config.logger.info(today)

# TODO
# Files: falls nicht full_image gegeben, über download versuchen?
#

ph = ProofhubApi(config=config)

if config.get_groups:
    config.logger.info("Getting groups")
    groups = Groups(proofhubApi=ph)
    groups.getGroups()

if config.get_people:
    config.logger.info("Getting people")
    people = Peoples(proofhubApi=ph)
    people.getPeoples()

if config.get_roles:
    config.logger.info("Getting roles")
    roles = Roles(proofhubApi=ph)
    roles.getRoles()
    
if config.get_category:
    config.logger.info("Getting categories")
    categories = Categories(proofhubApi=ph)
    categories.getCategories()

if config.get_announcement:
    config.logger.info("Getting announcements")
    announcements = Announcements(proofhubApi=ph)
    announcements.getAnnouncements()

if config.get_projects:
    config.logger.info("Getting projects")
    projects = Projects(proofhubApi=ph)
    projects.getProjects()

today = f"Finished program - date: {date.today()}"
config.logger.info(today)
config.logger.info("----------------------")

