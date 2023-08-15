# psd-to-css
psd to css

### installation
`git clone https://github.com/pseudoacacial/psd-to-css.git`
`cd psd-to-css`
`python -m venv ./`

`source bin/activate` OR `source bin/activate.fish`

`pip install psd-tools`
`pip install pyperclip`

`python main.py`

### usage
`source bin/activate` OR `source bin/activate.fish`

`python main.py`

### result
- a bunch of .scss, printed in the console and copied to clipboard
- images in the folder "exported_images"

### how does it work
it takes a config file (config.py). Inside it there's a path to the .psd file that we want parsed. There's also a 'scheme' - an array containing information about which layers from photoshop are of interest.
The script produces an .scss stylesheet, which describes each layer of interest, inside each of the top artboards or smart objects.

### config
Each config scheme entry can have possible values:

- 'selector' (string or False) - under what css selector will the css be exported. E.g. ".logo"
- 'name' (string, mandatory) - the name of the photoshop layer that we want exported. Uses regex. examples:
    - `^cta` - layer with the name starting with "cta"
    - `Group 1>Rectangle` - layer with the name starting with "Rectangle", immediate child of the layer with the name ending with "Group 1"
- 'frame' (string) - another layer name, relative to which the positions will be provided. By default, the positions are provided relative to the top artboard or smart object
- 'text' (boolean) - whether to look for the text in the elements descendants. Even if false, 'font-size' will be exported, if the element is a text element. If true, the script will look for a text element in descendants of the provided element.
- 'border' (boolean) - whether to look for shape in the element descendats (for border-radius). same as above, if the element is a rounded rectangle, border-radius will be exported even if this value is false.
- 'export' (dictionary)
    - 'extension' (string) - extension under which to save the exported file
    - 'name' (string) - name of the exported file. It will be followed by the top artboard/smart object name. For example, name 'bg' results in files "bg_300x600.jpg", "bg_300x250.jpg", ...
    - 'clip' (boolean) - whether to clip to the frame (top artboard / smart object by default). Leave False for Key Visuals, turn True for backgrounds/overlays.
- 'match' (number) - if 'name' matches more than one element, this allows to use a different one
