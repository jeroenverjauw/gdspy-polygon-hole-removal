import gdspy
import tkinter as tk
from tkinter import filedialog

gdsii = gdspy.GdsLibrary()
gdspy.current_library = gdsii

gdsii.read_gds("C:/Users/jeroen verjauw/Desktop/SWMAJ-MEC_HFSS_design.gds")

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
        layers = topcell.get_polygons(by_spec = True)
        for l in layers:
            print('test:{}'.format(l))
            tessellate(topcell,l)
        return None

    polygons = cell.get_polygons(by_spec=True)[lyr]
    box_coord = topcell.get_bounding_box()
    bbox = gdspy.Rectangle(box_coord[0],box_coord[1])

    for p in polygons:
        mask.append(gdspy.Polygon(p))

    cell.remove_polygons(lambda pts, layer, datatype:layer == lyr[0])
    result = gdspy.fast_boolean(bbox, mask, 'and', max_points=5, layer=lyr[0])
    cell.add(result)



for topcell in gdsii.top_level():
    tessellate(topcell)
    # layers = topcell.get_polygons(by_spec = True)
    # for l in layers:
    #     print(l)
    #     tessellate(topcell,l)

    gdspy.write_gds('test2.gds')
    gdspy.LayoutViewer(cells = topcell, depth=len(topcell.get_dependencies(recursive = True)))

