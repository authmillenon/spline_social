from ConfigParser import ConfigParser
import re

DEFAULTS = {
        'IRC': {
            'port': 6667,
        },
        'Bot': {
            'bot_nick': 'spline_social',
            'since_id': '',
        },
        'Database': {
            'username': None,
            'password': None,
        },
        'Identi.ca': {
            'since_id': 0
        }
    }

class OptionMissing(AttributeError):
    pass

class _Section:
    def __init__(self,name,items,config):
        self.__dict__['name'] = name
        self.__dict__['options'] = dict(items)
        self.__dict__['config'] = config
    
    def __getattr__(self,attr):
        if self.has_option(attr):
            if re.match('^[0-9]+$',self.options[attr]):
                return int(self.options[attr])
            else:
                return self.options[attr]
        else:
            if self.name in DEFAULTS.keys():
                if attr in DEFAULTS[self.name].keys():
                    return DEFAULTS[self.name][attr]
            raise OptionMissing("There is no option '%s' in section '%s'" % (attr, self.name))
    
    def __setattr__(self,attr,value):
        self.options[attr] = value
        file = open(self.config.filename, 'w')
        self.config.config.write(file)
        file.close()
    
    def has_option(self,attr):
        return attr in self.options.keys()

class Config(object):
    def __new__(type, *args, **kwargs):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance
    
    def __init__(self, filename = None):
        if filename != None:
            self.filename = filename
            self.config = ConfigParser()
            self.config.read([self.filename])
    
    def get_section(self,name):
        if self.config.has_section(name):
            return _Section(name, self.config.items(name), self)
        else:
            return None
    
    def __getattr__(self, attr):
        if attr == 'irc':
            return self.get_section('IRC')
        elif attr == 'bot':
            return self.get_section('Bot')
        elif attr == 'db':
            return self.get_section('Database')
        elif attr == 'identica':
            return self.get_section('Identi.ca')
