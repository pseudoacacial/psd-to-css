from psd_tools import PSDImage
from psd_tools.constants import Tag
import os
import re

# TODO
#
# allow a list of psd names for one selector - merge and give position
# of merged
#
# find out why converting to jpg eats the quality a lot
# 
# Nesting!!
#
# store a list of processed groups + selectors and don't write new css if it has
# been written earlier (for example when there are two "300x600" groups, then
# only store new element the second time). maybe: create a tree at the start of
# getCSS, add to it/overwrite, and only convert the tree to CSS at the end

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
            if(element.get('match') == None):
                element['match'] = 0
            match = findElement(element['name'], group, element['match'])
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
                        image = match.composite(viewport, layer_filter= lambda x: True, color=(1.,1.,1.)).convert('RGB')
                    else:
                        image = match.composite(viewport, layer_filter= lambda x: True)
                    image.save('images/'\
                        + filename.replace('.', '')\
                        + '_' + name\
                        + '.' + element['export']['extension'],\
                        quality=100\
                        )
        if os.path.exists("temp"):
            os.remove("temp")
        css += "\n}\n\n"
    return css

def findElement(psd_name, parent, match):
    matches = listMatches(parent, psd_name)
    if matches:
        if(len(matches) > match):
            return matches[match]
        else:
            return matches[0]
    else:
        return False

def getElementCSS(element, frame, config):
    selector = config.get('selector')
    text = config.get('text')
    position = config.get('position')
    style = ""
    if(position or text):
        if selector:
            style += "\n" + selector + " {\n"
            if position:
            # basic position
                style += f'left: {element.offset[0] - frame.offset[0]}px;\n'\
                + f'top: {element.offset[1] - frame.offset[1]}px;\n'\
                + f'width: {element.width}px;\n'\
                + f'height: {element.height}px;\n'
            # border radius, if available
            if(element.kind == 'shape' and element.origination[0].origin_type == 2):
                radii = element.origination[0].radii
                style += f'border-radius: {radii["topLeft"]}px {radii["topRight"]}px {radii["bottomLeft"]}px { radii["bottomRight"]}px;\n'
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
    find(artboard, name, artboard.name, matches)
    return matches

def find(artboard, name, element_path, result_list):

    try:
        for layer in artboard:
            current_element_path = element_path + ">" + layer.name
            # search only layer name first(so regex elements like "^" and "$" work)
            match = re.search(name, layer.name)
            if match:
                result_list.append(layer)
            # search whole path next(joined by ">" character)
            else:
                match = re.search(name, current_element_path)
                if match:
                    result_list.append(layer)
            find(layer, name, current_element_path, result_list)
    except TypeError:
        return
