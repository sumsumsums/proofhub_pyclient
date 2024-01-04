"""
Configuration object parsing and holding all configuration stuff
"""

import configparser
import argparse
import logging
import logging.config

class Config(object):
    
    default_section = 'default'
    parser: argparse.ArgumentDefaultsHelpFormatter = None
    logger = None
    
    urlbase = ''
    headers = { }
    outputdir = ''
    api_key = None
    user_agent = None
    
    get_people = True
    get_groups = True
    get_category = True 
    get_announcement = True 
    get_roles = True 
    get_projects = True
    get_folders = True
    get_topics = True 
    get_notebooks = True
    get_tasklists = True
    
    files_download_browser = False 
    files_temporary_dir = ''
    get_comments = True
    get_all_tasks = True
    
    projects_whitelist = []

    archive_deprecated = False
    archive_dir = ''
    
    def __init__(self):
        self.parser = None

    def buildArgumentParser(self) -> argparse.ArgumentParser:
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-c', '--configfile', required=False, default='configuration.ini')

    def parseInput(self):
        self.buildArgumentParser()
        args = vars(self.parser.parse_args())
        
        self.initializeLogger(args)
        
        configfile = args['configfile']
        
        self.readConfig(configfile)

    def readConfig(self, configfile):
        config = configparser.ConfigParser()
        print(configfile)
        config.read(configfile)
        
        self.api_key = config.get(self.default_section, 'api_key')
        self.urlbase = config.get(self.default_section, 'proofhub_url')
        self.outputdir = config.get(self.default_section, 'output_directory')
        self.user_agent = config.get(self.default_section, 'user_agent')

        self.headers =  {
            'X-API-KEY': self.api_key,
            'User-Agent': self.user_agent,
        }
        
        self.files_download_browser = config.getboolean(self.default_section, 'files_download_browser', fallback=False)
        self.files_temporary_dir = config.get(self.default_section, 'files_temporary_dir')
        
        # objects to get
        self.get_announcement = config.getboolean(self.default_section, 'get_announcement', fallback=True)
        self.get_category = config.getboolean(self.default_section, 'get_category', fallback=True)
        self.get_people = config.getboolean(self.default_section, 'get_people', fallback=True)
        self.get_groups = config.getboolean(self.default_section, 'get_groups', fallback=True)
        self.get_roles = config.getboolean(self.default_section, 'get_roles', fallback=True)
        self.get_projects = config.getboolean(self.default_section, 'get_projects', fallback=True)
        self.get_folders = config.getboolean(self.default_section, 'get_folders', fallback=True)
        self.get_topics = config.getboolean(self.default_section, 'get_topics', fallback=True)
        self.get_notebooks = config.getboolean(self.default_section, 'get_notebooks', fallback=True)
        self.get_tasklists = config.getboolean(self.default_section, 'get_tasklists', fallback=True)
        self.get_comments = config.getboolean(self.default_section, 'get_comments', fallback=True)
        self.get_all_tasks = config.getboolean(self.default_section, 'get_all_tasks', fallback=True)
        self.get_all_lists = config.getboolean(self.default_section, 'get_all_lists', fallback=True)
        self.include_archived_todolists = config.getboolean(self.default_section, 'include_archived_todolists', fallback=False)

        self.projects_whitelist = []
        projects_whitelist = config.get(self.default_section, 'projects')
        if projects_whitelist and not projects_whitelist == "":
            self.projects_whitelist = projects_whitelist.split(',')

        self.list_ids = []
        list_ids = config.get(self.default_section, 'todolists', fallback=[])
        if list_ids and not list_ids == "":
            self.list_ids = list_ids.split(',')

        self.archive_deprecated = config.getboolean(self.default_section, 'archive_deprecated', fallback=False)
        self.archive_dir = config.get(self.default_section, 'archive_dir')

    def initializeLogger(self, vars):
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        self.logger = logging.getLogger('proofhub_client')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)


