# $autorun
# -*- coding: utf-8 -*-
"""
@author: Ashkan
Email:ashkan.rezaee@uab.cat
"""

"""
Trasitor without VDD and VSS connection. Uses a modified version of transistor code on other cells. 
"""

from sys import path
from typing import Sized
import pya
import math

class Transistor(pya.PCellDeclarationHelper):
  """
  The PCell declaration for the Transistor
  """

  def __init__(self):

    # Important: initialize the super class
    super(Transistor, self).__init__()

    # declare the parameters
    self.param("w_d", self.TypeDouble, "Transistor Width", default = 90.0)
    self.param("mode", self.TypeInt, "Mode of connection to VDD or VSS", default = 2)
    self.param("n_d", self.TypeInt, "Number of Drive Fingers", default = 1)
    self.param("l_d", self.TypeDouble, "Drive Length", default = 2.5)
    self.param("l_l", self.TypeDouble, "Load Length", default = 2.5)
    self.param("r", self.TypeDouble, "Ratio", default = 1)
    self.param("o", self.TypeDouble, "Gate Overlap", default = 5)
    self.param("fw", self.TypeDouble, "Finger Width", default = 3.5)
    self.param("s", self.TypeDouble, "Finger Separation", default = 2.5)
    self.param("via", self.TypeDouble, "via size", default = 2.5)
    self.param("rail", self.TypeDouble, "rail to finger width ratio", default = 3)
    self.param("PDN_S", self.TypeDouble, "Extra distance for PDN", default = 0)
   #self.param("pad", self.TypeBoolean, "Pads", default = False)
    self.param("name", self.TypeString, "name", default = "ParametricTransistor")
    self.param("Int_Con", self.TypeInt, "Interconnection", default = 0)
    self.param("out", self.TypeInt, "External connectivity", default = 2) #0 to down, #1 to up, 2 to both.  
    self.param("load", self.TypeBoolean, "Connection with Load ", default = False)
    self.param("bg", self.TypeBoolean, "bg ", default = False)  #Legacy call. Does nothing in this version of the code. 
    self.param("ovl", self.TypeDouble, "Overlap Left", default = 0.0)
    self.param("ovr", self.TypeDouble, "Overlap Right", default = 0.0)

  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "STD Transistor :(ratio=" + str((self.r)) + ",Width= "+ str((self.w_d)) + " " + str((self.n_d)) +  "Mode:" + str((self.mode))  + ")"

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
       # bm = self.layout.layer(1, 0)
       # bl = self.layout.layer(2, 0)
       # sd = self.layout.layer(3, 0)
       # gm = self.layout.layer(4, 0)
       # pv = self.layout.layer(6, 0)
       # gc = self.layout.layer(7, 0)
       # pv2 = self.layout.layer(9, 0)
        # Define layer names - new version

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
    # Other design rules and other "fixed" variables, such as layer identifiers, path widths, via hole sizes, etc.
    nr = 128 # Number of points in a circle
    #bm = self.layout.layer(1,0)
    #bl = self.layout.layer(2,0)
    #sd = self.layout.layer(3,0)
    #gm = self.layout.layer(4,0)
    #pv = self.layout.layer(6,0)
    #gc = self.layout.layer(7,0)
    #pv2= self.layout.layer(9,0)
    #gc2= self.layout.layer(10,0)
    # New version of layer definition below
    # Define layer names
    # Assign layers using list comprehension
    layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
    # Unpack layers into variables
    txt, bm, bl, sd, gm, pv, gc, pv2 = layers

    # fetch the parameters
    dbu = self.layout.dbu # How large the database unit is in microns (usually 0.001, i.e. 1 nm)
    ov_l = ov_l / dbu
    ov_r = ov_r / dbu
    gate_overlap = self.o / dbu
    n = n_i
    bg_ov = gate_overlap/2
    channel_length = l_i / dbu
    finger_width = self.fw / dbu
    channel_width_per_f = w_i / dbu
    finger_sep = self.s / dbu
    PDN_S_dbu = self.PDN_S / dbu
    PV_BOX = self.via / dbu
    EL_W = (gate_overlap + PV_BOX)
    In_Box = (EL_W - PV_BOX) / 2
    Top_Edge = y/dbu + channel_width_per_f/2 + gate_overlap + 2*finger_sep + finger_width + PDN_S_dbu  #Top edge of Cell
    Bottom_Edge = y/dbu -(channel_width_per_f/2 + gate_overlap + 2*finger_sep + finger_width + self.rail * finger_width + PDN_S_dbu) #Bottom edge of Cell
    VDD_B_E = Top_Edge  #VDD bottom edge
    VDD_T_E = VDD_B_E + (self.rail * finger_width) #VDD top edge
    VSS_B_E = Bottom_Edge #Vss top edge
    VSS_T_E = VSS_B_E + (self.rail * finger_width) ##Vss bottom edge
        
    finger_length = finger_sep+channel_width_per_f+2*gate_overlap # Correct

    single_finger_region = pya.Region(pya.Box(0,0,finger_length,finger_width))
    single_finger_region.move(-single_finger_region.bbox().center())
    finger_region = pya.Region()
    for i in range(n+1): # For each finger
        if i%2 == 1:
            lr=1
        else:
            lr=-1
        finger_region=finger_region + single_finger_region.moved(lr*\
            (finger_sep/2),(finger_width+channel_length)*i)

    finger_region.move(-finger_region.bbox().center()) # Centre the fingers
    
    source_backbone_region = pya.Region(pya.Box(0, 0, finger_width,(n - \
        n%2)*(finger_width+channel_length)+finger_width))
    source_backbone_region = source_backbone_region.moved(\
        finger_region.bbox().left-finger_width,finger_region.bbox().bottom)

    drain_backbone_region = pya.Region(pya.Box(0,0,finger_width,(n-2 + n%2)\
        *(finger_width+channel_length)+finger_width))
    drain_backbone_region = drain_backbone_region.moved(\
        finger_region.bbox().right, \
        finger_region.bbox().top-drain_backbone_region.bbox().top-(((n+1)%2)*\
        (finger_width+channel_length)))

    source_drain_region = pya.Region()
    source_drain_region = source_drain_region + finger_region
    source_drain_region = source_drain_region + source_backbone_region
    source_drain_region = source_drain_region + drain_backbone_region
    
    Left_Edge = x/dbu + source_drain_region.bbox().bottom - finger_width #Left edge of Cell
    posx = Left_Edge - source_drain_region.bbox().bottom + finger_width
    posy = y/dbu

    if (level ==0):
        rotation = pya.ICplxTrans(float (1), float(90), True, posx, posy)
    else:
        rotation = pya.ICplxTrans(float (1), float(90), False, posx, posy)

    source_drain_region.merge()
    self.cell.shapes(sd).insert(source_drain_region, rotation)
    
    # Gate - Gate height calculations, Region creation and adding the region to the "gm" layer
    gate_height = (n)*channel_length+(n+1)*finger_width
    gate_region = pya.Region(pya.Box(0,0,channel_width_per_f,gate_height))

    gate_region.move(-pya.Box(0,0, channel_width_per_f, \
        gate_height).center()) # Centre the gate
    self.cell.shapes(gm).insert(gate_region, rotation)
    
    # Passivation layer for Transistor
    if (load==False and level != 0):
        if (out != 1):
            PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().left, gate_region.bbox().top,\
                gate_region.bbox().left+EL_W, gate_region.bbox().top-EL_W))
            self.cell.shapes(gc).insert(PV_Region_sq, rotation)
            self.cell.shapes(gm).insert(PV_Region_sq, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
                PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)
            #back gate layer
            vbg_cover = pya.Region(source_drain_region.bbox()).sized(bg_ov)
            self.cell.shapes(bm).insert(vbg_cover, rotation)        
            #back gate connection
            ##VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
            ##self.cell.shapes(bm).insert(VBG_Ele_out)
        if (out != 0):
            PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().right, gate_region.bbox().top,\
                gate_region.bbox().right-EL_W, gate_region.bbox().top-EL_W))
            self.cell.shapes(gc).insert(PV_Region_sq, rotation)
            self.cell.shapes(gm).insert(PV_Region_sq, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
                PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)
            #back gate layer
            vbg_cover = pya.Region(source_drain_region.bbox()).sized(bg_ov)
            self.cell.shapes(bm).insert(vbg_cover, rotation)        
            #back gate connection
            ##VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
            ##self.cell.shapes(bm).insert(VBG_Ele_out)

    if (load==False and level == 0):
        if (out != 1):
            PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().left, gate_region.bbox().bottom,\
                gate_region.bbox().left+EL_W, gate_region.bbox().bottom+EL_W))
            self.cell.shapes(gc).insert(PV_Region_sq, rotation)
            self.cell.shapes(gm).insert(PV_Region_sq, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
                PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))       
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)
            #back gate layer
            vbg_cover = pya.Region(source_drain_region.bbox()).sized(bg_ov)
            self.cell.shapes(bm).insert(vbg_cover, rotation)
            #back gate connection
            ##VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
            ##self.cell.shapes(bm).insert(VBG_Ele_out)
        if (out != 0):
            PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().right, gate_region.bbox().bottom,\
            gate_region.bbox().right-EL_W, gate_region.bbox().bottom+EL_W))
            self.cell.shapes(gc).insert(PV_Region_sq, rotation)
            self.cell.shapes(gm).insert(PV_Region_sq, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
                PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))       
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)
            #back gate layer
            vbg_cover = pya.Region(source_drain_region.bbox()).sized(bg_ov)
            self.cell.shapes(bm).insert(vbg_cover, rotation)
            #back gate connection
            ##VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
            ##self.cell.shapes(bm).insert(VBG_Ele_out)

    if (load==True):
        if (out != 1):
            #gate via
            PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().left, gate_region.bbox().top,\
                gate_region.bbox().left+EL_W, gate_region.bbox().top-EL_W))
            self.cell.shapes(gc).insert(PV_Region_sq, rotation)
            self.cell.shapes(gm).insert(PV_Region_sq, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
                PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))       
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)

            #back gate via
            PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().left, gate_region.bbox().top+EL_W,\
                gate_region.bbox().left+EL_W, gate_region.bbox().top))
            self.cell.shapes(gc).insert(PV_Region_sq, rotation)
            self.cell.shapes(bm).insert(PV_Region_sq, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
                PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))       
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)

            #Output via
            PV_Region_sq_via = pya.Region(pya.Box(PV_Region_sq.bbox().right, PV_Region_sq.bbox().top+EL_W,\
                PV_Region_sq.bbox().right-EL_W, PV_Region_sq.bbox().top))
            self.cell.shapes(gc).insert(PV_Region_sq_via, rotation)
            self.cell.shapes(sd).insert(PV_Region_sq_via, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq_via.bbox().left + In_Box, PV_Region_sq_via.bbox().bottom + In_Box,\
                PV_Region_sq_via.bbox().right - In_Box, PV_Region_sq_via.bbox().top - In_Box))       
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)

        #back gate layer
        # vbg_cover = pya.Region(source_drain_region.bbox()).sized(bg_ov)
        vbg_cover = pya.Region(pya.Box(source_drain_region.bbox().left - bg_ov, source_drain_region.bbox().bottom - bg_ov,\
            source_drain_region.bbox().right + bg_ov, gate_region.bbox().top+EL_W))
        self.cell.shapes(bm).insert(vbg_cover, rotation)
        
        if (out != 0):
            #gate via
            PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().right, gate_region.bbox().top,\
                gate_region.bbox().right-EL_W, gate_region.bbox().top-EL_W))
            self.cell.shapes(gc).insert(PV_Region_sq, rotation)
            self.cell.shapes(gm).insert(PV_Region_sq, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
                PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))       
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)

            #back gate via
            PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().right, gate_region.bbox().top+EL_W,\
                gate_region.bbox().right-EL_W, gate_region.bbox().top))
            self.cell.shapes(gc).insert(PV_Region_sq, rotation)
            self.cell.shapes(bm).insert(PV_Region_sq, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
                PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))       
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)

            #Output via
            PV_Region_sq_via = pya.Region(pya.Box(PV_Region_sq.bbox().right, PV_Region_sq.bbox().top+EL_W,\
                PV_Region_sq.bbox().right-EL_W, PV_Region_sq.bbox().top))
            self.cell.shapes(gc).insert(PV_Region_sq_via, rotation)
            self.cell.shapes(sd).insert(PV_Region_sq_via, rotation)
            PV_Region = pya.Region(pya.Box(PV_Region_sq_via.bbox().left + In_Box, PV_Region_sq_via.bbox().bottom + In_Box,\
                PV_Region_sq_via.bbox().right - In_Box, PV_Region_sq_via.bbox().top - In_Box))       
            PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
            self.cell.shapes(pv).insert(PV_Region, rotation)

            #back gate layer
            # vbg_cover = pya.Region(source_drain_region.bbox()).sized(bg_ov)
            vbg_cover = pya.Region(pya.Box(source_drain_region.bbox().left - bg_ov, source_drain_region.bbox().bottom - bg_ov,\
                source_drain_region.bbox().right + bg_ov, gate_region.bbox().top+EL_W))
            self.cell.shapes(bm).insert(vbg_cover, rotation)
      
    #Positions
    if (level == 0):
        vdd0 = pya.Region(pya.Box(posx - drain_backbone_region.bbox().top, VDD_B_E - finger_sep\
            , posx + drain_backbone_region.bbox().top, VDD_T_E))
        self.cell.shapes(sd).insert(vdd0)
    if (level == 1):
        vdd1 = pya.Region(pya.Box(posx - drain_backbone_region.bbox().top, VDD_B_E - finger_sep\
            , posx + drain_backbone_region.bbox().top, VDD_T_E))
        self.cell.shapes(sd).insert(vdd1)
    if (level == 3):
        vss = pya.Region(pya.Box(posx - source_backbone_region.bbox().bottom, VSS_T_E + finger_sep\
            , posx - source_backbone_region.bbox().top, VSS_B_E))
        self.cell.shapes(sd).insert(vss)
        
    Right_Edge = posx + source_drain_region.bbox().top + finger_width #Right edge of Cell
    if(level == 1):
     VDD_Ele = pya.Region(pya.Box(Left_Edge - ov_l, VDD_B_E, Right_Edge + ov_r, VDD_T_E)) # VDD rail
     V_Ele = VDD_Ele
    if(level == 3):
     VSS_Ele = pya.Region(pya.Box(Left_Edge - ov_l, VSS_B_E, Right_Edge + ov_r, VSS_T_E)) # VSS rail
     V_Ele = VSS_Ele
    #V_Ele = VDD_Ele + VSS_Ele #Old version did not use if levels here. 
    if (level != 2): #it is not a flota cell
        self.cell.shapes(sd).insert(V_Ele) #We do not want to create a VDD or VSS in this cells. 
    
    if (level != 2): #it is not a flota cell
        VBG_Ele = pya.Region(pya.Box(Left_Edge - ov_l, VDD_T_E, Right_Edge + ov_r, VDD_T_E - finger_width)) # Vgb rail
        self.cell.shapes(bm).insert(VBG_Ele)
        #This rail will be usefull
        VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
        self.cell.shapes(bm).insert(VBG_Ele_out)
        #Care with the order. 

    #VDDTregion = pya.TextGenerator.default_generator().text\
    #    ("VDD", 0.001, 2*self.via).move(posx - PV_BOX, VDD_B_E)
    #VSSTregion = pya.TextGenerator.default_generator().text\
    #    ("VSS", 0.001, 2*self.via).move(posx - PV_BOX, VSS_B_E)
    #Tregion = VDDTregion + VSSTregion
    #if (level != 2): #it is not a flota cell
       # self.cell.shapes(sd).insert(Tregion)
    
    #Connection
    #Source to Gate
    if (Int_Con == 1 and out != 1):
        D1_D2 = pya.Polygon([
            pya.Point(x/dbu - gate_region.bbox().top - bg_ov,\
                      posy + source_drain_region.bbox().left + finger_width + finger_sep + bg_ov+EL_W),\
            pya.Point(x/dbu - gate_region.bbox().top-bg_ov,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - bg_ov - finger_width ,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - bg_ov - finger_width ,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-bg_ov-EL_W,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-bg_ov-EL_W,\
                      posy + source_drain_region.bbox().left + finger_width + finger_sep + bg_ov+EL_W),\
            ])
        self.cell.shapes(sd).insert(D1_D2)

        #via connection
        PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().left, gate_region.bbox().top+bg_ov,\
            gate_region.bbox().left+EL_W, gate_region.bbox().top))
        self.cell.shapes(gc).insert(PV_Region_sq, rotation)

        #Output via
        PV_Region_sq_via = pya.Region(pya.Box(PV_Region_sq.bbox().right, PV_Region_sq.bbox().top+EL_W,\
            PV_Region_sq.bbox().right-EL_W, PV_Region_sq.bbox().top))
        self.cell.shapes(gc).insert(PV_Region_sq_via, rotation)
        self.cell.shapes(sd).insert(PV_Region_sq_via, rotation)
        PV_Region = pya.Region(pya.Box(PV_Region_sq_via.bbox().left + In_Box, PV_Region_sq_via.bbox().bottom + In_Box,\
            PV_Region_sq_via.bbox().right - In_Box, PV_Region_sq_via.bbox().top - In_Box))       
        PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
        self.cell.shapes(pv).insert(PV_Region, rotation)

    if (Int_Con == 1 and out != 0):
        D1_D2 = pya.Polygon([
            pya.Point(x/dbu - gate_region.bbox().top-bg_ov ,\
                      posy + source_drain_region.bbox().right - (finger_width + finger_sep + gate_overlap)),\
            pya.Point(x/dbu - gate_region.bbox().top-bg_ov,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - bg_ov - finger_width ,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - bg_ov - finger_width ,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-bg_ov-EL_W,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-bg_ov-EL_W,\
                      posy + source_drain_region.bbox().right - (finger_width + finger_sep + gate_overlap)),\
            ])
        self.cell.shapes(sd).insert(D1_D2)

        #via connection
        PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().right, gate_region.bbox().top+bg_ov,\
            gate_region.bbox().right-EL_W, gate_region.bbox().top))
        self.cell.shapes(gc).insert(PV_Region_sq, rotation)

        #Output via
        PV_Region_sq_via = pya.Region(pya.Box(PV_Region_sq.bbox().right, PV_Region_sq.bbox().top+EL_W,\
            PV_Region_sq.bbox().right-EL_W, PV_Region_sq.bbox().top))
        self.cell.shapes(gc).insert(PV_Region_sq_via, rotation)
        self.cell.shapes(sd).insert(PV_Region_sq_via, rotation)
        PV_Region = pya.Region(pya.Box(PV_Region_sq_via.bbox().left + In_Box, PV_Region_sq_via.bbox().bottom + In_Box,\
            PV_Region_sq_via.bbox().right - In_Box, PV_Region_sq_via.bbox().top - In_Box))       
        PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
        self.cell.shapes(pv).insert(PV_Region, rotation)

    #Source to Source
    if (Int_Con == 100):
        D1_D2 = pya.Region(pya.Box(x/dbu + channel_length/2 + finger_width, posy - source_drain_region.bbox().right,\
            x/dbu - n*channel_length + channel_length/2 - (n+1)*finger_width - 2*finger_sep, posy - \
            source_drain_region.bbox().right + finger_width))
        self.cell.shapes(sd).insert(D1_D2)
    #Source to Drain Load
    if (Int_Con == 101 and load == True):
        D1_D2 = pya.Polygon([
            pya.Point(x/dbu - channel_length/2, posy + source_drain_region.bbox().right - finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-EL_W ,\
                      posy + source_drain_region.bbox().right - finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-EL_W,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - bg_ov - finger_width ,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - bg_ov - finger_width ,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W,\
                      posy + source_drain_region.bbox().right),\
            pya.Point(x/dbu - channel_length/2 ,\
                      posy + source_drain_region.bbox().right),
            ])
        self.cell.shapes(sd).insert(D1_D2)

    #Source to Drain 
    if (Int_Con == 101 and load == False):
        D1_D2 = pya.Polygon([
            pya.Point(x/dbu - channel_length/2, posy + source_drain_region.bbox().right - finger_width),\
            pya.Point(x/dbu - source_drain_region.bbox().top - finger_sep,\
                      posy + source_drain_region.bbox().right - finger_width),\
            pya.Point(x/dbu - source_drain_region.bbox().top - finger_sep,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - source_drain_region.bbox().top - 2*finger_sep - 2*finger_width,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - source_drain_region.bbox().top - 2*finger_sep - 2*finger_width,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - source_drain_region.bbox().top - finger_sep -finger_width,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - source_drain_region.bbox().top - finger_sep -finger_width,\
                      posy + source_drain_region.bbox().right),\
            pya.Point(x/dbu - channel_length/2 ,\
                      posy + source_drain_region.bbox().right),
            ])
        self.cell.shapes(sd).insert(D1_D2)
    #Drain to Source
    if (Int_Con == 110):
        D1_D2 = pya.Polygon([
            pya.Point(x/dbu + channel_length/2 + finger_width, posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - source_drain_region.bbox().top - gate_overlap - finger_sep, \
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - source_drain_region.bbox().top - gate_overlap - finger_sep, \
                      posy + source_drain_region.bbox().right - finger_width),\
            pya.Point(x/dbu - source_drain_region.bbox().top -2* gate_overlap - 2*finger_sep - finger_width - channel_length, \
                      posy + source_drain_region.bbox().right - finger_width),\
            pya.Point(x/dbu - source_drain_region.bbox().top -2* gate_overlap - 2*finger_sep - finger_width - channel_length, \
                      posy + source_drain_region.bbox().right),\
            pya.Point(x/dbu - source_drain_region.bbox().top - gate_overlap, \
                      posy + source_drain_region.bbox().right),\
            pya.Point(x/dbu - source_drain_region.bbox().top - gate_overlap, \
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu + channel_length/2 + finger_width, 
                      posy + source_drain_region.bbox().left + finger_width),
            ])
        self.cell.shapes(sd).insert(D1_D2)
    #Drain to Drain
    if (Int_Con == 111):
        D1_D2 = pya.Region(pya.Box(x/dbu - channel_length/2, posy + source_drain_region.bbox().right,\
            x/dbu - source_drain_region.bbox().top - 2*gate_overlap - 2*finger_width - channel_length, posy + \
            source_drain_region.bbox().right - finger_width))
        self.cell.shapes(sd).insert(D1_D2)
    #    self.cell.shapes(sd).insert(D_In) #I do not where this came from. 

    #Drain Input
    if (Int_Con == 999):
        D_In = pya.Polygon([
            pya.Point(x/dbu, posy + source_drain_region.bbox().right),\
            pya.Point(x/dbu - gate_region.bbox().top -EL_W - bg_ov,\
                      posy + source_drain_region.bbox().right),\
            pya.Point(x/dbu - gate_region.bbox().top -EL_W - bg_ov,\
                      posy + source_drain_region.bbox().left + finger_width + finger_sep + gate_overlap),\
            pya.Point(x/dbu - gate_region.bbox().top - bg_ov,\
                      posy + source_drain_region.bbox().left + finger_width + finger_sep + gate_overlap),\
            pya.Point(x/dbu - gate_region.bbox().top - bg_ov,\
                      posy + source_drain_region.bbox().right - finger_width),\
            pya.Point(x/dbu,\
                      posy + source_drain_region.bbox().right - finger_width)\
            ])
        self.cell.shapes(sd).insert(D_In)

        #via connection
        PV_Region_sq = pya.Region(pya.Box(x/dbu - gate_region.bbox().top -EL_W - bg_ov\
            , posy + source_drain_region.bbox().left + finger_width + finger_sep + gate_overlap,\
            x/dbu - gate_region.bbox().top - bg_ov\
            , posy + source_drain_region.bbox().left + finger_width + finger_sep + gate_overlap + EL_W))
        self.cell.shapes(gc).insert(PV_Region_sq)
        self.cell.shapes(sd).insert(PV_Region_sq)

        #Output via
        PV_Region = pya.Region(pya.Box(PV_Region_sq.bbox().left + In_Box, PV_Region_sq.bbox().bottom + In_Box,\
            PV_Region_sq.bbox().right - In_Box, PV_Region_sq.bbox().top - In_Box))       
        PV_Region = PV_Region.round_corners(PV_BOX, PV_BOX, nr)
        self.cell.shapes(pv).insert(PV_Region)
        
  def impl(self):
    #Definitions
    dbu = self.layout.dbu
    ov = self.o
    ov_dbu = ov / dbu
    via = self. via
    w_d = self.w_d
    Int_Con = self.Int_Con
    out = self.out
    mode = self.mode
    load = self.load
    bg = self.bg
    ovl = self.ovl
    ovr = self.ovr
    path_width = ov + via
    path_width_dbu = path_width/dbu
    finger_width = self.fw
    finger_width_dbu = finger_width / dbu
    finger_sep = self.s
    finger_sep_dbu = finger_sep / dbu
    path_step = path_width_dbu + finger_sep_dbu
    right_ov_load = path_width + finger_sep
