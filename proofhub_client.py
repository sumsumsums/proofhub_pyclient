"""
Backup Client for ProofHub using ProofHub API
API: https://github.com/ProofHub/api_v3

TODO
Files: falls nicht full_image gegeben, über download versuchen?
"""

from datetime import date

from config import Config
from proofhub_api import ProofhubApi
from announcement import Announcements
from people import Peoples
from category import Categories
from role import Roles
from group import Groups
from project import Projects
from all_tasks import AllTasks
from all_lists import AllLists

config = Config()
config.parseInput()

config.logger.info("----------------------")
today = f"Starting program - date: {date.today()}"
config.logger.info(today)

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

if config.get_all_tasks:
    config.logger.info("Getting all tasks")
    all_tasks = AllTasks(proofhubApi=ph)
    all_tasks.getAllTasks()

if config.get_all_lists:
    config.logger.info("Getting all lists")
    all_lists = AllLists(proofhubApi=ph)
    all_lists.getAllLists()

today = f"Finished program - date: {date.today()}"
config.logger.info(today)
config.logger.info("----------------------")

