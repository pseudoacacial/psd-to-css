from psd_tools import PSDImage
psd = PSDImage.open('test/video-parallel-banner_set.psd')
# psd.composite().save('video-parallel-banner_set.png')
from modules.parse import getCSS
import nested_config
print(len(nested_config.scheme['.logo']['children']))

def config():
    pairs = []
    f = open('config', 'r')
    for x in f:
        pairs.append([word.rstrip() for word in x.split(" ")])
    f.close()
    return pairs


print(getCSS(psd, config()))
