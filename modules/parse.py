from psd_tools import PSDImage
import os
import re

# TODO
#
# get font-size, border-radius for button
#
# find out why converting to jpg eats the quality a lot
# 
# Nesting!!
#
# store a list of processed groups + selectors and don't write new css if it has
# been written earlier (for example when there are two "300x600" groups, then
# only store new element the second time). maybe: create a tree at the start of
# getCSS, add to it/overwrite, and only convert the tree to CSS at the end

# def getCSS(psd, config):
#     css = ""
#     for group in psd:
#         css += ".b" + group.name + " {"
#         if(group.kind == 'smartobject'):
#             print("smartobject layer. opening...")
#             group.smart_object.save('temp')
#             group = PSDImage.open("temp")
#         for [psd_name, selector] in config:
#             css += getElementCSS(psd_name, selector, group)
#         if os.path.exists("temp"):
#             os.remove("temp") # Delete file
#         css += "\n}\n\n"
#     return css

def getCSS(psd, config):
    css = ""
    for group in psd:
        css += ".b" + group.name + " {"
        name = group.name
        if(group.kind == 'smartobject'):
            print("smartobject layer. opening...")
            group.smart_object.save('temp')
            group = PSDImage.open("temp")
        # process element
        for element in config:
            print(element)
            match = findElement(element['name'], group)
            if (match):
                if (element.get('selector')):
                    css += getElementCSS(match, element['selector'], group)
                if(element.get('export')):
                    print("has export value")
                    print(element['export'])
                    print(group)
                    filename = element['export'].get('name') if element['export'].get('name') else element['selector']
                    if (group.kind == 'smartobject'):
                        viewport = group.viewbox if element['export'].get('clip') else None
                    else: 
                        viewport = group.bbox if element['export'].get('clip') else None
                    # discard transparency if jpg
                    if (element['export']['extension'] == "jpg"):
                        image = match.composite(viewport).convert('RGB')
                    else:
                        image = match.composite(viewport)
                    image.save(\
                        filename.replace('.', '')\
                        + '_' + name\
                        + '.' + element['export']['extension']\
                        )
        if os.path.exists("temp"):
            os.remove("temp")
        css += "\n}\n\n"
    return css

def findElement(psd_name, parent):
    if listMatches(parent, psd_name):
        return listMatches(parent, psd_name)[0]
    else:
        return False

def getElementCSS(element, selector, parent):

    style = ""
    style += "\n" + selector + " {\n"\
    + f'left: {element.offset[0] - parent.offset[0]}px;\n'\
    + f'top: {element.offset[1] - parent.offset[1]}px;\n'\
    + f'width: {element.width}px;\n'\
    + f'height: {element.height}px\n'\
    + "}"
    return style

def listMatches(artboard,name):
    matches = [];
    find(artboard, name, matches)
    return matches

def find(artboard, name, result_list):

    try:
        for layer in artboard:
            match = re.search(name, layer.name)
            if match:
                result_list.append(layer)
            find(layer, name, result_list)
    except TypeError:
        return
