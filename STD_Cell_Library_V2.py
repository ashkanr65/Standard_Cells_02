# $autorun

class STD_Cell_V2(pya.Library):
  """
  The library where we will put the PCells into 
  """

  def __init__(self):
  
    # Set the description
    self.description = "STD Cell Library V2"
    self.layout().register_pcell("AOI21_v2", AOI21_v2())
    self.layout().register_pcell("AOI211_v2", AOI211_v2())
    self.layout().register_pcell("AOI31_v2", AOI31_v2())
    self.layout().register_pcell("DFF_V2", DFF_V2())
    self.layout().register_pcell("DFFR_V2", DFFR_V2())
    self.layout().register_pcell("DFFS_V2", DFFS_V2())  
    self.layout().register_pcell("DLatch_v2", DLatch_v2()) 
    self.layout().register_pcell("Inverter_V2", Inverter_V2())
    self.layout().register_pcell("MUX_2_V2", MUX_2_V2())
    self.layout().register_pcell("MUX_4_V2", MUX_4_V2())
    self.layout().register_pcell("NAND2_v2", NAND2_v2())
    self.layout().register_pcell("NAND3_v2", NAND3_v2())
    self.layout().register_pcell("NOR2_v2", NOR2_v2())
    self.layout().register_pcell("NOR3_v2", NOR3_v2())
    self.layout().register_pcell("NOR4_v2", NOR4_v2())
    self.layout().register_pcell("XOR_V2", XOR_V2())
    
    # Register us with the name "STD_Cell".
    # If a library with that name already existed, it will be replaced then.
    self.register("STD_Cell_V2")

# Instantiate and register the library
STD_Cell_V2()