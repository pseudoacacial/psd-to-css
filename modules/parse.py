from psd_tools import PSDImage
from psd_tools.constants import Tag
import os
import re

# TODO
#
# border-radius for button
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
            group.smart_object.save('temp')
            group = PSDImage.open("temp")
        # process element
        for element in config:
            #default values
            if(element.get('position') == None):
                element['position'] = True
            match = findElement(element['name'], group)
            if (match):
                # add to css
                if (element.get('selector')):
                    css += getElementCSS(match, group, element)

                # export
                if(element.get('export')):
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

def getElementCSS(element, parent, config):
    selector = config.get('selector')
    text = config.get('text')
    position = config.get('position')
    style = ""
    if(position or text):
        if selector:
            style += "\n" + selector + " {\n"
            if position:
                style += f'left: {element.offset[0] - parent.offset[0]}px;\n'\
                + f'top: {element.offset[1] - parent.offset[1]}px;\n'\
                + f'width: {element.width}px;\n'\
                + f'height: {element.height}px;\n'
            # font-size, from this layer or from child layers, if "text" option set
            font_size =""
            if(text):
                if element.kind == 'type':
                    style += f'font-size: {getFontSize(element)}px;\n'
                else:
                    for child in element.descendants():
                        if child.kind == 'type':
                            style += f'font-size: {getFontSize(child)}px;\n'
                            break
            style += "}"
    return style

def getFontSize(element):
    runlength = element.engine_dict['StyleRun']['RunLengthArray']
    rundata= element.engine_dict['StyleRun']['RunArray']
    text = element.engine_dict['Editor']['Text'].value
    for length, data in zip(runlength, rundata):
        stylesheet = data['StyleSheet']['StyleSheetData']
        font_size = str(round(stylesheet['FontSize'] * element.transform[0], 2))
    return font_size


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
