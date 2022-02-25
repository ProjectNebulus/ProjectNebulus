import os
import certifi
from mongoengine import connect

from .create import *
from .delete import *
from .read import *
from .update import *

ca = certifi.where()
db = connect(db='Nebulus', username='MainUser', password=os.environ.get('MONGOPASS'), host=os.environ.get('MONGO'),
             tlsCAFile=ca)
