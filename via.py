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
        self.param("radius", self.TypeDouble, "Via radius", default=1.75)   # declaring the radius parameter (default is 1.25)
        self.param("overlap", self.TypeDouble, "Overlap", default=3.5)     # declaring the overlap parameter (default is 2.5)
        self.param("first_layer", self.TypeDouble, "First layer", default=1)   # declaring the first layer parameter (default is 1)
        self.param("Circles", self.TypeBoolean, "Circles", default= True)     # declaring the circles parameter (default is True))

    def display_text_impl(self):
        """
        Provide a descriptive text for the cell.
        """
        return "Via"

    def coerce_parameters_impl(self):
        # Check if layer has been selected correctly   
        if self.first_layer not in [1, 3, 4]:    # checks if first layer is either 1, 3, or 4
            raise Exception("Incorrect layer has been selected")
        
        # Check radius   
        if self.radius < 1.75:      # checks if radius is less than 1.25
            raise Exception("You cannot make radius smaller than 1.25")
        
        # Check overlap
        if self.overlap < 3.5:      # checks if overlap is less than 2.5
            raise Exception("Overlap cannot be less than 2.5")

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

        # Define layer names and layes using list comprehension
        txt, bm, bl, sd, gm, pv, gc, pv2 = [self.layout.layer(i, 0) for i in range(10) if i in [0, 1, 2, 3, 4, 6, 7, 9]]
        dbu = self.layout.dbu       # gets the database unit
        radius = self.radius / dbu   # calculates the radius in terms of DBU
        overlap = self.overlap / dbu   # calculates the ovelap in terms of DBU
        
        # Create via region using pya.Region()
        via_circle = pya.Polygon().ellipse(pya.DBox(-radius, -radius, radius, radius), nr)
        # Insert shapes into specific layers
        self.cell.shapes(pv).insert(via_circle)
        # Check whether or not via is circle
        if self.Circles:
            # If True, insert via_circle with the specified overlap into both shapes on first_layer and gc layers
            self.cell.shapes(self.first_layer).insert(via_circle.sized(overlap))
            self.cell.shapes(gc).insert(via_circle.sized(overlap))
        else:
            # If False, create a box called via_box with dimensions [-radius, -radius, radius, radius], in a Region object
            via_box = pya.Region(pya.Box(-radius, -radius, radius, radius))
            # Insert the via_box with specified overlap into both shapes on first_layer and gc layers
            self.cell.shapes(self.first_layer).insert(via_box.sized(overlap))
            self.cell.shapes(gc).insert(via_box.sized(overlap))

        # Center the Via region
        # Define vertical line using pya Path and add it to the layout cell 
        vert = pya.Path([
            pya.Point(-radius, 0),
            pya.Point(radius, 0)
        ], radius)
        self.cell.shapes(gc).insert(vert)
        
        # Define horizontal line using pya Path and add it to the layout cell
        hor = pya.Path([
            pya.Point(0, -radius),
            pya.Point(0, radius)
        ], radius)
        self.cell.shapes(gc).insert(hor)   
