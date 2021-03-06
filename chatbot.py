import logging
import threading
import configparser
from Legobot.Lego import Lego
from Local.Roll import Roll
from Local.Msync import Audit

from Legobot.Connectors.IRC import IRC
from Legobot.Legos.Help import Help

config = configparser.ConfigParser()
config.read('config.ini')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)

# Initialize lock and baseplate
lock = threading.Lock()
baseplate = Lego.start(None, lock)
baseplate_proxy = baseplate.proxy()

# Add children
baseplate_proxy.add_child(IRC,
                          channels=['#voxpupuli'],
                          nickname=config['freenode']['username'],
                          server=config['freenode']['host'],
                          port=int(config['freenode']['port']),
                          use_ssl=config.getboolean('freenode','ssl'),
                          username=config['freenode']['username'],
                          password=config['freenode']['password'])
baseplate_proxy.add_child(Help)
baseplate_proxy.add_child(Roll)
baseplate_proxy.add_child(Audit)
