from psd_tools import PSDImage
import pyperclip as pc

from config import settings, scheme
from modules.parse import getCSS

#default values
if(settings.get('prefix') == None):
    settings['prefix'] = ""
if(settings.get('group_match') == None):
    settings['group_match'] = False
psd = PSDImage.open(settings['psd_location'])
prefix = settings['prefix']

result = getCSS(psd, scheme, settings)
print(result)
# copy the resulting css to clipboard
pc.copy(result)
