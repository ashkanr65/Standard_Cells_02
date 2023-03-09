# $autorun
# -*- coding: utf-8 -*-
"""
@author: Ashkan
Email:ashkan.rezaee@uab.cat
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
    # Provide a descriptive text for the cell
    return "Pads"

  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which 
    # has a finite bounding box
    return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
     
  def create_pad(self, x, y, a, b):
    # This is the main part of the implementation: create the layout

    # fetch the parameters
    # Get the database unit, as w_via_cir is defined in microns the conversion is needed
    dbu = self.layout.dbu   
    w_via_cir = 2.5 / dbu
    
    # Resize x, y coordinates, width and height to be measured in terms of dbu
    x, y, a, b = x / dbu, y / dbu, a / dbu, b / dbu
    
    # Define sd_width for later use
    sd_width = 50 / dbu
    
    # Define other design rules and fixed objects (measured in terms of dbu)
    ov = 2.5 / dbu    # via overlap 
    nr = 128          # Number of points in a circle
    
    # Obtain layer objects by calling the layout's layer method with desired layer indexes.
    layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
    
    # Unpack values from list comprehension into convenient named variables 
    txt, bm, bl, sd, gm, pv, gc, pv2 = layers
    
    # Create area object using pya.Region() for specified box
    area = pya.Region(pya.Box(x + 0, y + 0, x + a, y + b))
    
    # Connect area object with specific Layers viathe shapes method of this cell
    # polygon inside geometry contains rectangle defined by x,y,a,b 
    self.cell.shapes(gc).insert(area)  
    self.cell.shapes(bm).insert(area)
    
    # Create another Region object for the bar 
    sd_region_bar = pya.Region(pya.Box(x + sd_width, y + sd_width, x + a - sd_width, y + b - sd_width))
    
    # Insert masked areas using shape's difference method which subtracts overlapped areas from given shape 
    self.cell.shapes(sd).insert(area - sd_region_bar)    
    self.cell.shapes(gc).insert(area - sd_region_bar)
    
    # For the given heights around segment, create a partial ellipse with defined radius size and find their location on print board.
    ho = [b - (sd_width / 2), (sd_width / 2)]
    for i in (ho):
        circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
            x + (a / 2 - (w_via_cir)),   # xmin 
            y + (i  - (w_via_cir)),     # ymin
            x + (a / 2 + (w_via_cir)),   # xmax
            y + (i + (w_via_cir)),      # ymax
            ), nr)   # nr defines number of points to represent elipse shape 
    
        # nested loops to insert the via shapes into coordinates determined from mathematical operations       
        p = 0     #counter variable initialization
        while ( p + 1 < (sd_width / 2) / (2 * w_via_cir + 2 * ov)):   # conditional check with mathematical operation
            k = 0   # counter variable initialization
            while ( k + 1 < (a / 2 ) / (2 * w_via_cir + 4 * ov)):   # conditional check with mathematical operation
                ho_x = [k * (2 * w_via_cir + 4 * ov), -k * (2 * w_via_cir + 4 * ov)] # list of X-coordinates determined mathematically during every iteration.
                ho_y = [p * (2 * w_via_cir + 4 * ov), -p * (2 * w_via_cir + 4 * ov)] # list of Y-coordinates determined mathematically during every iteration. 
                for i in (ho_x):           # loop through X-coordinate list 
                    for j in (ho_y):       # loop through Y-coordinate list
                        self.cell.shapes(pv).insert(circumscribed_circle_via.moved( #add this shape to polygon layer with a move function
                        i, j))
                        self.cell.shapes(gc).insert(circumscribed_circle_via.moved(  # add a duplicate of that shape to the guard ring layer.
                        i, j).sized(2 * ov))
                k += 1     # progress the counter variable k by 1
            p += 1         #progress the counter
        

        # Creates a list of two elements representing the position of vias along the vertical axis.
        ve = [a - (sd_width / 2), (sd_width / 2)]
    
        # Loop through the two elements in the ve list.
        for j in (ve):
            # Create a polygon object with a circular shape that circumscribes via, using DBox to specify its dimensions.
            circumscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
                x + (j - (w_via_cir)),
                y + (b / 2  - (w_via_cir)),
                x + (j + (w_via_cir)),
                y + (b / 2 + (w_via_cir)),
            ), nr)
    
            # layout
            p = 0
            # The first nested loop increments by multiples of horizontal pitch and adds 5 times spacing between vias. 
            while ( p + 1 < ((b - sd_width) / 2) / (2 * w_via_cir + 5 * ov)):
                k = 0 
                # The second nested loop increments by multiples of vertical pitch and adds 2 times spacing between vias.  
                while ( k + 1 < (sd_width / 2 ) / (2 * w_via_cir + 2 * ov)):
                    # Calculates the horizontal and vertical positioning of the vias and stores them into the lists ho_x and ho_y.
                    ho_x = [k * (2 * w_via_cir + 4 * ov), -k * (2 * w_via_cir + 4 * ov)]
                    ho_y = [p * (2 * w_via_cir + 4 * ov), -p * (2 * w_via_cir + 4 * ov)]
                    # Loop through the values in the ho_x and ho_y lists and insert the polyogns, both as themselves and sized up with the constant ov.
                    for i in (ho_x):
                        for j in (ho_y):
                            self.cell.shapes(pv).insert(circumscribed_circle_via.moved(i, j))
                            self.cell.shapes(gc).insert(circumscribed_circle_via.moved(i, j).sized(2 * ov))
                    k += 1
                p += 1
    
        # Inscribed
        # Create a polygon object with a circular shape that inscribes via, using DBox to specify its dimensions.
        inscribed_circle_via = pya.Polygon().ellipse(pya.DBox(
              x + (a / 2- (1.5 * w_via_cir)),
              y + (b / 2 - (1.5 * w_via_cir)),
              x + (a / 2 + (1.5 * w_via_cir)),
              y + (b / 2 + (1.5 * w_via_cir)),
            ), nr) 
    
        # The code above creates vias both using a circumscribed and inscribed circle, depending on size requirements.
    
        # p and k correspond to the number of inscribed circles that can be inserted vertically or horizontally given current dimensions
        p = 0
        while ( p+1 < (b/2 - sd_width) / (3*w_via_cir+6*ov)):  
            k = 0 
            while ( k+1 < (a/2 - sd_width) / (3*w_via_cir+6*ov)):
    
                # Find candidate locations for horizontal wire segments
                ho_x = [k * (3 * w_via_cir + 6 * ov), -k * (3 * w_via_cir + 6 * ov)]
    
                # Find candidate locations for vertical wire segments
                ho_y = [p * (3 * w_via_cir + 6 * ov), -p * (3 * w_via_cir + 6 * ov)]
                
                # Iterate over all candidate locations and insert shapes in each one.
                for i in (ho_x):
                    for j in (ho_y):
                        self.cell.shapes(pv).insert(inscribed_circle_via.moved(
                        i, j))
                        self.cell.shapes(gc).insert(inscribed_circle_via.moved(
                        i, j).sized(3 * ov))
                k += 1
            p += 1
    

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
    coords = [(i*500+750)/dbu for i in range(16)]
    paths = [pya.Path([pya.Point(c, 0), pya.Point(c, 9000/dbu)], 0.1) for c in coords] + \
            [pya.Path([pya.Point(0, c), pya.Point(9000/dbu, c)], 0.1) for c in coords]
    for path in paths:
        self.cell.shapes(txt).insert(path)

    circle = pya.Region(pya.Box(4350/dbu,4350/dbu,4650/dbu,4650/dbu)).rounded_corners(0, 200/dbu, nr)
    circle = circle - pya.Region(pya.Box(4400/dbu,4400/dbu,4600/dbu,4600/dbu)).rounded_corners(0, 100/dbu, nr)
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
    for k in (bo):
        for i in range(16):
            # Create a pad on the top side of the circuit board
            self.create_pad(625+(i*500), k, 250, 400)
            # Create a pad on the back side of the circuit board
            self.create_pad(k, 625+(i*500), 400, 250)

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