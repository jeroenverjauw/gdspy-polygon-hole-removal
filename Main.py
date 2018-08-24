import gdspy
import tkinter as tk
from tkinter import filedialog

gdsii = gdspy.GdsLibrary()
gdspy.current_library = gdsii

gdsii.read_gds("C:/Users/jeroenverjauw/Desktop/SWMAJ-MEC_HFSS_design.gds")


def invert_layer(cell,lyr):

    mask = []
    polygons = cell.get_polygons(by_spec=True)[lyr]
    box_coord = cell.get_bounding_box()
    bbox = gdspy.Rectangle(box_coord[0],box_coord[1])

    for p in polygons:
        mask.append(gdspy.Polygon(p))
    cell.remove_polygons(lambda pts, layer, datatype:layer == lyr[0])
    result = ((gdspy.fast_boolean(bbox, mask, 'not',layer=lyr[0])))
    return result

    # return gdspy.Polygon(result.polygons)




def tessellate(cell, lyr=None):
    """
    within a cell, an old layer is subtracted from the chip size, and is written to the new layer

    Args:
        cell - gdspy cell
        lyr - layer name

    Return:
        cell with inverted new layer and removed old layer
    """

    mask = []
    if lyr is None:
        layers = cell.get_polygons(by_spec = True)
        for l in layers:
            tessellate(cell,l)
        return None

    polygons = cell.get_polygons(by_spec=True)[lyr]
    box_coord = cell.get_bounding_box()
    bbox = gdspy.Rectangle(box_coord[0],box_coord[1])

    for p in polygons:
        mask.append(gdspy.Polygon(p))

    cell.remove_polygons(lambda pts, layer, datatype:layer == lyr[0])
    result = gdspy.fast_boolean(bbox, mask, 'and', max_points=5, layer=lyr[0])
    cell.add(result)



for topcell in gdsii.top_level():
    # tessellate(topcell)
    box_coord = topcell.get_bounding_box()
    layers = topcell.get_polygons(by_spec = True)
    for l in layers:
        inv = invert_layer(topcell,l)
        if (inv) is not None:
            # print(box_coord[0][0],box_coord[1])
            bbox = []
            for p in inv.polygons:
                bbox.append(gdspy.Polygon(p).get_bounding_box())
            # 1 coordinaat moet op de rand liggen
            if any((coord[0][0] > box_coord[0][0] and coord[0][1] >  box_coord[0][1]) and (coord[1][0] < box_coord[1][0] and coord[1][1] <  box_coord[1][1]) for coord in bbox):
                  print(l)
            # else we need to test a few other things!



    gdspy.write_gds('test2.gds')
    gdspy.LayoutViewer(cells = topcell, depth=len(topcell.get_dependencies(recursive = True)))

