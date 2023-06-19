def getCSS(psd, config):
    css = ""
    for artboard in psd:
        css += ".b" + artboard.name + " {"
        for [psd_name, selector] in config:
            css += getElementCSS(psd_name, selector, artboard)
        css += "\n}\n\n"
    return css

def getElementCSS(psd_name, selector, parent):
    if listMatches(parent, psd_name):
        style = "\n" + selector + " {\n"
        print(psd_name)
        match = listMatches(parent, psd_name)[0]
        style += f'left: {match.offset[0] - parent.offset[0]}px;\n'\
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
    print(artboard)
    print(name)
    try:
        for layer in artboard:
            if layer.name == name:
                result_list.append(layer)
            find(layer, name, result_list)
    except TypeError:
        return
