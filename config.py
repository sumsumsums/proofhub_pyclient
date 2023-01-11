import configparser
import argparse
import logging
import logging.config

class Config(object):
    
    defaultSection = 'default'
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
        config.read(configfile)
        
        self.api_key = config.get(self.defaultSection, 'api_key')
        self.urlbase = config.get(self.defaultSection, 'proofhub_url')
        self.outputdir = config.get(self.defaultSection, 'output_directory')
        self.user_agent = config.get(self.defaultSection, 'user_agent')

        self.headers =  {
            'X-API-KEY': self.api_key,
            'User-Agent': self.user_agent,
        }
        
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

    def initializeLogger(self, vars):
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        self.logger = logging.getLogger('proofhub_client')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)


