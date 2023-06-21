from psd_tools import PSDImage
import os
def getCSS(psd, config):
    css = ""
    for group in psd:
        css += ".b" + group.name + " {"
        print(group.kind)
        if(group.kind == 'smartobject'):
            print("smartobject layer. opening...")
            group.smart_object.save('temp')
            group = PSDImage.open("temp")
        for [psd_name, selector] in config:
            css += getElementCSS(psd_name, selector, group)
        if os.path.exists("temp"):
            os.remove("temp") # Delete file
        css += "\n}\n\n"
    return css

def getElementCSS(psd_name, selector, parent):
    style = ""
    if listMatches(parent, psd_name):
        print(psd_name)
        match = listMatches(parent, psd_name)[0]
        style += "\n" + selector + " {\n"\
            + f'left: {match.offset[0] - parent.offset[0]}px;\n'\
            + f'top: {match.offset[1] - parent.offset[1]}px;\n'\
            + f'width: {match.width}px;\n'\
            + f'height: {match.height}px\n'\
            + "}"
    return style

def listMatches(artboard,name):
    matches = [];
    find(artboard, name, matches)
    return matches

def find(artboard, name, result_list):

    try:
        for layer in artboard:
            print(layer)
            if layer.name == name:
                result_list.append(layer)
            find(layer, name, result_list)
    except TypeError:
        return
