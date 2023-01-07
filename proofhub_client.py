import requests
import json

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
#

urlbase='https://aaverify.proofhub.com/api/v3/'
apikey='4c58546494ba3ee4436696c701d45e7a02a944c2'
useragent='ProofClient (proofhub-client@fmey.org)'
rootdirectory="C:/Users/frank/99_tmp/proofhub"

# TODO
# Folders recursive auflösen
# Task comments GET v3/projects/23423233/todolists/13964085/tasks/13966758/comments

# Fehler abfangen: {'status': False, 'error': 'Rate limit exceeded. Try after 10 seconds'}

# Not: Timesheets, Time, Quickies, Request forms, Everything

ph = ProofhubApi(urlbase=urlbase, api_key=apikey, user_agent=useragent, outputdir=rootdirectory)

#groups = Groups(proofhubApi=ph)
#groups.getGroups()

#people = Peoples(proofhubApi=ph)
#people.getPeoples()

#roles = Roles(proofhubApi=ph)
#roles.getRoles()

projects = Projects(proofhubApi=ph)
projects.getProjects()

#categories = Categories(proofhubApi=ph)
#categories.getCategories()

#announcements = Announcements(proofhubApi=ph)
#announcements.getAnnouncements()
