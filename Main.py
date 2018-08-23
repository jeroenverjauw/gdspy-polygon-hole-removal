import gdspy
import tkinter as tk
from tkinter import filedialog

gdsii = gdspy.GdsLibrary()
gdspy.current_library = gdsii

gdsii.read_gds("")

def subtract_layer(cell, old_layer, new_layer, box, keep=False):
    """
    within a cell, an old layer is subtracted from the chip size, and is written to the new layer

    Args:
        cell - gdspy cell
        old_layer - old layer name
        new_layer - new layer name
        specs - dictionary with all parameters
        keep - (Default: False) keep neg layer

    Return:
        cell with inverted new layer and removed old layer
    """


    subtr = []
    chip = box
    layers = cell.get_polygons(by_spec=True)
    polygons = layers[old_layer]
    result = chip
    for p in polygons:
        result = gdspy.fast_boolean(result, gdspy.Polygon(p), 'and')


    cell.remove_polygons(lambda pts, layer, datatype: layer == int(old_layer[0])) if keep == False else None
    # result = gdspy.fast_boolean(chip, subtr, 'not', layer= int(specs[new_layer]))

    return result

def box(cell)
    areas = topcell.area(cell,by_spec = True)
    print(areas)

data = dict()


for topcell in gdsii.top_level():
    box = box(topcell)

    polygons = topcell.get_polygons(by_spec = True)

    print(box)
    for i in polygons:
#        print(i)
#        subtract_layer(topcell,i,i,box)

    gdspy.LayoutViewer(cells = topcell, depth=len(topcell.get_dependencies(recursive = True)))

