from psd_tools import PSDImage
# psd = PSDImage.open('test/video-parallel-banner_set.psd')
psd = PSDImage.open('test/smart_objects.psd')
# psd.composite().save('video-parallel-banner_set.png')
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
# nested_config()
print(getCSS(psd, nested_config()))
# print(getCSS(psd, config()))
