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

def getCSS(psd, config, settings):
    processedSelectors = {}
    ### save styles in a dictionary
    for group in psd:
        name=group.name
        # ignore groups which names don't match the specified group_match
        if(settings['group_match']):
            matchedName = re.search(settings['group_match'], group.name)
            if (not matchedName):
                continue
            name = matchedName[0]
        # add the group to list of processedSelectors, if it's the first time processing this group
        if(processedSelectors.get(name) == None):
            processedSelectors[name] = {} 
        # handle smartobject
        wasSmartObject = False
        if(group.kind == 'smartobject'):
            group.smart_object.save('temp')
            group = PSDImage.open("temp")
            wasSmartObject = True
        # process element
        for element in config:
            #default values
            if(element.get('position') == None):
                element['position'] = True
            if(element.get('size') == None):
                element['size'] = True
            if(element.get('match') == None):
                element['match'] = 0
            if(element.get('frameMatch') == None):
                element['frameMatch'] = 0
            match = findElement(element['name'], group, element['match'])
            if (match):
                # add to css, if the selector hasn't already been processed 
                if (element.get('selector')):
                    if (processedSelectors[name].get('selector') == None):
                        dictionary = {element["selector"]:None}
                        processedSelectors[name][element["selector"]] = None
                        if (element.get('frame')):
                            frame = findElement(element['frame'], group, element['frameMatch'])
                        else:
                            frame = group
                        if(not type(frame) is bool):
                            processedSelectors[name][element["selector"]] = getElementCSS(match, frame, element)

                # export
                if(element.get('export')):
                    filename = element['export'].get('name') if element['export'].get('name') else element['selector']
                    if (wasSmartObject):
                        viewport = group.viewbox if element['export'].get('clip') else None
                    else:
                        viewport = group.bbox if element['export'].get('clip') else None
                    # discard transparency if jpg
                    if (element['export']['extension'] == "jpg"):
                        image = match.composite(viewport, layer_filter= lambda x: True, color=(1.,1.,1.)).convert('RGB')
                    else:
                        image = match.composite(viewport, layer_filter= lambda x: True)
                    if not os.path.exists('exported_images/'):
                        os.mkdir('exported_images/')
                    image.save('exported_images/'\
                        + filename.replace('.', '')\
                        + '_' + name\
                        + '.' + element['export']['extension'],\
                        quality=100\
                        )
        if os.path.exists("temp"):
            os.remove("temp")

    ### convert the dictionary to text
    css = "" 
    for group in processedSelectors:
        css += settings['prefix'] + group + settings['suffix'] + " {\n"
        for element in processedSelectors[group]:
            if(processedSelectors[group][element]):
                css += element + " {\n" + processedSelectors[group][element] + "}\n"
        css += "}\n\n"
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

def findDescendantOfType(element, type):
    if element.kind == type:
        return element
    if element.kind == 'group':
        for child in element.descendants():
            if child.kind == type:
                return child
    return False

def getElementCSS(element, frame, config):
    selector = config.get('selector')
    style = ""
    if selector:
        if config.get('position'):
        # basic position
            style += f'left: {element.offset[0] - frame.offset[0]}px;\n'\
            + f'top: {element.offset[1] - frame.offset[1]}px;\n'
        if config.get('size'):
        # size
            style += f'width: {element.width}px;\n'\
            + f'height: {element.height}px;\n'
        # # rotation 
        # if hasattr(element, 'warp'):
        #     style += f'TRANSFORM HERE ~~~~~~~~~~~~~~~~~~~~~~~'
        #     style += f'{element.warp}'\
        # border radius, if wanted 
        if(config.get('border')):
            elementWithBorder = findDescendantOfType(element, 'shape') if findDescendantOfType(element, 'shape') else element

            if(elementWithBorder.kind == 'shape' and elementWithBorder.origination[0].origin_type == 2):
                radii = elementWithBorder.origination[0].radii
                style += f'border-radius: {round(float(radii["topLeft"]), 2)}px {round(float(radii["topRight"]), 2)}px {round(float(radii["bottomLeft"]), 2)}px {round(float(radii["bottomRight"]), 2)}px;\n'
        # font-size, from this layer or from child layers, if "text" option set
        font_size =""
        if(config.get('text')):
            elementWithText = findDescendantOfType(element, 'type') if findDescendantOfType(element, 'type') else element
        else:
            elementWithText = element
        if elementWithText.kind == 'type' and not config.get('text')==False:
            style += f'font-size: {getFontSize(elementWithText)}px;\n'
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
    return list(filter(lambda n: n.width>0,matches))

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
