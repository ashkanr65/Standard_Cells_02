# $autorun
# -*- coding: utf-8 -*-
"""
@author: Ashkan
Email:ashkan.rezaee@uab.cat
"""

from typing import Sized
import pya
import math

class DFF_chain(pya.PCellDeclarationHelper):
  """
  The PCell declaration for the Corbino
  """

  def __init__(self):

    # Important: initialize the super class
    super(DFF_chain, self).__init__()

    # declare the parameters
    self.param("n_d", self.TypeInt, "Number of Drive Fingers", default = 1)
    self.param("l_d", self.TypeDouble, "Drive Length", default = 2.5)
    self.param("l_l", self.TypeDouble, "Load Length", default = 2.5)
    self.param("r", self.TypeDouble, "Ratio", default = 1)
    self.param("o", self.TypeDouble, "Gate Overlap", default = 2.5)
    self.param("fw", self.TypeDouble, "Finger Width", default = 3.5)
    self.param("s", self.TypeDouble, "Finger Separation", default = 2.5)
    self.param("via", self.TypeDouble, "via size", default = 2.5)
    self.param("rail", self.TypeDouble, "rail to finger width ratio", default = 3)
    self.param("PDN_S", self.TypeDouble, "Extra distance for PDN", default = 0)
    self.param("pad", self.TypeBoolean, "Pads", default = False)
    
  def display_text_impl(self):
    # Provide a descriptive text for the cell
    return "STD Cell DFF_chain:(ratio=" + str((self.r)) + ",Width="+ "90*"+str((self.n_d)) + ")"

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
        bm = self.layout.layer(1, 0)
        bl = self.layout.layer(2, 0)
        sd = self.layout.layer(3, 0)
        gm = self.layout.layer(4, 0)
        pv = self.layout.layer(6, 0)
        gc = self.layout.layer(7, 0)
        pv2 = self.layout.layer(9, 0)

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
    bm = self.layout.layer(1,0)
    bl = self.layout.layer(2,0)
    sd = self.layout.layer(3,0)
    gm = self.layout.layer(4,0)
    pv = self.layout.layer(6,0)
    gc = self.layout.layer(7,0)
    pv2= self.layout.layer(9,0)
    gc2= self.layout.layer(10,0)

    # fetch the parameters
    dbu = self.layout.dbu # How large the database unit is in microns (usually 0.001, i.e. 1 nm)
    ov_l = ov_l / dbu
    ov_r = ov_r / dbu
    gate_overlap = self.o / dbu
    n = n_i
    bg_ov = gate_overlap
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
            VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
            self.cell.shapes(bm).insert(VBG_Ele_out)
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
            VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
            self.cell.shapes(bm).insert(VBG_Ele_out)

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
            VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
            self.cell.shapes(bm).insert(VBG_Ele_out)
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
            VBG_Ele_out = pya.Region(pya.Box(posx - finger_width, VDD_T_E, posx, posy)) # Vbgelectrode
            self.cell.shapes(bm).insert(VBG_Ele_out)

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
        vdd0 = pya.Region(pya.Box(posx - drain_backbone_region.bbox().top, VDD_B_E - gate_overlap\
            , posx + drain_backbone_region.bbox().top, VDD_T_E))
        self.cell.shapes(sd).insert(vdd0)
    if (level == 1):
        vdd1 = pya.Region(pya.Box(posx - drain_backbone_region.bbox().top, VDD_B_E - gate_overlap\
            , posx + drain_backbone_region.bbox().top, VDD_T_E))
        self.cell.shapes(sd).insert(vdd1)
    if (level == 3):
        vss = pya.Region(pya.Box(posx - source_backbone_region.bbox().bottom, VSS_T_E + gate_overlap\
            , posx - source_backbone_region.bbox().top, VSS_B_E))
        self.cell.shapes(sd).insert(vss)
        
    Right_Edge = posx + source_drain_region.bbox().top + finger_width #Right edge of Cell
    
    VDD_Ele = pya.Region(pya.Box(Left_Edge - ov_l, VDD_B_E, Right_Edge + ov_r, VDD_T_E)) # VDD rail
    VSS_Ele = pya.Region(pya.Box(Left_Edge - ov_l, VSS_B_E, Right_Edge + ov_r, VSS_T_E)) # VSS rail
    V_Ele = VDD_Ele + VSS_Ele
    self.cell.shapes(sd).insert(V_Ele)

    VBG_Ele = pya.Region(pya.Box(Left_Edge - ov_l, VDD_T_E, Right_Edge + ov_r, VDD_T_E - finger_width)) # Vgb rail
    self.cell.shapes(bm).insert(VBG_Ele)

    VDDTregion = pya.TextGenerator.default_generator().text\
        ("VDD", 0.001, 2*self.via).move(posx - PV_BOX, VDD_B_E)
    VSSTregion = pya.TextGenerator.default_generator().text\
        ("VSS", 0.001, 2*self.via).move(posx - PV_BOX, VSS_B_E)
    Tregion = VDDTregion + VSSTregion
    self.cell.shapes(sd).insert(Tregion)
    
    #Connection
    #Source to Gate
    if (Int_Con == 1 and out != 1):
        D1_D2 = pya.Polygon([
            pya.Point(x/dbu - gate_region.bbox().top-gate_overlap ,\
                      posy + source_drain_region.bbox().left + finger_width + finger_sep + gate_overlap+EL_W),\
            pya.Point(x/dbu - gate_region.bbox().top-gate_overlap,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - gate_overlap - finger_width ,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - gate_overlap - finger_width ,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-gate_overlap-EL_W,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-gate_overlap-EL_W,\
                      posy + source_drain_region.bbox().left + finger_width + finger_sep + gate_overlap+EL_W),\
            ])
        self.cell.shapes(sd).insert(D1_D2)

        #via connection
        PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().left, gate_region.bbox().top+gate_overlap,\
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
            pya.Point(x/dbu - gate_region.bbox().top-gate_overlap ,\
                      posy + source_drain_region.bbox().right - (finger_width + finger_sep + gate_overlap)),\
            pya.Point(x/dbu - gate_region.bbox().top-gate_overlap,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - gate_overlap - finger_width ,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - gate_overlap - finger_width ,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-gate_overlap-EL_W,\
                      posy + source_drain_region.bbox().left + finger_width),\
            pya.Point(x/dbu - gate_region.bbox().top-gate_overlap-EL_W,\
                      posy + source_drain_region.bbox().right - (finger_width + finger_sep + gate_overlap)),\
            ])
        self.cell.shapes(sd).insert(D1_D2)

        #via connection
        PV_Region_sq = pya.Region(pya.Box(gate_region.bbox().right, gate_region.bbox().top+gate_overlap,\
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
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - gate_overlap - finger_width ,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - gate_region.bbox().top-2*EL_W - gate_overlap - finger_width ,\
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
            pya.Point(x/dbu - source_drain_region.bbox().top - 2*finger_sep - gate_overlap - finger_width,\
                      posy + source_drain_region.bbox().left),\
            pya.Point(x/dbu - source_drain_region.bbox().top - 2*finger_sep - gate_overlap - finger_width,\
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
        
  def impl(self):
    #Definitions
    dbu = self.layout.dbu
    ov = self.o
    ov_dbu = ov / dbu
    via = self. via
    w_d = 90
    path_width = ov + via
    path_width_dbu = path_width/dbu
    finger_width = self.fw
    finger_sep = self.s
    finger_sep_dbu = finger_sep / dbu
    finger_width_dbu = finger_width / dbu
    path_step = path_width_dbu + finger_sep_dbu
    right_ov_load = path_width + finger_sep
    txt = self.layout.layer(0,0)
    bm = self.layout.layer(1,0)
    bl = self.layout.layer(2,0)
    sd = self.layout.layer(3,0)
    gm = self.layout.layer(4,0)
    pv = self.layout.layer(6,0)
    gc = self.layout.layer(7,0)
    pv2= self.layout.layer(9,0)
    gc2= self.layout.layer(10,0)
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
        + 3*ov +2*via)/5
    Top_Path = (w_d/2 + self.o + 2*self.s + finger_width - path_width/2)/dbu #Top edge of Cell
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
    for k in range(0,600,150):
        y = k
        Top_Edge = (y + w_d/2 + ov + 2*finger_sep + finger_width + self.PDN_S)/dbu  #Top edge of Cell
        Bottom_Edge = (y-(w_d/2 + ov + 2*finger_sep + finger_width + self.PDN_S))/dbu #Bottom edge of Cell
        #CHAIN 1
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)0
        tr_n=38
        xp=x0-(self.n_d*tr_n*(finger_width+self.l_d)/2)
        self.transistor(0, xp, y, w_d, self.n_d, self.l_d, True, False, 0, 0, 0, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("clk", 0.001, 5).move((xp- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)1
        x1 = xp + 5*d_x_100
        self.transistor(1, x1, y, w_d, self.n_d, self.l_d, True, False, 100, d_x_0, d_x_0, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("D", 0.001, 5).move((x1- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)2
        x2 = x1 + 5*d_x_101
        self.transistor(2, x2, y, w_d, self.n_d, self.l_d, True, False, 101, d_x_101, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out1", 0.001, 5).move((x2- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)3
        x3 = x2 + 5*l_x
        self.transistor(3, x3, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out0", 0.001, 5).move((x3 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #D inverter
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)4
        x4 = x3 + 5*d_x_101
        self.transistor(1, x4, y, w_d, self.n_d, self.l_d, True, False, 0, 0, right_ov_load, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("D", 0.001, 5).move((x4- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)5
        x5 = x4 + 5*l_x
        self.transistor(3, x5, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!D", 0.001, 5).move((x5- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #AOI21_2
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)6
        x6 = x5 + 5*d_x_101
        self.transistor(0, x6, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, d_x_101, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!D", 0.001, 5).move((x6- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)7
        x7 = x6 + 5*d_x_0
        self.transistor(1, x7, y, w_d, self.n_d, self.l_d, True, False, 100, d_x_0, d_x_0, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("clk", 0.001, 5).move((x7 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)8
        x8 = x7 + 5*d_x_101
        self.transistor(2, x8, y, w_d, self.n_d, self.l_d, True, False, 101, d_x_101, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out0", 0.001, 5).move((x8- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)9
        x9 = x8 + 5*l_x
        self.transistor(3, x9, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out1", 0.001, 5).move((x9- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #clock inverter
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)10
        x10 = x9 + 5*d_x_101
        self.transistor(1, x10, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, right_ov_load, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("clk", 0.001, 5).move((x10- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)11
        x11 = x10 + 5*l_x
        self.transistor(3, x11, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!clk", 0.001, 5).move((x11 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #AOI21_3
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)12
        x12 = x11 + 5*d_x_101
        self.transistor(0, x12, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, d_x_101, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!clk", 0.001, 5).move((x12 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)13
        x13 = x12 + 5*d_x_0
        self.transistor(1, x13, y, w_d, self.n_d, self.l_d, True, False, 100, d_x_0, d_x_0, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out1", 0.001, 5).move((x13 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)14
        x14 = x13 + 5*d_x_101
        self.transistor(2, x14, y, w_d, self.n_d, self.l_d, True, False, 101, d_x_101, right_ov_load, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("Q", 0.001, 5).move((x14 - gate_edge) / dbu, Top_Path + 20 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)15
        x15 = x14 + 5*l_x
        self.transistor(3, x15, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("Q'", 0.001, 5).move((x15 - gate_edge) / dbu, Top_Path + 20 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #D inverter
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)16
        x16 = x15 + 5*d_x_101
        self.transistor(1, x16, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out1", 0.001, 5).move((x16 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)17
        x17 = x16 + 5*l_x
        self.transistor(3, x17, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!out1", 0.001, 5).move((x17 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #AOI21_4
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)18
        x18 = x17 + 5*d_x_101
        self.transistor(0, x18, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, d_x_101, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!out1", 0.001, 5).move((x18 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)19
        x19 = x18 + 5*d_x_0
        self.transistor(1, x19, y, w_d, self.n_d, self.l_d, True, False, 100, d_x_0, d_x_0, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!clk", 0.001, 5).move((x19 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)20
        x20 = x19 + 5*d_x_101
        self.transistor(2, x20, y, w_d, self.n_d, self.l_d, True, False, 101, d_x_101, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("Q'", 0.001, 5).move((x20 - gate_edge) / dbu, Top_Path + 20 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)21
        x21 = x20 + 5*l_x
        self.transistor(3, x21, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 3)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("Q", 0.001, 5).move((x21 - gate_edge) / dbu, Top_Path + 20 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #CHAIN 2
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)22
        x22 = x21 + 5*d_x_101
        self.transistor(0, x22, y, w_d, self.n_d, self.l_d, True, False, 0, 0, 0, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("clk", 0.001, 5).move((x22- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)23
        x23 = x22 + 5*d_x_100
        self.transistor(1, x23, y, w_d, self.n_d, self.l_d, True, False, 100, d_x_0, d_x_0, 3)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("D", 0.001, 5).move((x23- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)24
        x24 = x23 + 5*d_x_101
        self.transistor(2, x24, y, w_d, self.n_d, self.l_d, True, False, 101, d_x_101, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out1", 0.001, 5).move((x24- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)25
        x25 = x24 + 5*l_x
        self.transistor(3, x25, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out0", 0.001, 5).move((x25 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #D inverter
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)26
        x26 = x25 + 5*d_x_101
        self.transistor(1, x26, y, w_d, self.n_d, self.l_d, True, False, 0, 0, right_ov_load, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("D", 0.001, 5).move((x26- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)27
        x27 = x26 + 5*l_x
        self.transistor(3, x27, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!D", 0.001, 5).move((x27- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #AOI21_2
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)28
        x28 = x27 + 5*d_x_101
        self.transistor(0, x28, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, d_x_101, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!D", 0.001, 5).move((x28- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)29
        x29 = x28 + 5*d_x_0
        self.transistor(1, x29, y, w_d, self.n_d, self.l_d, True, False, 100, d_x_0, d_x_0, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("clk", 0.001, 5).move((x29 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)30
        x30 = x29 + 5*d_x_101
        self.transistor(2, x30, y, w_d, self.n_d, self.l_d, True, False, 101, d_x_101, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out0", 0.001, 5).move((x30- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)31
        x31 = x30 + 5*l_x
        self.transistor(3, x31, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out1", 0.001, 5).move((x31- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #clock inverter
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)32
        x32 = x31 + 5*d_x_101
        self.transistor(1, x32, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, right_ov_load, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("clk", 0.001, 5).move((x32- gate_edge)/ dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)33
        x33 = x32 + 5*l_x
        self.transistor(3, x33, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!clk", 0.001, 5).move((x33 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #AOI21_3
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)34
        x34 = x33 + 5*d_x_101
        self.transistor(0, x34, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, d_x_101, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!clk", 0.001, 5).move((x34 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)35
        x35 = x34 + 5*d_x_0
        self.transistor(1, x35, y, w_d, self.n_d, self.l_d, True, False, 100, d_x_0, d_x_0, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out1", 0.001, 5).move((x35 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)36
        x36 = x35 + 5*d_x_101
        self.transistor(2, x36, y, w_d, self.n_d, self.l_d, True, False, 101, d_x_101, right_ov_load, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("Q", 0.001, 5).move((x36 - gate_edge) / dbu, Top_Path + 20 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)37
        x37 = x36 + 5*l_x
        self.transistor(3, x37, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("Q'", 0.001, 5).move((x37 - gate_edge) / dbu, Top_Path + 20 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #D inverter
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)38
        x38 = x37 + 5*d_x_101
        self.transistor(1, x38, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("out1", 0.001, 5).move((x38 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)39
        x39 = x38 + 5*l_x
        self.transistor(3, x39, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!out1", 0.001, 5).move((x39 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #AOI21_4
        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)40
        x40 = x39 + 5*d_x_101
        self.transistor(0, x40, y, w_d, self.n_d, self.l_d, True, False, 0, d_x_101, d_x_101, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!out1", 0.001, 5).move((x40 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)41
        x41 = x40 + 5*d_x_0
        self.transistor(1, x41, y, w_d, self.n_d, self.l_d, True, False, 100, d_x_0, d_x_0, 0)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("!clk", 0.001, 5).move((x41 - gate_edge) / dbu, -Top_Path - 25 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)42
        x42 = x41 + 5*d_x_101
        self.transistor(2, x42, y, w_d, self.n_d, self.l_d, True, False, 101, d_x_101, right_ov_load, 1)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("Q'", 0.001, 5).move((x42 - gate_edge) / dbu, Top_Path + 20 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        # (level, x, y, w_i, n_i, l_i, bg, Load, In_Con, overlap_left, overlap_rigth, out)43
        x43 = x42 + 5*l_x
        self.transistor(3, x43, y, w_d, p * self.n_d, self.l_l, True, True, 101, l_x, 0, 3)
        #gates name
        iTregion = pya.TextGenerator.default_generator().text\
            ("Q", 0.001, 5).move((x43 - gate_edge) / dbu, Top_Path + 20 / dbu)
        self.cell.shapes(txt).insert(iTregion)

        #Chain 1
        # X0 to X7 connection
        interconnect = pya.Path([pya.Point((xp-gate_edge + (via + ov)/2)/dbu, y/dbu-gate_connection),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, y/dbu-gate_connection + 3*path_step),
            pya.Point((x7-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + 3*path_step),
            pya.Point((x7-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X1 to X4 connection
        interconnect = pya.Path([pya.Point((x1-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x4-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X2 to X9 connection
        interconnect = pya.Path([pya.Point((x2-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x2-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x9-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x9-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X3 to X8 connection
        interconnect = pya.Path([pya.Point((x3-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x3-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection - path_step),
            pya.Point((x8-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection - path_step),
            pya.Point((x8-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X5 to X6 connection
        interconnect = pya.Path([pya.Point((x5-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x6-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X7 to X10 connection
        interconnect = pya.Path([pya.Point((x7-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x7-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + 3*path_step),
            pya.Point((x10-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + 3*path_step),
            pya.Point((x10-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X9 to X13 connection
        interconnect = pya.Path([pya.Point((x9-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x9-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x13-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x13-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X11 to X12 connection
        interconnect = pya.Path([pya.Point((x11-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x12-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X12 to X19 connection
        interconnect = pya.Path([pya.Point((x12-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x12-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + path_step),
            pya.Point((x19-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + path_step),
            pya.Point((x19-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X13 to X16 connection
        interconnect = pya.Path([pya.Point((x13-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x13-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection - path_step),
            pya.Point((x16-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection - path_step),
            pya.Point((x16-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X14 to X21 connection
        interconnect = pya.Path([pya.Point((x14-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x14-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection - path_step),
            pya.Point((x21-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection - path_step),
            pya.Point((x21-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)
        
        # X15 to X20 connection
        interconnect = pya.Path([pya.Point((x15-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x15-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x20-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x20-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X17 to X18 connection
        interconnect = pya.Path([pya.Point((x17-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x18-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # D Input
        Input = pya.Path([pya.Point((x1-gate_edge + (via + ov)/2)/dbu, y/dbu-gate_connection ),
            pya.Point((x1-gate_edge + (via + ov)/2)/dbu, Bottom_Edge),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(Input)

        # clk Input
        Input = pya.Path([pya.Point((xp-gate_edge + (via + ov)/2)/dbu, y/dbu-gate_connection ),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, Bottom_Edge),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(Input)

        # # Q out
        # Out = pya.Path([pya.Point((x20-gate_edge + (via + ov)/2)/dbu, y/dbu+gate_connection ),
        #     pya.Point((x20-gate_edge + (via + ov)/2)/dbu, Top_Edge),
        #     ],path_width_dbu)
        # self.cell.shapes(gc).insert(Out)

        # # Q' out
        # Out = pya.Path([pya.Point((x21-gate_edge + (via + ov)/2)/dbu, y/dbu+gate_connection ),
        #     pya.Point((x21-gate_edge + (via + ov)/2)/dbu, Top_Edge),
        #     ],path_width_dbu)
        # self.cell.shapes(gc).insert(Out)

        #Chain 2
        # X21 to X23 connection
        interconnect = pya.Path([pya.Point((x21-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x23-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X22 to X29 connection
        interconnect = pya.Path([pya.Point((x22-gate_edge + (via + ov)/2)/dbu, y/dbu-gate_connection),
            pya.Point((x22-gate_edge + (via + ov)/2)/dbu, y/dbu-gate_connection + 3*path_step),
            pya.Point((x29-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + 3*path_step),
            pya.Point((x29-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X23 to X26 connection
        interconnect = pya.Path([pya.Point((x23-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x26-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X24 to X31 connection
        interconnect = pya.Path([pya.Point((x24-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x24-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x31-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x31-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X25 to X30 connection
        interconnect = pya.Path([pya.Point((x25-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x25-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection - path_step),
            pya.Point((x30-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection - path_step),
            pya.Point((x30-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X27 to X28 connection
        interconnect = pya.Path([pya.Point((x27-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x28-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X29 to X32 connection
        interconnect = pya.Path([pya.Point((x29-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x29-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + 3*path_step),
            pya.Point((x32-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + 3*path_step),
            pya.Point((x32-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X31 to X35 connection
        interconnect = pya.Path([pya.Point((x31-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x31-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x35-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x35-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X33 to X34 connection
        interconnect = pya.Path([pya.Point((x33-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x34-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X34 to X41 connection
        interconnect = pya.Path([pya.Point((x34-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x34-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + path_step),
            pya.Point((x41-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + path_step),
            pya.Point((x41-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X35 to X16 connection
        interconnect = pya.Path([pya.Point((x35-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x35-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection - path_step),
            pya.Point((x38-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection - path_step),
            pya.Point((x38-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X36 to X43 connection
        interconnect = pya.Path([pya.Point((x36-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x36-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection - path_step),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection - path_step),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)
        
        # X37 to X42 connection
        interconnect = pya.Path([pya.Point((x37-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x37-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x42-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + path_step),
            pya.Point((x42-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X39 to X40 connection
        interconnect = pya.Path([pya.Point((x39-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            pya.Point((x40-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # X10 to X22 connection clock
        interconnect = pya.Path([pya.Point((x10-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            pya.Point((x10-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + 3*path_step),
            pya.Point((x22-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection + 3*path_step),
            pya.Point((x22-gate_edge + (via + ov)/2)/dbu,y/dbu-gate_connection),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(interconnect)

        # # D Input
        # Input = pya.Path([pya.Point((x24-gate_edge + (via + ov)/2)/dbu, y/dbu-gate_connection ),
        #     pya.Point((x24-gate_edge + (via + ov)/2)/dbu, Bottom_Edge),
        #     ],path_width_dbu)
        # self.cell.shapes(gc).insert(Input)

        # # clk Input
        # Input = pya.Path([pya.Point((x27-gate_edge + (via + ov)/2)/dbu, y/dbu-gate_connection + path_step ),
        #     pya.Point((x27-gate_edge + (via + ov)/2)/dbu, Bottom_Edge),
        #     ],path_width_dbu)
        # self.cell.shapes(gc).insert(Input)

        # # Q out
        # Out = pya.Path([pya.Point((x42-gate_edge + (via + ov)/2)/dbu, y/dbu+gate_connection ),
        #     pya.Point((x42-gate_edge + (via + ov)/2)/dbu, Top_Edge),
        #     ],path_width_dbu)
        # self.cell.shapes(gc).insert(Out)

        # Q to next rail D connection clock
        if (y<400):
            interconnect = pya.Path([pya.Point((x43-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection),
                pya.Point((x43-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + 32.5/dbu),
                pya.Point((x1-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + 32.5/dbu),
                pya.Point((x1-gate_edge + (via + ov)/2)/dbu,y/dbu+gate_connection + 65/dbu),
                ],path_width_dbu)
            self.cell.shapes(gc).insert(interconnect)

        # Q out
        Out = pya.Path([pya.Point((x43-gate_edge + (via + ov)/2)/dbu, y/dbu+gate_connection ),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu, Top_Edge),
            ],path_width_dbu)
        self.cell.shapes(gc).insert(Out)

    # Pads
    if(self.pad):
        
        list_a = [-450, 307.5, 1065]
        list_b = [-200, k+200]
        for i in list_a:
            for j in list_b:
                self.create_pad(i, j)
        
        # Vdd connection
        vdd = pya.Path([
            pya.Point((list_a[0]-80)/dbu, (list_b[1])/dbu),
            pya.Point((list_a[0]-80)/dbu, Top_rail),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, Top_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vdd)

        vdd = pya.Path([
            pya.Point((list_a[0]-80)/dbu, (list_b[1])/dbu),
            pya.Point((list_a[0]-80)/dbu, y/3/dbu+Top_rail),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, y/3/dbu+Top_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vdd)

        vdd = pya.Path([
            pya.Point((list_a[0]-80)/dbu, (list_b[1])/dbu),
            pya.Point((list_a[0]-80)/dbu, 2*y/3/dbu+Top_rail),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, 2*y/3/dbu+Top_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vdd)

        vdd = pya.Path([
            pya.Point((list_a[0]-80)/dbu, (list_b[1])/dbu),
            pya.Point((list_a[0]-80)/dbu, y/dbu+Top_rail),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, y/dbu+Top_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vdd)

        # Vss connection
        vss = pya.Path([
            pya.Point((list_a[2]+80)/dbu, (list_b[0])/dbu),
            pya.Point((list_a[2]+80)/dbu, Bottom_rail),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu, Bottom_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vss)

        vss = pya.Path([
            pya.Point((list_a[2]+80)/dbu, (list_b[0])/dbu),
            pya.Point((list_a[2]+80)/dbu, y/3/dbu + Bottom_rail),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu, y/3/dbu + Bottom_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vss)

        vss = pya.Path([
            pya.Point((list_a[2]+80)/dbu, (list_b[0])/dbu),
            pya.Point((list_a[2]+80)/dbu, 2*y/3/dbu + Bottom_rail),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu, 2*y/3/dbu + Bottom_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vss)

        vss = pya.Path([
            pya.Point((list_a[2]+80)/dbu, (list_b[0])/dbu),
            pya.Point((list_a[2]+80)/dbu, y/dbu + Bottom_rail),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu, y/dbu + Bottom_rail),
        ],self.rail*finger_width_dbu)
        self.cell.shapes(sd).insert(vss)

        # Vbg connection
        vbg = pya.Path([
            pya.Point((list_a[1])/dbu, (list_b[1])/dbu),
            pya.Point((list_a[1])/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2),
            pya.Point((list_a[0]-80)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2)
            # pya.Point((xp-gate_edge + (via + ov)/2)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2)
        ],finger_width_dbu)
        self.cell.shapes(bm).insert(vbg)

        vbg = pya.Path([
            pya.Point((list_a[0]-80)/dbu, Top_Edge + self.rail*finger_width_dbu),
            pya.Point((list_a[0]-80)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2 - y/3/dbu),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2 - y/3/dbu)
        ],finger_width_dbu)
        self.cell.shapes(bm).insert(vbg)

        vbg = pya.Path([
            pya.Point((list_a[0]-80)/dbu, Top_Edge + self.rail*finger_width_dbu),
            pya.Point((list_a[0]-80)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2 - 2*y/3/dbu),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2 - 2*y/3/dbu)
        ],finger_width_dbu)
        self.cell.shapes(bm).insert(vbg)

        vbg = pya.Path([
            pya.Point((list_a[0]-80)/dbu, Top_Edge + self.rail*finger_width_dbu),
            pya.Point((list_a[0]-80)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2 - y/dbu),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, Top_Edge + self.rail*finger_width_dbu - finger_width_dbu/2 - y/dbu)
        ],finger_width_dbu)
        self.cell.shapes(bm).insert(vbg)   

        # Vin clock connection
        vin1 = pya.Path([
            pya.Point((list_a[0]+80)/dbu, (list_b[0])/dbu),
            pya.Point((list_a[0]+80)/dbu, -2*path_step + gate_in),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, -2*path_step + gate_in),
            pya.Point((xp-gate_edge + (via + ov)/2)/dbu, Bottom_Edge),
        ],path_width_dbu)
        self.cell.shapes(gc).insert(vin1)

        # Vin2 connection
        vin2 = pya.Path([
            pya.Point((list_a[1])/dbu, (list_b[0])/dbu),
            pya.Point((list_a[1])/dbu, gate_in),
            pya.Point((x1-gate_edge + (via + ov)/2)/dbu, gate_in),
            pya.Point((x1-gate_edge + (via + ov)/2)/dbu, Bottom_Edge - y/dbu),
        ],path_width_dbu)
        self.cell.shapes(gc).insert(vin2)

        # Vout connection
        vout = pya.Path([
            pya.Point((list_a[2]-80)/dbu, (list_b[1])/dbu),
            pya.Point((list_a[2]-80)/dbu, y/dbu+gate_out),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu, y/dbu+gate_out),
            pya.Point((x43-gate_edge + (via + ov)/2)/dbu, Top_Edge),
        ],path_width_dbu)
        self.cell.shapes(gc).insert(vout)

  def produce_impl(self):
    
    self.impl()

class MyLib(pya.Library):

  #The library where we will put the PCell into 

  def __init__(self):
  
    # Set the description
    self.description = "DFF_chain"
    
    # Create the PCell declarations
    self.layout().register_pcell("DFF_chain", DFF_chain())
    # That would be the place to put in more PCells ...
    
    # Register us with the name "MyLib".
    # If a library with that name already existed, it will be replaced then.
    self.register("DFF_chain")

# Instantiate and register the library
MyLib() 