from psd_tools import PSDImage
import pyperclip as pc
from config import scheme, psd_location
psd = PSDImage.open(psd_location)
from modules.parse import getCSS

result = getCSS(psd, scheme)
print(result)
# copy the resulting css to clipboard
pc.copy(result)
