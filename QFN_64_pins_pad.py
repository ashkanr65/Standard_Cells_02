# $autorun
# -*- coding: utf-8 -*-
"""
@author: Ashkan
Email:ashkan.rezaee@uab.cat
"""

import pya

class QFN_64_pins_pad(pya.PCellDeclarationHelper):
  """
  The PCell declaration for the Corbino
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
        dbu = self.layout.dbu
        w_via_cir = 2.5 / dbu
        x, y, a, b = x / dbu, y / dbu, a / dbu, b / dbu
        sd_width = 50 / dbu
        
        # Other design rules and other "fixed" variables
        ov = 2.5 / dbu
        nr = 128  # Number of points in a circle
        txt = self.layout.layer(0,0)
        bm = self.layout.layer(1, 0)
        bl = self.layout.layer(2, 0)
        sd = self.layout.layer(3, 0)
        gm = self.layout.layer(4, 0)
        pv = self.layout.layer(6, 0)
        gc = self.layout.layer(7, 0)
        pv2 = self.layout.layer(9, 0)

        area = pya.Region(pya.Box(x + 0, y + 0, x + a, y + b))
        self.cell.shapes(gc).insert(area)
        self.cell.shapes(bm).insert(area)
        # circumscribed 
        sd_region_bar = pya.Region(pya.Box(x + sd_width, y + sd_width, x + a - sd_width, y + b - sd_width))
        self.cell.shapes(sd).insert(area - sd_region_bar)
        self.cell.shapes(gc).insert(area - sd_region_bar)

        # Horizontal
        ho = [b - (sd_width / 2), (sd_width / 2)]
        for i in (ho):
            circumscribed_circle_via = pya.Region(pya.Box(
            x + (a / 2 - (w_via_cir)),
            y + (i  - (w_via_cir)),
            x + (a / 2 + (w_via_cir)),
            y + (i + (w_via_cir)),
            )).rounded_corners(0, 2 * w_via_cir, nr)
            # layout
            p = 0
            while ( p + 1 < (sd_width / 2) / (2 * w_via_cir + 2 * ov)):
                k = 0 
                while ( k + 1 < (a / 2 ) / (2 * w_via_cir + 4 * ov)):
                    ho_x = [k * (2 * w_via_cir + 4 * ov), -k * (2 * w_via_cir + 4 * ov)]
                    ho_y = [p * (2 * w_via_cir + 4 * ov), -p * (2 * w_via_cir + 4 * ov)]
                    for i in (ho_x):
                        for j in (ho_y):
                            self.cell.shapes(pv).insert(circumscribed_circle_via.moved(
                            i, j))
                            self.cell.shapes(gc).insert(circumscribed_circle_via.moved(
                            i, j).sized(2 * ov))
                    k += 1
                p += 1

        # Vertical
        ve = [a - (sd_width / 2), (sd_width / 2)]
        for j in (ve):
            circumscribed_circle_via = pya.Region(pya.Box(
            x + (j - (w_via_cir)),
            y + (b / 2  - (w_via_cir)),
            x + (j + (w_via_cir)),
            y + (b / 2 + (w_via_cir)),
            )).rounded_corners(0, 2 * w_via_cir, nr)
            # layout
            p = 0
            while ( p + 1 < ((b - sd_width) / 2) / (2 * w_via_cir + 5 * ov)):
                k = 0 
                while ( k + 1 < (sd_width / 2 ) / (2 * w_via_cir + 2 * ov)):
                    ho_x = [k * (2 * w_via_cir + 4 * ov), -k * (2 * w_via_cir + 4 * ov)]
                    ho_y = [p * (2 * w_via_cir + 4 * ov), -p * (2 * w_via_cir + 4 * ov)]
                    for i in (ho_x):
                        for j in (ho_y):
                            self.cell.shapes(pv).insert(circumscribed_circle_via.moved(
                            i, j))
                            self.cell.shapes(gc).insert(circumscribed_circle_via.moved(
                            i, j).sized(2 * ov))
                    k += 1
                p += 1

        # Inscribed
        inscribed_circle_via = pya.Region(pya.Box(
          x + (a / 2- (1.5 * w_via_cir)),
          y + (b / 2 - (1.5 * w_via_cir)),
          x + (a / 2 + (1.5 * w_via_cir)),
          y + (b / 2 + (1.5 * w_via_cir)),
        )).rounded_corners(0, 3 * w_via_cir, nr)
        # layout
        p = 0
        while ( p+1 < (b/2 - sd_width) / (3*w_via_cir+6*ov)):
            k = 0 
            while ( k+1 < (a/2 - sd_width) / (3*w_via_cir+6*ov)):

                ho_x = [k * (3 * w_via_cir + 6 * ov), -k * (3 * w_via_cir + 6 * ov)]
                ho_y = [p * (3 * w_via_cir + 6 * ov), -p * (3 * w_via_cir + 6 * ov)]
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
    txt = self.layout.layer(0,0)
    bm = self.layout.layer(1, 0)
    bl = self.layout.layer(2, 0)
    sd = self.layout.layer(3, 0)
    gm = self.layout.layer(4, 0)
    pv = self.layout.layer(6, 0)
    gc = self.layout.layer(7, 0)
    pv2 = self.layout.layer(9, 0)

    cut = pya.Region(pya.Polygon([

       pya.Point(0/dbu, 0/dbu),
       pya.Point(0/dbu, -285/dbu),
       pya.Point(-285/dbu, -285/dbu),
       pya.Point(-285/dbu, -195/dbu),
       pya.Point(-90/dbu, -195/dbu),
       pya.Point(-90/dbu, 0/dbu)
    ]))
    rotation = []
    rotation.append(pya.ICplxTrans(float (1), float(180), True, -435/dbu, -150/dbu))
    rotation.append(pya.ICplxTrans(float (1), float(0), True, 9435/dbu, 9150/dbu))
    rotation.append(pya.ICplxTrans(float (1), float(270), True, 9150/dbu, -435/dbu))
    rotation.append(pya.ICplxTrans(float (1), float(90), True, -150/dbu, 9435/dbu))
    layer = [bm, sd, gc]
    for i in range (4):
        for j in layer:
            self.cell.shapes(j).insert(cut, rotation[i])

  def impl(self):
    #Definitions
    dbu = self.layout.dbu
    ind_sz = 500 / dbu
    txt = self.layout.layer(0,0)
    bm = self.layout.layer(1, 0)
    bl = self.layout.layer(2, 0)
    sd = self.layout.layer(3, 0)
    gm = self.layout.layer(4, 0)
    pv = self.layout.layer(6, 0)
    gc = self.layout.layer(7, 0)
    pv2 = self.layout.layer(9, 0)
    # TOP layout
    indicator = pya.Region(pya.Box(0, 0, ind_sz, ind_sz))
    self.cell.shapes(sd).insert(indicator)
    name = pya.TextGenerator.default_generator().text\
        ("TOP", 0.001, 290).move(0/dbu, 150/dbu)
    self.cell.shapes(bm).insert(name)
    self.cell.shapes(gc).insert(name)
    name = pya.TextGenerator.default_generator().text\
        (">>>>", 0.001, 220).move(0/dbu, 0/dbu)
    self.cell.shapes(bm).insert(name)
    self.cell.shapes(gc).insert(name)

    self.cut()

    bo = [0, 8600]
    for k in (bo):
        for i in range(16):
            self.create_pad(625+(i*500), k, 250, 400)
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