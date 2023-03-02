# $autorun
# -*- coding: utf-8 -*-
"""
@author: Ashkan
Email:ashkan.rezaee@uab.cat
"""

import pya

class Via(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the Via.
    """
    def __init__(self):

        # Initialize the super class
        super(Via, self).__init__()

        # Declare the parameters
        self.param("r", self.TypeDouble, "Via radius", default=1.25)
        self.param("ov", self.TypeDouble, "Overlap", default=2.5)
        self.param("f_lay", self.TypeInt, "First layer", default=3)
        self.param("s_lay", self.TypeInt, "Second layer", default=4)

    def display_text_impl(self):
        """
        Provide a descriptive text for the cell.
        """
        return "Via"

    def can_create_from_shape_impl(self):
        """
        Implement the "Create PCell from shape" protocol: we can use any shape which 
        has a finite bounding box.
        """
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()

    def produce_impl(self):
        """
        Create the Via PCell.
        """
        nr = 128  # Number of points in a circle

        # Define layer names
        layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
        # Unpack layers into variables
        txt, bm, bl, sd, gm, pv, gc, pv2 = layers
        dbu = self.layout.dbu
        r = self.r / dbu
        ov = self.ov / dbu

        # Create via region
        via_box = pya.Region(pya.Box(-r, -r, r, r)).rounded_corners(0, 2*r, nr)
        self.cell.shapes(pv).insert(via_box)
        self.cell.shapes(self.f_lay).insert(via_box.sized(ov))
        self.cell.shapes(self.s_lay).insert(via_box.sized(ov))