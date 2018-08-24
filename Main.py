import gdspy
import tkinter as tk
from tkinter import filedialog

gdsii = gdspy.GdsLibrary()
gdspy.current_library = gdsii

gdsii.read_gds("C:/Users/jeroen verjauw/Desktop/SWMAJ-MEC_HFSS_design.gds")

def tessellate(cell, lyr):
    """
    within a cell, an old layer is subtracted from the chip size, and is written to the new layer

    Args:
        cell - gdspy cell
        lyr - layer name

    Return:
        cell with inverted new layer and removed old layer
    """

    mask = []
    polygons = cell.get_polygons(by_spec=True)[lyr]
    box_coord = topcell.get_bounding_box()
    bbox = gdspy.Rectangle(box_coord[0],box_coord[1])

    for p in polygons:
        mask.append(gdspy.Polygon(p))

    cell.remove_polygons(lambda pts, layer, datatype:layer == lyr[0])
    result = gdspy.fast_boolean(bbox, mask, 'and', max_points=5, layer=lyr[0])
    cell.add(result)

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
    layers = topcell.get_polygons(by_spec = True)
    for l in layers:
        print(l)
        tessellate(topcell,l)

    gdspy.write_gds('test2.gds')
    gdspy.LayoutViewer(cells = topcell, depth=len(topcell.get_dependencies(recursive = True)))

