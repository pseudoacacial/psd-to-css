from psd_tools import PSDImage
import pyperclip as pc
# psd = PSDImage.open('test/video-parallel-banner_set.psd')
# psd = PSDImage.open('test/smart_objects.psd')
from nested_config import scheme, psd_location
psd = PSDImage.open(psd_location)
from modules.parse import getCSS

def config():
    pairs = []
    f = open('config', 'r')
    for x in f:
        pairs.append([word.strip() for word in x.split(",")])
    f.close()
    return pairs

def nested_config():
    from nested_config import scheme
    return scheme
result = getCSS(psd, nested_config())
print(result)
# copy the resulting css to clipboard
pc.copy(result)
# print(getCSS(psd, config()))
