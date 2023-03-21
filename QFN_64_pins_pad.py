# $autorun
# -*- coding: utf-8 -*-
"""
PCell declaration for the QFN_64_pins_pad.
Author: Ashkan (ashkan.rezaee@uab.cat)
"""

import pya

class QFN_64_pins_pad(pya.PCellDeclarationHelper):
    """
    The PCell declaration for the QFN_64_pins_pad.
    """

    def __init__(self):

        # Important: initialize the super class
        super(QFN_64_pins_pad, self).__init__()

        # declare the parameters

    def display_text_impl(self):
        # Return the descriptive text for the cell
        return "QFN_64_pins_pad"

    def can_create_from_shape_impl(self):
        # Implement the "Create PCell from shape" protocol
        # This PCell can be created from any shape with a finite bounding box
        return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
     
    def create_pad(self, x, y, a, b, rot):
        """
        This function creates a layout pad at position (x,y) with width 'a' and height 'b', rotated by angle 'rot'.
        
        :param x: x-coordinate of the pad
        :param y: y-coordinate of the pad
        :param a: width of the pad
        :param b: height of the pad
        :param rot: rotation angle of the pad
        """
        # Get the database unit, as w_via_cir is defined in microns the conversion is needed
        dbu = self.layout.dbu   
        w_via_cir = 2.5 / dbu
        # Resize x,y coordinates and width/height to be measured in terms of dbu.
        x /= dbu
        y /= dbu
        a /= dbu
        b /= dbu
        
        # Define sd_width for later use
        sd_width = 50 / dbu
        pv_cir_sd = 6 / dbu
        ov_cir_sd = 7 / dbu
        in_h_cir_sd = 22 / dbu
        in_v_cir_sd = 27 / dbu
        inner_cir_via = 10 / dbu
        inner_ov_via = 10 / dbu

        # Define other design rules and fixed objects (measured in terms of dbu)
        ov = 2.5 / dbu    # via overlap 
        nr = 128          # Number of points in a circle
        
        # Obtain layer objects by calling the layout's layer method with desired layer indexes.
        layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
        
        # Unpack values from list comprehension into convenient named variables 
        txt, bm, bl, sd, gm, pv, gc, pv2 = layers
        
        # Define the area region as a rectangle with bottom-left corner at (x,y) and top-right corner at (x+a,y+b).
        area = pya.Region(pya.Box(x, y, x + a, y + b))

        # Calculate the center point of the area region.
        center_x = area.bbox().center().x
        center_y = area.bbox().center().y

        # Create a transformation object for rotation around the center point.
        if rot == False:
            trans = pya.Trans(pya.Trans.R0)
        else:
            trans = pya.Trans(pya.Trans.R90)

        # Apply the transformation to the area region.
        area = area.transform(trans)
        
        # Connect area object with specific layers via the shapes method of this cell.
        self.cell.shapes(gc).insert(area)  
        self.cell.shapes(bm).insert(area)
            
        # Create another Region object for the bar.
        sd_region_bar = pya.Region(pya.Box(area.bbox().left + sd_width,
            area.bbox().bottom + sd_width,
            area.bbox().right - sd_width,
            area.bbox().top - sd_width))
        
        # Subtract the bar region from the area region to create a new region.
        sd_region = area - sd_region_bar
        
        # Insert masked areas using shape's difference method which subtracts overlapped areas from given shape.
        self.cell.shapes(sd).insert(sd_region)

        # Inserts sd_region shape with the defined parameters again to the 'gc' layer of a cell object.
        self.cell.shapes(gc).insert(sd_region)
        
        # Resizes the sd_region by subtracting the given value from its dimensions and assigns the result to pc_sd_region variable.
        pv_sd_region = sd_region.sized(-(4*w_via_cir + 4*ov))
        
        # Inserts pc_sd_region shape with defined parameters to the 'pv' layer of a cell object.
        self.cell.shapes(pv).insert(pv_sd_region)
        
        # Create GC-PV attachment
        spacing = 6*w_via_cir + 6*ov
        gc_pv_attachment = pya.Region(pya.Box(sd_region_bar.bbox().left + spacing,
            sd_region_bar.bbox().bottom + spacing,
            sd_region_bar.bbox().right - spacing,
            sd_region_bar.bbox().top - spacing))
        self.cell.shapes(pv).insert(gc_pv_attachment)    
        
        # Calculate values for m,n,k,l depending on the value of rot.
        if rot == False:
            m = int(a * dbu / 21)
            n = int((a * dbu - 50) / 21)
            k = int((b * dbu - 20) / 21)
            l = int((b * dbu - 85) / 21)
        else:
            m = int(b * dbu / 22)
            n = int((b * dbu - 50) / 21)
            k = int(a * dbu / 21)
            l = int((a * dbu - 75) / 21)

        # Create a circumscribed circle via depending on the value of rot.
        # Create Outer horizontal vias
        if rot == False:
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                area.bbox().left + in_h_cir_sd,
                area.bbox().bottom + ov_cir_sd,
                area.bbox().left + in_h_cir_sd + pv_cir_sd,
                area.bbox().bottom + ov_cir_sd + pv_cir_sd
            ), nr)
        else:
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                area.bbox().left + in_v_cir_sd,
                area.bbox().bottom + ov_cir_sd,
                area.bbox().left + in_v_cir_sd + pv_cir_sd,
                area.bbox().bottom + ov_cir_sd + pv_cir_sd
            ), nr)
        # Insert circumscribed_circle_via into the pv and gc layers of the cell object.
        for i in range(m):
            self.cell.shapes(pv).insert(circumscribed_circle_via)
            self.cell.shapes(gc).insert(circumscribed_circle_via.sized(ov_cir_sd))
            
            # Move circumscribed_circle_via vertically depending on the value of rot.
            if rot == False:
                self.cell.shapes(pv).insert(circumscribed_circle_via.moved(0, b - (2 * ov_cir_sd + pv_cir_sd)))
                self.cell.shapes(gc).insert(circumscribed_circle_via.moved(0, b - (2 * ov_cir_sd + pv_cir_sd)).sized(ov_cir_sd))
            else:
                self.cell.shapes(pv).insert(circumscribed_circle_via.moved(0, a - (2 * ov_cir_sd + pv_cir_sd)))
                self.cell.shapes(gc).insert(circumscribed_circle_via.moved(0, a - (2 * ov_cir_sd + pv_cir_sd)).sized(ov_cir_sd))
            
            # Move circumscribed_circle_via horizontally.
            circumscribed_circle_via = circumscribed_circle_via.moved(2 * ov_cir_sd + pv_cir_sd, 0)

        # Create Inner horizontal vias
        if rot == False:
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                area.bbox().left + 7 * pv_cir_sd,
                area.bbox().bottom + ov_cir_sd + 5 * pv_cir_sd,
                area.bbox().left + 8 * pv_cir_sd,
                area.bbox().bottom + ov_cir_sd + pv_cir_sd + 5 * pv_cir_sd
            ), nr)
        else:
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                area.bbox().left + 7 * pv_cir_sd + 2 * ov,
                area.bbox().bottom + ov_cir_sd + 5 * pv_cir_sd,
                area.bbox().left + 8 * pv_cir_sd + 2 * ov,
                area.bbox().bottom + ov_cir_sd + pv_cir_sd + 5 * pv_cir_sd,
            ), nr)
        
        for i in range(n):
            self.cell.shapes(pv).insert(circumscribed_circle_via)
            self.cell.shapes(gc).insert(circumscribed_circle_via.sized(ov_cir_sd))

            # Move circumscribed_circle_via vertically depending on the value of rot.
            if ( rot == False):
                self.cell.shapes(pv).insert(circumscribed_circle_via.moved(0, b - (8 * ov_cir_sd + 4 * pv_cir_sd)))
                self.cell.shapes(gc).insert(circumscribed_circle_via.moved(0, b - (8 * ov_cir_sd + 4 * pv_cir_sd)).sized(ov_cir_sd))
            else:
                self.cell.shapes(pv).insert(circumscribed_circle_via.moved(0, a - (8 * ov_cir_sd + 4 * pv_cir_sd)))
                self.cell.shapes(gc).insert(circumscribed_circle_via.moved(0, a - (8 * ov_cir_sd + 4 * pv_cir_sd)).sized(ov_cir_sd))
            
            # Move circumscribed_circle_via horizontally.
            circumscribed_circle_via = circumscribed_circle_via.moved(2 * ov_cir_sd + pv_cir_sd, 0)

        # Outer vertical part of the bar
        if rot == False:
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                area.bbox().left + ov_cir_sd,
                area.bbox().bottom + in_v_cir_sd,
                area.bbox().left + ov_cir_sd + pv_cir_sd,
                area.bbox().bottom + in_v_cir_sd + pv_cir_sd,
            ), nr)
        else:
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                area.bbox().left + ov_cir_sd,
                area.bbox().bottom + in_h_cir_sd,
                area.bbox().left + ov_cir_sd + pv_cir_sd,
                area.bbox().bottom + in_h_cir_sd + pv_cir_sd,
            ), nr)
        
        for i in range(k):
            self.cell.shapes(pv).insert(circumscribed_circle_via)
            self.cell.shapes(gc).insert(circumscribed_circle_via.sized(ov_cir_sd))

            # Move circumscribed_circle_via vertically depending on the value of rot.
            if rot == False:
                self.cell.shapes(pv).insert(circumscribed_circle_via.moved(a - (2 * ov_cir_sd + pv_cir_sd), 0))
                self.cell.shapes(gc).insert(circumscribed_circle_via.moved(a - (2 * ov_cir_sd + pv_cir_sd), 0).sized(ov_cir_sd))
            else:
                self.cell.shapes(pv).insert(circumscribed_circle_via.moved(b - (2 * ov_cir_sd + pv_cir_sd), 0))
                self.cell.shapes(gc).insert(circumscribed_circle_via.moved(b - (2 * ov_cir_sd + pv_cir_sd), 0).sized(ov_cir_sd))
            
            # Move circumscribed_circle_via horizontally.
            circumscribed_circle_via = circumscribed_circle_via.moved(0, 2 * ov_cir_sd + pv_cir_sd)

        # Inner vertical part of the bar
        if rot == False:
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                area.bbox().left + in_v_cir_sd + 0.5 * pv_cir_sd + ov_cir_sd,
                area.bbox().bottom + in_v_cir_sd + 5 * pv_cir_sd,
                area.bbox().left + in_v_cir_sd + 1.5 * pv_cir_sd + ov_cir_sd,
                area.bbox().bottom + in_v_cir_sd + 6 * pv_cir_sd,
            ), nr)
        else:
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                area.bbox().left + in_h_cir_sd + 2 / dbu + pv_cir_sd + ov_cir_sd,
                area.bbox().bottom + in_h_cir_sd + 5 * pv_cir_sd,
                area.bbox().left + in_h_cir_sd + 2 / dbu + 2 * pv_cir_sd + ov_cir_sd,
                area.bbox().bottom + in_h_cir_sd + 6 * pv_cir_sd,
            ), nr)

        for i in range(l):
            self.cell.shapes(pv).insert(circumscribed_circle_via)
            self.cell.shapes(gc).insert(circumscribed_circle_via.sized(ov_cir_sd))

            # Move circumscribed_circle_via vertically depending on the value of rot.
            if rot == False:
                self.cell.shapes(pv).insert(circumscribed_circle_via.moved(a - (8 * ov_cir_sd + 4 * pv_cir_sd), 0))
                self.cell.shapes(gc).insert(circumscribed_circle_via.moved(a - (8 * ov_cir_sd + 4 * pv_cir_sd), 0).sized(ov_cir_sd))
            else:
                self.cell.shapes(pv).insert(circumscribed_circle_via.moved(b - (8 * ov_cir_sd + 4 * pv_cir_sd), 0))
                self.cell.shapes(gc).insert(circumscribed_circle_via.moved(b - (8 * ov_cir_sd + 4 * pv_cir_sd), 0).sized(ov_cir_sd))

            # Move circumscribed_circle_via horizontally.
            circumscribed_circle_via = circumscribed_circle_via.moved(0, 2 * ov_cir_sd + pv_cir_sd)


        # Inner circle vias
        if rot == False:
            Inscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                    sd_region_bar.bbox().left + inner_ov_via,
                    sd_region_bar.bbox().bottom + inner_ov_via,
                    sd_region_bar.bbox().left + inner_ov_via + inner_cir_via,
                    sd_region_bar.bbox().bottom + inner_ov_via + inner_cir_via,
                ), nr)
        else:
            Inscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                    sd_region_bar.bbox().left + inner_ov_via,
                    sd_region_bar.bbox().bottom + inner_ov_via,
                    sd_region_bar.bbox().left + inner_ov_via + inner_cir_via,
                    sd_region_bar.bbox().bottom + inner_ov_via + inner_cir_via,
                ), nr)

        for i in range(5):
            self.cell.shapes(pv).insert(Inscribed_circle_via)
            self.cell.shapes(gc).insert(Inscribed_circle_via.sized(inner_ov_via))

            # Move circumscribed_circle_via vertically depending on the value of rot.
            if rot == False:
                self.cell.shapes(pv).insert(Inscribed_circle_via.moved(0, 270 / dbu))
                self.cell.shapes(gc).insert(Inscribed_circle_via.moved(0, 270 / dbu).sized(inner_ov_via))
                # Move circumscribed_circle_via horizontally.
                Inscribed_circle_via = Inscribed_circle_via.moved(inner_cir_via + 2 * inner_ov_via, 0)
            else:
                self.cell.shapes(pv).insert(Inscribed_circle_via.moved(270 / dbu, 0))
                self.cell.shapes(gc).insert(Inscribed_circle_via.moved(270 / dbu, 0).sized(inner_ov_via))
                # Move circumscribed_circle_via horizontally.
                Inscribed_circle_via = Inscribed_circle_via.moved(0, inner_cir_via + 2 * inner_ov_via)
            
        # Inner circle vias
        if rot == False:
            Inscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                    sd_region_bar.bbox().left + inner_ov_via,
                    sd_region_bar.bbox().bottom + inner_ov_via,
                    sd_region_bar.bbox().left + inner_ov_via + inner_cir_via,
                    sd_region_bar.bbox().bottom + inner_ov_via + inner_cir_via,
                ), nr)
        else:
            Inscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                    sd_region_bar.bbox().left + inner_ov_via,
                    sd_region_bar.bbox().bottom + inner_ov_via,
                    sd_region_bar.bbox().left + inner_ov_via + inner_cir_via,
                    sd_region_bar.bbox().bottom + inner_ov_via + inner_cir_via,
                ), nr)

        for i in range(10):
            self.cell.shapes(pv).insert(Inscribed_circle_via)
            self.cell.shapes(gc).insert(Inscribed_circle_via.sized(inner_ov_via))

            # Move circumscribed_circle_via vertically depending on the value of rot.
            if rot == False:
                self.cell.shapes(pv).insert(Inscribed_circle_via.moved(120 / dbu, 0))
                self.cell.shapes(gc).insert(Inscribed_circle_via.moved(120 / dbu, 0).sized(inner_ov_via))
                # Move circumscribed_circle_via horizontally.
                Inscribed_circle_via = Inscribed_circle_via.moved(0, inner_cir_via + 2 * inner_ov_via)
            else:
                self.cell.shapes(pv).insert(Inscribed_circle_via.moved(0, 120 / dbu))
                self.cell.shapes(gc).insert(Inscribed_circle_via.moved(0, 120 / dbu).sized(inner_ov_via))
                # Move circumscribed_circle_via horizontally.
                Inscribed_circle_via = Inscribed_circle_via.moved(inner_cir_via + 2 * inner_ov_via, 0)


    def cut(self):
        dbu = self.layout.dbu
        # Define layer names -> not used in the code, commented out
        # layer_names = ["txt", "bm", "bl", "sd", "gm", "pv", "gc", "pv2"]
        
        # Assign layers to variables using list comprehension
        layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
        
        # Unpack layers variable into individual layer variables
        txt, bm, bl, sd, gm, pv, gc, pv2 = layers 
        
        # Set nr value to 128
        nr = 128
        
        # Creates a cut polygon 
        cut = pya.Region(pya.Polygon([
        pya.Point(0/dbu, 0/dbu),
        pya.Point(0/dbu, -285/dbu),
        pya.Point(-285/dbu, -285/dbu),
        pya.Point(-285/dbu, -195/dbu),
        pya.Point(-90/dbu, -195/dbu),
        pya.Point(-90/dbu, 0/dbu)
        ]))
        
        # Sets angles and their corresponding asscoiated (x,y) vertices
        angles = [180, 0, 270, 90]
        coords = [(-435, -150), (9435, 9150), (9150, -435), (-150, 9435)]
        
        # Assign rotation transformations using list comprehension
        rotation = [pya.ICplxTrans(1.0, a, True, x/dbu, y/dbu) for a,(x,y) in zip(angles, coords)]
        layer = [bm, sd, gc]
        for i in range (4):
            for j in layer:
                self.cell.shapes(j).insert(cut, rotation[i])
        
        # Cell separation txt lines
        coords = [(i * 500 + 750)/dbu for i in range(16)]
        paths = [pya.Path([pya.Point(c, 0), pya.Point(c, 9000 / dbu)], 0.1) for c in coords] + \
                [pya.Path([pya.Point(0, c), pya.Point(9000 / dbu, c)], 0.1) for c in coords]
        for path in paths:
            self.cell.shapes(txt).insert(path)

        circle = pya.Region(pya.Box(4350 / dbu, 4350 / dbu, 4650 / dbu, 4650 / dbu)).rounded_corners(0, 200 / dbu, nr)
        circle = circle - pya.Region(pya.Box(4400 / dbu, 4400 / dbu, 4600 / dbu, 4600 / dbu)).rounded_corners(0, 100 / dbu, nr)
        self.cell.shapes(bm).insert(circle)

    def impl(self):
        #Definitions
        dbu = self.layout.dbu
        ind_sz = 500 / dbu
        # Define layer names
        # layer_names = ["txt", "bm", "bl", "sd", "gm", "pv", "gc", "pv2"]
        # Assign layers using list comprehension
        layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
        # Unpack layers into variables
        txt, bm, bl, sd, gm, pv, gc, pv2 = layers

        # TOP layout
        # Set the name of the layout
        name = pya.TextGenerator.default_generator().text
        # Add a label to the layout for the back side of the circuit board
        self.cell.shapes(bm).insert((name("Back", 0.001, 210)), pya.DTrans(90, True, 500, 350))
        # Add a label to the layout for the top side of the circuit board
        self.cell.shapes(gc).insert((name("TOP", 0.001, 290)), pya.DTrans(0, False, 0, 0))
        # Add a right arrow to the layout to indicate orientation
        self.cell.shapes(bm).insert((name(">>>>", 0.001, 220)), pya.DTrans(0, False, 0, 200))
        self.cell.shapes(gc).insert((name(">>>>", 0.001, 220)), pya.DTrans(0, False, 0, 200))

        # Cut the layout
        self.cut()

        # Set the position of the pads
        bo = [0, 8600]
        # self.create_pad(625, 0, 250, 400, False)
        # self.create_pad(625, -400, 250, 400, True)
 
        for k in (bo):
            for i in range(16):
                # Create a pad on the top side of the circuit board
                self.create_pad(625+(i*500), k, 250, 400, False)

                # Create a pad on the back side of the circuit board
                self.create_pad(625+(i*500), k - 9000, 250, 400, True)


    def produce_impl(self):
        
        self.impl()

class MyLib(pya.Library):

#The library where we will put the PCell into 

    def __init__(self):

        # Set the description
        self.description = "QFN_64_pins_pad"
        
        # Create the PCell declarations
        self.layout().register_pcell("QFN_64_pins_pad", QFN_64_pins_pad())
        # That would be the place to put in more PCells ...
        
        # Register us with the name "MyLib".
        # If a library with that name already existed, it will be replaced then.
        self.register("QFN_64_pins_pad")

# Instantiate and register the library
MyLib() 