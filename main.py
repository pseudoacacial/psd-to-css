from psd_tools import PSDImage
import pyperclip as pc
from config import scheme, prefix, psd_location
psd = PSDImage.open(psd_location)
from modules.parse import getCSS

result = getCSS(psd, scheme, prefix)
print(result)
# copy the resulting css to clipboard
pc.copy(result)
