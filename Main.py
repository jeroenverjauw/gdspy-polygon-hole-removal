import gdspy
import tkinter as tk
from tkinter import filedialog

gdsii = gdspy.GdsLibrary()
gdspy.current_library = gdsii

gdsii.read_gds("C:/Users/jeroenverjauw/Desktop/SWMAJ-MEC_HFSS_design.gds")


def invert_layer(cell,lyr,keep = False):

    mask = []
    polygons = cell.get_polygons(by_spec=True)[lyr]
    box_coord = cell.get_bounding_box()
    bbox = gdspy.Rectangle(box_coord[0],box_coord[1])

    for p in polygons:
        mask.append(gdspy.Polygon(p))
    cell.remove_polygons(lambda pts, layer, datatype:layer == lyr[0]) if keep is False else None
    result = gdspy.fast_boolean(bbox, mask, 'not',layer=lyr[0])
    return result

def hole(cell,lyr):



    inv = invert_layer(topcell,lyr,keep = True)
    box_coord = cell.get_bounding_box()
    if inv is not None:
        bbox = []
        holes = []
        # [holes.append(p) for p in inv.polygons]
        [bbox.append(gdspy.Polygon(p).get_bounding_box()) for p in inv.polygons]
        # print('number of bboxes: {0}'.format(len(bbox)))
        # print('number of holes: {0}'.format(len(holes)))
        # # 1 coordinaat moet op de rand liggen
        # if any((coord[0][0] > box_coord[0][0] and coord[0][1] >  box_coord[0][1]) and (coord[1][0] < box_coord[1][0] and coord[1][1] <  box_coord[1][1]) for coord in bbox):
        #     print(lyr)
        #     # there are holes inside, check if already something has been subdivided!
        result = False
        for p in cell.get_polygons(by_spec = True)[lyr]:
            box_coord = gdspy.Polygon(p).get_bounding_box()
            p_holes = any([any((h[0][0] > box_coord[0][0] and h[0][1] >  box_coord[0][1]) and (h[1][0] < box_coord[1][0] and h[1][1] < box_coord[1][1]) for h in bbox)])
            # print(p_holes)
            result = (result or p_holes)
                # print(result)
                # gdspy.LayoutViewer()
                # if not all(all(gdspy.inside(h,gdspy.Polygon(p))) for h in holes):
                #     print('succes')
                #
                #     return False
            # gdspy.LayoutViewer()
        return result
    return False

def tessellate(cell,i=199, lyr=None):
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
            i = 199
            while  hole(cell,l):
                tessellate(cell,i,l)
                i=i-1
        return None

    polygons = cell.get_polygons(by_spec=True)[lyr]
    box_coord = cell.get_bounding_box()
    bbox = gdspy.Rectangle(box_coord[0],box_coord[1])

    for p in polygons:
        mask.append(gdspy.Polygon(p))

    cell.remove_polygons(lambda pts, layer, datatype:layer == lyr[0])
    result = gdspy.fast_boolean(bbox, mask, 'and', max_points=i, layer=lyr[0])
    # print(len(result.polygons))
    cell.add(result)



for topcell in gdsii.top_level():
    layers = topcell.get_polygons(by_spec = True)
    for l in layers:
        if hole(topcell,l):
            tessellate(topcell,l)


    gdspy.write_gds('test2.gds')
    gdspy.LayoutViewer(cells = topcell, depth=len(topcell.get_dependencies(recursive = True)))

