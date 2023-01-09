import configparser
import argparse

class Config(object):
    
    defaultSection = 'default'
    
    parser: argparse.ArgumentDefaultsHelpFormatter = None
    
    urlbase = ''
    headers = { }
    outputdir = ''
    api_key = None
    user_agent = None
    
    def __init__(self):
        self.parser = None

    def buildArgumentParser(self) -> argparse.ArgumentParser:
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-c', '--configfile', required=False, default='configuration.ini')

    def parseInput(self):
        self.buildArgumentParser()
        args = vars(self.parser.parse_args())
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