#    txt = self.layout.layer(0,0)
#    bm = self.layout.layer(1,0)
#    bl = self.layout.layer(2,0)
#    sd = self.layout.layer(3,0)
#    gm = self.layout.layer(4,0)
#    pv = self.layout.layer(6,0)
#    gc = self.layout.layer(7,0)
#    pv2= self.layout.layer(9,0)
#    gc2= self.layout.layer(10,0)

        # Define layer names
    # Assign layers using list comprehension
    layers = [self.layout.layer(i, 0) for i in [0, 1, 2, 3, 4, 6, 7, 9]]
    # Unpack layers into variables
    txt, bm, bl, sd, gm, pv, gc, pv2 = layers
    q = self.l_d / self.l_l
    p = int(self.r / q)
    y = 0
    x0 = -((self.n_d*self.l_d)+(self.n_d+1)*finger_width)/2 
    tr_n=1
    xp=x0-(self.n_d*tr_n*(finger_width+self.l_d)/2)
    
    
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
        # 999: Drain Input
    #If out = 0, the via of the transistors are down
    #If out = 1, the via of the transistors are up
    # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)0
    self.transistor(mode, xp, y, w_d, self.n_d, self.l_d, bg, load, Int_Con, ovl, ovr, out)

  def produce_impl(self):
    
    self.impl()

# class MyLib(pya.Library):

# The library where we will put the PCell into 

#  def _init_(self):
#  
#    # Set the description
#    self.description = "Transistor"
#    
#    # Create the PCell declarations
#    self.layout().register_pcell("Transistor", Transistor())
#    # That would be the place to put in more PCells ...
#    
#    # Register us with the name "MyLib".
#    # If a library with that name already existed, it will be replaced then.
#    self.register("Transistor")

# Instantiate and register the library
#MyLib()