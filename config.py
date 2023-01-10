import configparser
import argparse
import logging
import logging.config

class Config(object):
    
    defaultSection = 'default'
    
    parser: argparse.ArgumentDefaultsHelpFormatter = None
    
    urlbase = ''
    headers = { }
    outputdir = ''
    api_key = None
    user_agent = None
    
    logger = None
    
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

    def initializeLogger(self, vars):
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        self.logger = logging.getLogger('proofhub_client')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)


