# $autorun
# -*- coding: utf-8 -*-
"""
@author: Ashkan
Email:ashkan.rezaee@uab.cat
"""

import pya

class Transistor_V2(pya.PCellDeclarationHelper):
  """
  The PCell declaration for the Inverter.
  """

  def __init__(self):

    # Important: initialize the super class
    super(Transistor_V2, self).__init__()

    # declare the parameters
    self.param("w", self.TypeInt, "Width per finger", default = 90)
    self.param("n_d", self.TypeInt, "Number of Channels", default = 1)
    self.param("l_d", self.TypeDouble, "Drive Length", default = 2.5)
    self.param("l_l", self.TypeDouble, "Load Length", default = 2.5)
    self.param("r", self.TypeDouble, "Ratio", default = 1)
    self.param("o", self.TypeDouble, "Metal Overlap", default = 3)
    self.param("gm_ov", self.TypeDouble, "Gate Overlap", default = 1.5)
    self.param("fw", self.TypeDouble, "Finger Width", default = 5)
    self.param("s", self.TypeDouble, "Finger Separation", default = 2.5)
    self.param("via", self.TypeDouble, "via size", default = 3.5)
    self.param("via_ov", self.TypeDouble, "via overlap", default = 3.5)
    self.param("vias", self.TypeInt, "I/O", default = 1)
    self.param("load", self.TypeBoolean, "Load?", default = False)
    self.param("pos", self.TypeInt, "Position", default = 1)
    self.param("int", self.TypeInt, "Internal Connection", default = 0)
    self.param("rail", self.TypeDouble, "rail to finger width ratio", default = 3)
    self.param("PDN_S", self.TypeDouble, "Extra distance for PDN", default = 0)
    self.param("pad", self.TypeBoolean, "Pads", default = False)
    self.param("name", self.TypeString, "name", default = "1_001")

    
  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "STD Cell Inverter:(ratio=" + str((self.r)) + ",Width="+ "90*"+str((self.n_d)) + ")"

  def can_create_from_shape_impl(self):
    # Implement the "Create PCell from shape" protocol: we can use any shape which 
    # has a finite bounding box
    return self.shape.is_box() or self.shape.is_polygon() or self.shape.is_path()
  
  def create_pad(self, x, y):
        # This is the main part of the implementation: create the layout

        # fetch the parameters
        w_dbu = 175 / self.layout.dbu
        l_dbu = 175 / self.layout.dbu
        w_via = 0.0857142857142857 * w_dbu
        l_via = 0.0857142857142857 * l_dbu
        w_via_cir = 5 / self.layout.dbu
        l_via_cir = 5 / self.layout.dbu

        # Other design rules and other "fixed" variables
        posx = x / self.layout.dbu
        posy = y / self.layout.dbu

        nr = 128  # Number of points in a circle
        # Define layer names
        # Assign layers using list comprehension
        layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
        # Unpack layers into variables
        txt, bm, bl, sd, gm, pv, gc, pv2 = layers

        # create the shape
        # back-gate layer
        full_region = pya.Box(posx - w_dbu / 2, posy - l_dbu / 2, posx + w_dbu / 2, posy + l_dbu / 2)
        # print region
        self.cell.shapes(bm).insert(full_region)

        # gate connection layer
        self.cell.shapes(gc).insert(full_region)

        # inner via
        square_region = pya.Region(
            pya.Box(posx - w_dbu * 0.73 / 2, posy - l_dbu * 0.73 / 2, posx + w_dbu * 0.73 / 2, posy + l_dbu * 0.73 / 2))
        # print region
        self.cell.shapes(pv).insert(square_region)

        # sqaure sd layer
        b_region = pya.Region(pya.Box(posx - w_dbu / 2, posy - l_dbu / 2, posx + w_dbu / 2, posy - l_dbu / 2 + (l_via)))
        r_region = pya.Region(pya.Box((posx + w_dbu / 2) - w_via, posy - l_dbu / 2, posx + w_dbu / 2, posy + l_dbu / 2))
        t_region = pya.Region(pya.Box(posx - w_dbu / 2, posy + l_dbu / 2 - (l_via), posx + w_dbu / 2, posy + l_dbu / 2))
        l_region = pya.Region(pya.Box((posx - w_dbu / 2) + w_via, posy - l_dbu / 2, posx - w_dbu / 2, posy + l_dbu / 2))
        tot_region = b_region + r_region + t_region + l_region
        tot_region.round_corners(0, 0, nr)
        # print region
        self.cell.shapes(sd).insert(tot_region)

        # Round via
        w_mar = int(((175 + 20) / 2) / 20)
        l_mar = int(175 / 2 / 20)

        for i in range(w_mar):
            i = i / self.layout.dbu

            # bottom line
            # square region
            # positive loop
            square_region = pya.Region(pya.Box(posx - 7.5 / self.layout.dbu + 20 * i, posy - l_dbu / 2,\
                posx + 7.5 / self.layout.dbu + 20 * i, posy - l_dbu / 2 + ((l_via - (\
                15 / self.layout.dbu)) / 2) + 15 / self.layout.dbu))
            # print region
            self.cell.shapes(gc).insert(square_region)
            # negative loop
            square_region = pya.Region(pya.Box(posx - 7.5 / self.layout.dbu - 20 * i, posy - l_dbu / 2,\
                posx + 7.5 / self.layout.dbu - 20 * i, posy - l_dbu / 2 + ((l_via - (\
                15 / self.layout.dbu)) / 2) + 15 / self.layout.dbu))
            # print region
            self.cell.shapes(gc).insert(square_region)

            # circle
            # positive loop
            circle_region = pya.Region(pya.Box(posx - 2.5 / self.layout.dbu + 20 * i, posy - l_dbu / 2 + (\
                (l_via - (15 / self.layout.dbu)) / 2) + 5 / self.layout.dbu,\
                posx + 2.5 / self.layout.dbu + 20 * i, posy - l_dbu / 2 + ((l_via - (\
                15 / self.layout.dbu)) / 2) + 10 / self.layout.dbu)).round_corners(0, w_via_cir / 2, nr)
            # print region
            self.cell.shapes(pv).insert(circle_region)
            # negative loop
            circle_region = pya.Region(pya.Box(posx - 2.5 / self.layout.dbu - 20 * i, posy - l_dbu / 2 + (\
                (l_via - (15 / self.layout.dbu)) / 2) + 5 / self.layout.dbu,\
                posx + 2.5 / self.layout.dbu - 20 * i, posy - l_dbu / 2 + ((l_via - (\
                15 / self.layout.dbu)) / 2) + 10 / self.layout.dbu)).round_corners(0, w_via_cir / 2, nr)
            # print region
            self.cell.shapes(pv).insert(circle_region)

            # top line
            # square region
            # positive loop
            square_region = pya.Region(pya.Box(posx - 7.5 / self.layout.dbu + 20 * i, posy + l_dbu / 2,\
                posx + 7.5 / self.layout.dbu + 20 * i, posy + l_dbu / 2 - ((l_via - (\
                15 / self.layout.dbu)) / 2) - 15 / self.layout.dbu))
            # print region
            self.cell.shapes(gc).insert(square_region)
            # negative loop
            square_region = pya.Region(pya.Box(posx - 7.5 / self.layout.dbu - 20 * i,\
                posy + l_dbu / 2, posx + 7.5 / self.layout.dbu - 20 * i,\
                posy + l_dbu / 2 - ((l_via - (15 / self.layout.dbu)) / 2) - 15 / self.layout.dbu))
            # print region
            self.cell.shapes(gc).insert(square_region)

            # circle region
            # positive loop
            circle_region = pya.Region(pya.Box(posx - 2.5 / self.layout.dbu + 20 * i, posy + l_dbu / 2 - (\
                (l_via - (15 / self.layout.dbu)) / 2) - 5 / self.layout.dbu,\
                posx + 2.5 / self.layout.dbu + 20 * i, posy + l_dbu / 2 - ((l_via - (\
                15 / self.layout.dbu)) / 2) - 10 / self.layout.dbu)).round_corners(0, w_via_cir / 2, nr)
            # print region
            self.cell.shapes(pv).insert(circle_region)
            # negative loop
            circle_region = pya.Region(pya.Box(posx - 2.5 / self.layout.dbu - 20 * i, posy + l_dbu / 2 - (\
                (l_via - (15 / self.layout.dbu)) / 2) - 5 / self.layout.dbu,\
                posx + 2.5 / self.layout.dbu - 20 * i, posy + l_dbu / 2 - ((l_via - (\
                15 / self.layout.dbu)) / 2) - 10 / self.layout.dbu)).round_corners(0, w_via_cir / 2, nr)
            # print region
            self.cell.shapes(pv).insert(circle_region)

        for i in range(l_mar):
            i = i / self.layout.dbu

            # left line
            # square region
            # positive loop
            square_region = pya.Region(pya.Box(posx - w_dbu / 2, posy - 7.5 / self.layout.dbu + 20 * i,\
                posx - w_dbu / 2 + ((w_via - (15 / self.layout.dbu)) / 2) + 15 / self.layout.dbu,\
                posy + 7.5 / self.layout.dbu + 20 * i))
            # print region
            self.cell.shapes(gc).insert(square_region)
            # negative loop
            square_region = pya.Region(pya.Box(posx - w_dbu / 2, posy - 7.5 / self.layout.dbu - 20 * i,\
                posx - w_dbu / 2 + ((w_via - (15 / self.layout.dbu)) / 2) + 15 / self.layout.dbu,\
                posy + 7.5 / self.layout.dbu - 20 * i))
            # print region
            self.cell.shapes(gc).insert(square_region)

            # circle region
            # positive loop
            circle_region = pya.Region(pya.Box(posx - w_dbu / 2 + ((w_via - (15 / self.layout.dbu)) / 2) + \
                5 / self.layout.dbu, posy - 2.5 / self.layout.dbu + 20 * i,\
                posx - w_dbu / 2 + ((w_via - (15 / self.layout.dbu)) / 2) + 10 / self.layout.dbu,\
                posy + 2.5 / self.layout.dbu + 20 * i)).round_corners(0, l_via_cir / 2, nr)
            # print region
            self.cell.shapes(pv).insert(circle_region)
            # negative loop
            circle_region = pya.Region(pya.Box(posx - w_dbu / 2 + ((w_via - (15 / self.layout.dbu)) / 2) + \
                5 / self.layout.dbu, posy - 2.5 / self.layout.dbu - 20 * i,\
                posx - w_dbu / 2 + ((w_via - (15 / self.layout.dbu)) / 2) + 10 / self.layout.dbu,\
                posy + 2.5 / self.layout.dbu - 20 * i)).round_corners(0, l_via_cir / 2, nr)
            # print region
            self.cell.shapes(pv).insert(circle_region)

            # right line
            # square region
            # positive loop
            square_region = pya.Region(pya.Box(posx + w_dbu / 2, posy - 7.5 / self.layout.dbu + 20 * i,\
                posx + w_dbu / 2 - ((w_via - (15 / self.layout.dbu)) / 2) - 15 / self.layout.dbu,\
                posy + 7.5 / self.layout.dbu + 20 * i))
            # print region
            self.cell.shapes(gc).insert(square_region)
            # negative loop
            square_region = pya.Region(pya.Box(posx + w_dbu / 2, posy - 7.5 / self.layout.dbu - 20 * i,\
                posx + w_dbu / 2 - ((w_via - (15 / self.layout.dbu)) / 2) - 15 / self.layout.dbu,\
                posy + 7.5 / self.layout.dbu - 20 * i))
            # print region
            self.cell.shapes(gc).insert(square_region)

            # circle
            # positive loop
            circle_region = pya.Region(pya.Box(posx + w_dbu / 2 - ((w_via - (15 / self.layout.dbu)) / 2) - \
                5 / self.layout.dbu, posy - 2.5 / self.layout.dbu + 20 * i,\
                posx + w_dbu / 2 - ((w_via - (15 / self.layout.dbu)) / 2) - 10 / self.layout.dbu,\
                posy + 2.5 / self.layout.dbu + 20 * i)).round_corners(0, l_via_cir / 2, nr)
            # print region
            self.cell.shapes(pv).insert(circle_region)
            # negative loop
            circle_region = pya.Region(pya.Box(posx + w_dbu / 2 - ((w_via - (15 / self.layout.dbu)) / 2) - \
                5 / self.layout.dbu, posy - 2.5 / self.layout.dbu - 20 * i,\
                posx + w_dbu / 2 - ((w_via - (15 / self.layout.dbu)) / 2) - 10 / self.layout.dbu,\
                posy + 2.5 / self.layout.dbu - 20 * i)).round_corners(0, l_via_cir / 2, nr)
            # print region
            self.cell.shapes(pv).insert(circle_region)
  
  def transistor(self, level, x, y, w_i, n_i, l_i, bg, load, Int_Con, ov_l, ov_r, out):
    # Other design rules and other "fixed" variables 
    # Define layer names
    # Assign layers using list comprehension
    layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
    # Unpack layers into variables
    txt, bm, bl, sd, gm, pv, gc, pv2 = layers

    # fetch the parameters
    dbu = self.layout.dbu # The variable dbu is assigned the value of the database unit represented in microns.
    nr = 128  # Number of points in a circle
    # Global variables
    metal_ov = self.o / dbu
    via = self.via / dbu
    via_ov = self.via_ov / dbu
    finger_sep = self.s / dbu
    PDN_S_dbu = self.PDN_S / dbu
    finger_width = self.fw / dbu
    gm_ov = self.gm_ov / dbu
    # Local variables
    ov_l /= dbu
    ov_r /= dbu
    bg_ov = metal_ov
    n = n_i
    channel_length = l_i / dbu
    channel_width_per_f = w_i / dbu
    posx = x / dbu
    posy = y / dbu
    round = 1 / dbu
    # Calculations 
    via_size = (via + 2 * via_ov)
    
    Top_Edge = posy + channel_width_per_f / 2 + metal_ov +\
         2 * finger_sep + finger_width + PDN_S_dbu  # Top edge of Cell
    Bottom_Edge = posy -(channel_width_per_f / 2 + metal_ov +\
        2 * finger_sep + finger_width + self.rail * finger_width + PDN_S_dbu) # Bottom edge of Cell
    VDD_B_E = Top_Edge  # VDD bottom edge
    VDD_T_E = VDD_B_E + (self.rail * finger_width) # VDD top edge
    VSS_B_E = Bottom_Edge # Vss top edge
    VSS_T_E = VSS_B_E + (self.rail * finger_width) # Vss bottom edge
        
    finger_length = finger_sep + channel_width_per_f + 2 * metal_ov # Correct

    # Create a region for a single finger with the given length and width
    single_finger_region = pya.Region(pya.Box(0, 0, finger_length, finger_width))
    
    # Move the single finger to the center of the bounding box
    single_finger_region.move(-single_finger_region.bbox().center())
    
    # Create an empty region for all fingers
    finger_region = pya.Region()
    
    # For each finger, create a new region by moving the single finger region horizontally by half the 
    # finger separation multiplied by -1 or 1 (depending on the index), and vertically by the finger + channel length
    for i in range(n + 1): # For each finger
        if i % 2 == 1:
            lr = 1
        else:
            lr = -1
        finger_region = finger_region + single_finger_region.moved(
            lr * (finger_sep / 2), (finger_width + channel_length) * i)
    # Centring the fingers
    finger_region.move(-finger_region.bbox().center())
    
    # Generating region for source backbone using pya.Box function and calculating its position with respect to finger_region bounding box
    source_backbone_region = pya.Region(pya.Box(
            0, 0,
            finger_width,
            (n - n % 2) * (finger_width + channel_length) + finger_width))
    source_backbone_region = source_backbone_region.moved(
            finger_region.bbox().left - finger_width, finger_region.bbox().bottom)
    
    # Generating region for drain backbone using pya.Box function and calculating its position with respect to finger_region bounding box
    drain_backbone_region = pya.Region(pya.Box(
            0, 0,
            finger_width,
            (n - 2 + n % 2) * (finger_width + channel_length) + finger_width))
    drain_backbone_region = drain_backbone_region.moved(
            finger_region.bbox().right,
            finger_region.bbox().top - drain_backbone_region.bbox().top\
                - (((n + 1) % 2) * (finger_width + channel_length)))

    source_drain_region = pya.Region()
    source_drain_region = source_drain_region + finger_region
    source_drain_region = source_drain_region + source_backbone_region
    source_drain_region = source_drain_region + drain_backbone_region
    source_drain_region.merge()
    source_drain_region.round_corners(round, round, nr)

    Left_Edge = posx + source_drain_region.bbox().bottom - finger_width #Left edge of Cell


    if (level == 0):
        rotation = pya.ICplxTrans(float (1), float(90), True, posx, posy)
    else:
        rotation = pya.ICplxTrans(float (1), float(90), False, posx, posy) 
     
    self.cell.shapes(sd).insert(source_drain_region, rotation)
    
    # Gate - Gate height calculations, Region creation and adding the region to the "gm" layer
    gate_height = (n) * channel_length + (n + 1) * finger_width
    gate_region = pya.Region(pya.Box(
        0,0,channel_width_per_f,gate_height + 2 * gm_ov)).round_corners(round, round, nr)
    
    gate_region.move(-pya.Box(0, 0, channel_width_per_f, gate_height + 2 * gm_ov).center()) # Centre the gate
    self.cell.shapes(gm).insert(gate_region, rotation)
    

    # Back gate layer
    vbg_cover = pya.Region(pya.Box(
        gate_region.bbox().left - (bg_ov + 2 * channel_length + finger_width),
        gate_region.bbox().bottom - bg_ov,
        gate_region.bbox().right + (bg_ov + 2 * channel_length + finger_width),
        gate_region.bbox().top + bg_ov
        )).round_corners(round, round, nr)

    self.cell.shapes(bm).insert(vbg_cover, rotation)
        
    # Passivation layer for Transistor
    # Drive transistors
    if load == False:
        # Back gate connection
        VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbg electrode
        self.cell.shapes(bm).insert(VBG_Ele_out)
        if level != 0:
            # If the lower via selected
            if out != 1:
                PV_Region = pya.Region(pya.Box(
                    gate_region.bbox().left,
                    gate_region.bbox().top,
                    gate_region.bbox().left + via_size,
                    gate_region.bbox().top-via_size
                    )).round_corners(via_size, via_size, nr)
                self.cell.shapes(gc).insert(PV_Region, rotation)
                self.cell.shapes(gm).insert(PV_Region, rotation)
                self.cell.shapes(pv).insert(PV_Region.sized(-via_ov), rotation)
            # If the upper via selected
            if out != 0:
                PV_Region = pya.Region(pya.Box(
                    gate_region.bbox().right,
                    gate_region.bbox().top,
                    gate_region.bbox().right - via_size,
                    gate_region.bbox().top - via_size
                    )).round_corners(via_size, via_size, nr)
                self.cell.shapes(gc).insert(PV_Region, rotation)
                self.cell.shapes(gm).insert(PV_Region, rotation)
                self.cell.shapes(pv).insert(PV_Region.sized(-via_ov), rotation)
        # Reversed tarnsistor
        if level == 0:
            # If the lower via selected
            if out != 1:
                PV_Region = pya.Region(pya.Box(
                    gate_region.bbox().left,
                    gate_region.bbox().bottom,
                    gate_region.bbox().left + via_size,
                    gate_region.bbox().bottom + via_size
                    )).round_corners(via_size, via_size, nr)
                self.cell.shapes(gc).insert(PV_Region, rotation)
                self.cell.shapes(gm).insert(PV_Region, rotation)
                self.cell.shapes(pv).insert(PV_Region.sized(-via_ov), rotation)
            # If the upper via selected
            if out != 0:
                PV_Region = pya.Region(pya.Box(
                    gate_region.bbox().right,
                    gate_region.bbox().bottom,
                    gate_region.bbox().right - via_size,
                    gate_region.bbox().bottom + via_size
                    )).round_corners(via_size, via_size, nr)
                self.cell.shapes(gc).insert(PV_Region, rotation)
                self.cell.shapes(gm).insert(PV_Region, rotation)
                self.cell.shapes(pv).insert(PV_Region.sized(-via_ov), rotation)
    # Load transistors
    if load==True:
        if out != 1:
            # Gate via
            PV_Region_gm = pya.Region(pya.Box(
                gate_region.bbox().left,
                gate_region.bbox().top,
                gate_region.bbox().left + via_size,
                gate_region.bbox().top - via_size))
            self.cell.shapes(gc).insert(PV_Region_gm, rotation)
            self.cell.shapes(gm).insert(PV_Region_gm, rotation)      
            self.cell.shapes(pv).insert(
                PV_Region_gm.sized(-via_ov).round_corners(via_size, via_size, nr),
                rotation)

            # Back gate via
            PV_Region_bm = PV_Region_gm.move(0, via_size)
            self.cell.shapes(gc).insert(PV_Region_bm, rotation)
            self.cell.shapes(bm).insert(PV_Region_bm, rotation)      
            self.cell.shapes(pv).insert(
                PV_Region_bm.sized(-via_ov).round_corners(via_size, via_size, nr),
                rotation)

            # Output SD via
            PV_Region_sq_via = PV_Region_bm.move(via_size, bg_ov)
            self.cell.shapes(gc).insert(PV_Region_sq_via, rotation)
            self.cell.shapes(sd).insert(PV_Region_sq_via, rotation)
            self.cell.shapes(pv).insert(
                PV_Region_bm.sized(-via_ov).round_corners(via_size, via_size, nr),
                rotation)
            
            # SD to BG via
            sd_gc_via = pya.Region(pya.Box(
                PV_Region_sq_via.bbox().right,
                PV_Region_bm.bbox().top,
                PV_Region_sq_via.bbox().left - via_size,
                PV_Region_bm.bbox().bottom             
                )).round_corners(round, round, nr)
            self.cell.shapes(gc).insert(sd_gc_via,rotation)
        
        if out != 0:
            # Gate via
            PV_Region_gm = pya.Region(pya.Box(
                gate_region.bbox().right,
                gate_region.bbox().top,
                gate_region.bbox().right - via_size,
                gate_region.bbox().top - via_size))
            self.cell.shapes(gc).insert(PV_Region_gm, rotation)
            self.cell.shapes(gm).insert(PV_Region_gm, rotation)      
            self.cell.shapes(pv).insert(
                PV_Region_gm.sized(-via_ov).round_corners(via_size, via_size, nr),
                rotation)

            # Back gate via
            PV_Region_bm = PV_Region_gm.move(0, via_size)
            self.cell.shapes(gc).insert(PV_Region_bm, rotation)
            self.cell.shapes(bm).insert(PV_Region_bm, rotation)      
            self.cell.shapes(pv).insert(
                PV_Region_bm.sized(-via_ov).round_corners(via_size, via_size, nr),
                rotation)

            # Output SD via
            PV_Region_sq_via = PV_Region_bm.move(-via_size, bg_ov)
            self.cell.shapes(gc).insert(PV_Region_sq_via, rotation)
            self.cell.shapes(sd).insert(PV_Region_sq_via, rotation)
            self.cell.shapes(pv).insert(
                PV_Region_bm.sized(-via_ov).round_corners(via_size, via_size, nr),
                rotation)

            # SD to BG via
            sd_gc_via = pya.Region(pya.Box(
                PV_Region_sq_via.bbox().left,
                PV_Region_bm.bbox().top,
                PV_Region_sq_via.bbox().right + via_size,
                PV_Region_bm.bbox().bottom             
                )).round_corners(round, round, nr)
            self.cell.shapes(gc).insert(sd_gc_via, rotation)
      
    # Vdd and Vss Positions
    if level == 0 or level == 1:
        if level == 1:
            offset = n % 2 * (-1) * (finger_sep + finger_width)
        else:
            offset = 0
        bottom = drain_backbone_region.bbox().bottom + offset
        top = drain_backbone_region.bbox().top + offset
        vdd = pya.Region(pya.Box(posx + top, VDD_B_E - finger_sep - finger_width, posx + bottom, VDD_T_E))
        self.cell.shapes(sd).insert(vdd)

    elif level == 3:
        bottom = source_backbone_region.bbox().bottom
        top = source_backbone_region.bbox().top
        vss = pya.Region(pya.Box(posx - bottom, VSS_T_E + finger_sep + finger_width, posx - top, VSS_B_E))
        self.cell.shapes(sd).insert(vss)
        
    # Define variables
    right_edge = posx + source_drain_region.bbox().top + finger_width # Right edge of Cell
    vdd_box = pya.Box(Left_Edge - ov_l, VDD_B_E, right_edge + ov_r, VDD_T_E) # VDD rail box
    vss_box = pya.Box(Left_Edge - ov_l, VSS_B_E, right_edge + ov_r, VSS_T_E) # VSS rail box
    
    # Create Regions and insert into layout
    vdd_ele = pya.Region(vdd_box) # Create VDD rail region
    vss_ele = pya.Region(vss_box) # Create VSS rail region
    v_ele = vdd_ele + vss_ele # Add regions together to create combined voltage regions
    self.cell.shapes(sd).insert(v_ele) # Insert into cell shape in layout
    

    VBG_Ele = pya.Region(pya.Box(Left_Edge - ov_l, VDD_T_E, right_edge + ov_r, VDD_T_E - finger_width)) # Vgb rail
    self.cell.shapes(bm).insert(VBG_Ele)

    VDDTregion = pya.TextGenerator.default_generator().text\
        ("VDD", 0.001, 2*self.via).move(posx - gate_region.bbox().top, VDD_B_E)
    VSSTregion = pya.TextGenerator.default_generator().text\
        ("VSS", 0.001, 2*self.via).move(posx - gate_region.bbox().top, VSS_B_E)
    Tregion = VDDTregion + VSSTregion
    self.cell.shapes(sd).insert(Tregion)
    
    # Connection
    # Source to Gate
    if Int_Con == 1:
        # Lower output
        if out != 1:
            D1_D2 = pya.Polygon([
                pya.Point(posx - vbg_cover.bbox().top,
                    posy - gate_region.bbox().right + via_size),
                pya.Point(posx - vbg_cover.bbox().top,
                    posy + VSS_T_E + channel_length),
                pya.Point(posx - 2 * vbg_cover.bbox().top - gate_region.bbox().top,
                    posy + VSS_T_E + channel_length),
                pya.Point(posx - 2 * vbg_cover.bbox().top - gate_region.bbox().top,
                    posy + VSS_T_E + channel_length + finger_width),
                pya.Point(posx - vbg_cover.bbox().top - via_size,
                    posy + VSS_T_E + channel_length + finger_width),
                pya.Point(posx - vbg_cover.bbox().top - via_size,
                    posy - gate_region.bbox().right + via_size)
                ]).round_corners(round, round, nr)
            self.cell.shapes(sd).insert(D1_D2)
        
            # Out via connection
            PV_Region_sq = pya.Region(pya.Box(
                posx - vbg_cover.bbox().top,
                posy - gate_region.bbox().right + via_size,
                posx - vbg_cover.bbox().top - via_size,
                posy - gate_region.bbox().right)).round_corners(round, round, nr)
            self.cell.shapes(gc).insert(PV_Region_sq)
            self.cell.shapes(sd).insert(PV_Region_sq)
            self.cell.shapes(pv).insert(
                PV_Region_sq.sized(-via_ov).rounded_corners(via_size, via_size, nr))
            
            #Connection
            conn = pya.Region(pya.Box(
                PV_Region_sq.bbox().left,
                posy - gate_region.bbox().right + via_size,
                PV_Region_sq.bbox().left + metal_ov + 2 * via_size,
                posy - gate_region.bbox().right)).round_corners(round, round, nr)
            self.cell.shapes(gc).insert(conn)  
        # Higher output
        if out != 0:
            D1_D2 = pya.Polygon([
                pya.Point(posx - vbg_cover.bbox().top,
                    posy + gate_region.bbox().right - via_size),
                pya.Point(posx - vbg_cover.bbox().top,
                    posy + VDD_B_E - channel_length),
                pya.Point(posx - 2 * vbg_cover.bbox().top - gate_region.bbox().top,
                    posy + VDD_B_E - channel_length),
                pya.Point(posx - 2 * vbg_cover.bbox().top - gate_region.bbox().top,
                    posy + VDD_B_E - channel_length - finger_width),
                pya.Point(posx - vbg_cover.bbox().top - via_size,
                    posy + VDD_B_E - channel_length - finger_width),
                pya.Point(posx - vbg_cover.bbox().top - via_size,
                    posy + gate_region.bbox().right - via_size)
                ]).round_corners(round, round, nr)
            self.cell.shapes(sd).insert(D1_D2)

            # Out via connection
            PV_Region_sq = pya.Region(pya.Box(
                posx - vbg_cover.bbox().top,
                posy + gate_region.bbox().right - via_size,
                posx - vbg_cover.bbox().top - via_size,
                posy + gate_region.bbox().right)).round_corners(round, round, nr)
            self.cell.shapes(gc).insert(PV_Region_sq)
            self.cell.shapes(sd).insert(PV_Region_sq)
            self.cell.shapes(pv).insert(
                PV_Region_sq.sized(-via_ov).rounded_corners(via_size, via_size, nr))
    
            #Connection
            conn = pya.Region(pya.Box(
                PV_Region_sq.bbox().left,
                posy + gate_region.bbox().right - via_size,
                PV_Region_sq.bbox().left + metal_ov + 2 * via_size,
                posy + gate_region.bbox().right)).round_corners(round, round, nr)
            self.cell.shapes(gc).insert(conn)  

    #Source to Source
    if Int_Con == 100:
        D1_D2 = pya.Region(pya.Box(
            posx  + channel_length / 2 + finger_width,
            posy - source_drain_region.bbox().right,
            posx - 3 * channel_length / 2 - 2 * vbg_cover.bbox().top - finger_width,
            posy - source_drain_region.bbox().right + finger_width
            )).round_corners(round, round, nr)
        self.cell.shapes(sd).insert(D1_D2)

    #Source to Drain
    if Int_Con == 101:
        # Load
        if load == True:
            D1_D2 = pya.Polygon([
                pya.Point(posx + channel_length / 2 + finger_width,
                    posy + VDD_B_E - channel_length),
                pya.Point(posx - PV_Region_gm.bbox().top,
                    posy + VDD_B_E - channel_length),
                pya.Point(posx - PV_Region_gm.bbox().top,
                    posy + VSS_T_E + channel_length + finger_width),
                pya.Point(posx - PV_Region_gm.bbox().top - vbg_cover.bbox().top - finger_width - channel_length / 2,
                    posy + VSS_T_E + channel_length + finger_width),
                pya.Point(posx - PV_Region_gm.bbox().top - vbg_cover.bbox().top - finger_width - channel_length / 2,
                    posy + VSS_T_E + channel_length),
                pya.Point(posx - vbg_cover.bbox().top,
                    posy + VSS_T_E + channel_length),
                pya.Point(posx - vbg_cover.bbox().top,
                    posy + VDD_B_E - channel_length - finger_width),
                pya.Point(posx + channel_length / 2 + finger_width,
                    posy + VDD_B_E - channel_length - finger_width)
                ]).round_corners(round, round, nr)
            self.cell.shapes(sd).insert(D1_D2)
        # Drive
        if load == False:
            D1_D2 = pya.Polygon([
                pya.Point(posx + channel_length / 2 + finger_width,
                    posy + VDD_B_E - channel_length),
                pya.Point(posx - vbg_cover.bbox().top - finger_width,
                    posy + VDD_B_E - channel_length),
                pya.Point(posx - vbg_cover.bbox().top - finger_width,
                    posy + VSS_T_E + channel_length + finger_width),
                pya.Point(posx - 2 * vbg_cover.bbox().top - 2 * finger_width - channel_length / 2,
                    posy + VSS_T_E + channel_length + finger_width),
                pya.Point(posx - 2 * vbg_cover.bbox().top - 2 * finger_width - channel_length / 2,
                    posy + VSS_T_E + channel_length),
                pya.Point(posx - vbg_cover.bbox().top,
                    posy + VSS_T_E + channel_length),
                pya.Point(posx - vbg_cover.bbox().top,
                    posy + VDD_B_E - channel_length - finger_width),
                pya.Point(posx + channel_length / 2 + finger_width,
                    posy + VDD_B_E - channel_length - finger_width)
                ]).round_corners(round, round, nr)
            self.cell.shapes(sd).insert(D1_D2)
    
    #Drain to Source
    if (Int_Con == 110):
        D1_D2 = pya.Polygon([
            pya.Point(posx + channel_length / 2 + finger_width,
                posy + VDD_B_E - channel_length),
            pya.Point(posx - vbg_cover.bbox().top - finger_width,
                posy + VDD_B_E - channel_length),
            pya.Point(posx - vbg_cover.bbox().top - finger_width,
                posy + VSS_T_E + channel_length + finger_width),
            pya.Point(posx - 2 * vbg_cover.bbox().top - 2 * finger_width - channel_length / 2,
                posy + VSS_T_E + channel_length + finger_width),
            pya.Point(posx - 2 * vbg_cover.bbox().top - 2 * finger_width - channel_length / 2,
                posy + VSS_T_E + channel_length),
            pya.Point(posx - vbg_cover.bbox().top,
                posy + VSS_T_E + channel_length),
            pya.Point(posx - vbg_cover.bbox().top,
                posy + VDD_B_E - channel_length - finger_width),
            pya.Point(posx + channel_length / 2 + finger_width,
                posy + VDD_B_E - channel_length - finger_width),
            ]).round_corners(round, round, nr)
        self.cell.shapes(sd).insert(D1_D2)

    #Drain to Drain
    if (Int_Con == 111):
        D1_D2 = pya.Region(pya.Box(
            posx - channel_length / 2,
            posy + VDD_B_E - channel_length - finger_width,
            posx - channel_length / 2 - 2 * finger_width - 2 * vbg_cover.bbox().top,
            posy + VDD_B_E - channel_length
            )).round_corners(round, round, nr)
        self.cell.shapes(sd).insert(D1_D2)
        
  def impl(self):
    #Definitions
    dbu = self.layout.dbu
    ov = self.o
    ov_dbu = ov / dbu
    via = self. via
    w_d = self.w
    out = self.vias
    path_width = ov + via
    path_width_dbu = path_width/dbu
    finger_width = self.fw
    finger_width_dbu = finger_width / dbu
    finger_sep = self.s
    finger_sep_dbu = finger_sep / dbu
    path_step = path_width_dbu + finger_sep_dbu
    right_ov_load = path_width + finger_sep
    # Define layer names
    # Assign layers using list comprehension
    layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
    # Unpack layers into variables
    txt, bm, bl, sd, gm, pv, gc, pv2 = layers
    q = self.l_d / self.l_l
    p = int(self.r / q)
    y = 0
    Top_Edge = (y + w_d/2 + ov + 2*finger_sep + finger_width + self.PDN_S)/dbu  #Top edge of Cell
    Top_rail = Top_Edge + self.rail*finger_width_dbu/2
    Bottom_Edge = (y-(w_d/2 + ov + 2*finger_sep + finger_width + self.PDN_S))/dbu #Bottom edge of Cell
    Bottom_rail = Bottom_Edge - self.rail*finger_width_dbu/2
    x0 = -((self.n_d*self.l_d)+(self.n_d+1)*finger_width)/2 
    # x0 = 0
    d_x_0 = ((-2*x0) + finger_sep ) / 5
    d_x_1 = ((-2*x0) + 2*finger_sep + path_width) / 5
    d_x_100 = ((-2*x0) + finger_sep ) / 5
    d_x_101 = ((-2*x0) + 2*finger_sep + finger_width) / 5
    d_x_110 = ((-2*x0) + 2*finger_sep + finger_width) / 5
    d_x_111 = ((-2*x0) + 2*finger_sep) / 5

    l_x = (((p*self.n_d*self.l_l)+(p*self.n_d+1)*finger_width)/2 -x0\
        + 2.5*ov +2*via)/5
    Top_Path = (w_d/2 + ov + 2*self.s + finger_width - path_width/2)/dbu #Top edge of Cell
    # third_path = Top_Path / 3 
    third_path = y/dbu + path_width_dbu/2 + 3*ov_dbu/2 + via/2/dbu
    gate_connection = (w_d/2 - path_width/2)/dbu #Top gate of Cell
    gate_edge = ((self.n_d)*self.l_d+(self.n_d+1)*finger_width)/2
    gate_out = gate_connection + 4*path_step - path_width_dbu/2 + finger_sep_dbu
    gate_in = -gate_out
    #transistors implementation
    # self.transistor(level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth)
    # Levels: 
    # 1: connected to VDD
    # 2: Float
    # 3: connected to VSS
    # If Int_Con start with 0 nothing will happend, but for:
        # 001: Source to Gate
        # 100: Source to Source
        # 101: Source to Drain
        # 110: Drain to Source
        # 111: Drain to Drain
    #If out = 0, the via of the transistors are down
    #If out = 1, the via of the transistors are up
    # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)0
    self.transistor(self.pos, x0, y, w_d, self.n_d, self.l_d, True, self.load, self.int, 0, 0, out)
    #gates name
    iTregion = pya.TextGenerator.default_generator().text\
        ("IN", 0.001, 5).move((x0- gate_edge)/ dbu, -Top_Path - 25 / dbu)
    self.cell.shapes(txt).insert(iTregion)

    # Pads
    if(self.pad):
        
        list_a = [-400, 0, 400]
        list_b = [-200, 200]
        for i in list_a:
            for j in list_b:
                self.create_pad(i, j)
        
        # Vdd connection
        vdd = pya.Path([
            pya.Point((list_a[0]+80)/dbu, (list_b[1])/dbu),
            pya.Point((list_a[0]+80)/dbu, Top_rail),
            pya.Point((x0-gate_edge + (via + ov)/2)/dbu, Top_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vdd)

        # Vss connection
        vss = pya.Path([
            pya.Point((list_a[2]-80)/dbu, (list_b[0])/dbu),
            pya.Point((list_a[2]-80)/dbu, Bottom_rail),
            pya.Point((x0-gate_edge + (via + ov)/2)/dbu, Bottom_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vss)

        # Vbg connection
        vbg = pya.Path([
            pya.Point((list_a[1])/dbu, (list_b[1])/dbu),
            pya.Point((list_a[1])/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2),
            pya.Point((x0-gate_edge + (via + ov)/2)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2),
            pya.Point((x0-gate_edge + (via + ov)/2)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu),
        ],finger_width_dbu)
        self.cell.shapes(bm).insert(vbg)

        # Vin connection
        vin = pya.Path([
            pya.Point((list_a[0]+80)/dbu, (list_b[0])/dbu),
            pya.Point((list_a[0]+80)/dbu, gate_in),
            pya.Point((x0-gate_edge + (via + ov)/2)/dbu, gate_in),
            pya.Point((x0-gate_edge + (via + ov)/2)/dbu, Bottom_Edge),
        ],path_width_dbu)
        self.cell.shapes(gc).insert(vin)

        # Vout connection
        vout = pya.Path([
            pya.Point((list_a[2]-80)/dbu, (list_b[1])/dbu),
            pya.Point((list_a[2]-80)/dbu, gate_out),
            pya.Point((x0-gate_edge + (via + ov)/2)/dbu, gate_out),
            pya.Point((x0-gate_edge + (via + ov)/2)/dbu, Top_Edge),
        ],path_width_dbu)
        self.cell.shapes(gc).insert(vout)

    #name
    name = pya.TextGenerator.default_generator().text\
        ("Trans", 0.001, 10).move((x0 - 15)/ dbu, -85 / dbu)
    self.cell.shapes(gc).insert(name)
    self.cell.shapes(sd).insert(name)
    self.cell.shapes(bm).insert(name)
    name = pya.TextGenerator.default_generator().text\
        (self.name, 0.001, 10).move((x0 - 15) / dbu, -95 / dbu)
    self.cell.shapes(gc).insert(name)
    self.cell.shapes(sd).insert(name)
    self.cell.shapes(bm).insert(name)

  def produce_impl(self):
    
    self.impl()