from psd_tools import PSDImage
psd = PSDImage.open('video-parallel-banner_set.psd')
# psd.composite().save('video-parallel-banner_set.png')

def listMatches(artboard,name):
    matches = [];
    find(artboard, name, matches)
    return matches

def find(artboard, name, result_list):
    try:
        for layer in artboard:
            if layer.name == name:
                result_list.append(layer)
            find(layer, name, result_list)
    except TypeError:
        return

def getCSS(config):
    css = ""
    for artboard in psd:
        css += ".b" + artboard.name + " {"
        for [psd_name, selector] in config:
            if listMatches(artboard, psd_name):
                css += "\n" + selector + " {\n"
                print(psd_name)
                match = listMatches(artboard, psd_name)[0]
                css += f'left: {match.offset[0] - artboard.offset[0]}px;\n'\
                + f'top: {match.offset[1] - artboard.offset[1]}px;\n'\
                + f'width: {match.width}px;\n'\
                + f'height: {match.height}px\n'\
                + "}"
        css += "\n}\n\n"
    return css
        # for layer in flatten(artboard):
        #     if layer.name =="video":
        #         print(layer)
        #         print(layer.parent.offset)
        #         print(layer.offset)
            # layer_image = layer.composite()
            # layer_image.save('%s.png' % layer.name)

def config():
    pairs = []
    f = open('config', 'r')
    for x in f:
        pairs.append([word.rstrip() for word in x.split(" ")])
    f.close()
    return pairs

print(getCSS(config()))
