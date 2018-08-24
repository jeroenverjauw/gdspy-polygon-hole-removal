import gdspy
import tkinter as tk
from tkinter import filedialog

gdsii = gdspy.GdsLibrary()
gdspy.current_library = gdsii

gdsii.read_gds("C:/Users/jeroenverjauw/Desktop/SWMAJ-MEC_HFSS_design.gds")

def tessellate(cell, old_layer, new_layer, boxlayer, keep=False):
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

    mask = []
    layers = cell.get_polygons(by_spec=True)
    print(layers)
    polygons = layers[old_layer]
    # print(layers.keys())
    box = boxlayer
    result = boxlayer
    print(old_layer)
    print(len(polygons))

    for p in polygons:
        mask.append(gdspy.Polygon(p))

    cell.remove_polygons(lambda pts, layer, datatype:layer == old_layer[0])
    result = gdspy.fast_boolean(box, mask, 'and', max_points=5, layer=old_layer[0])
    # for p in polygons:
    #     result = gdspy.fast_boolean(result, gdspy.Polygon(p), 'and',max_points=5,layer = old_layer[0])
    # #
    # cell.remove_polygons(lambda pts, layer, datatype:layer == old_layer[0])
    # # cell.remove_polygons(lambda pts, layer, datatype: layer == int(old_layer[0])) if keep == False else None

    cell.add(result)
    # return (result)

def box(cell):
    """
    within a cell, the largest area layer is found and it is checked if it has only one polygon

    Args:
        cell - gdspy cell

    Return:
        largest polygon
    """

    areas = cell.area(by_spec = True)
    polygons = cell.get_polygons(by_spec=True)

    max_val = (max(areas.values()))
    max_keys = ([key for key in areas.keys() if areas[key]==max_val])
    # check if biggest value is only one polygon
    for k in max_keys:
        if len(polygons[k]) == 1:
            return polygons[k]
    print('bounding box is not defined properly: a single rectangle is required')
    return None


for topcell in gdsii.top_level():
    box = box(topcell)
    box = topcell.get_bounding_box()
    print(box)
    polygons = topcell.get_polygons(by_spec = True)
    for i in polygons:
        print(i)
        tessellate(topcell,i,i,box)

    gdspy.write_gds('test2.gds')
    gdspy.LayoutViewer(cells = topcell, depth=len(topcell.get_dependencies(recursive = True)))

