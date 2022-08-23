# $description: Ring Oscillator Array generator
# $version: 0.1
import pya
import csv
import os
import time
# Fetch a reference to the current layout (ly is an alias)
ly = pya.CellView().active().layout()

bm = ly.layer(1,0)
sd = ly.layer(3,0)
gm = ly.layer(4,0)
gc = ly.layer(7,0)
text_param_list = list()
text_param_list.append(["device_id", "device design", "X", "Y", "Drive Width", "Drive Length","number of fingers", "Buffer"])
# array_cell is created if it doesn't exist, otherwise we just grab a reference to the existing cell
array_cell = ly.cell("TOP")
inverter_id_params ={
    "n_f": [1, 2, 3, 4],
    "ring_name":['Ring_AOI21','Ring_AOI31','Ring_AOI211','Ring_Inv', 'Ring_NAND2', 'Ring_NAND3','Ring_NOR2', 'Ring_NOR3', 'Ring_NOR4' ],
    "buff": [True, False]
    }
device_id = 0
i = -1
j = 0
x_dis = 1400
y_dis = 600
x = 13
y = 15
if array_cell is None:
  print("Creating array_cell")
  array_cell = ly.create_cell("TOP")
  pya.CellView().active().cell.insert(pya.DCellInstArray(array_cell.cell_index(), pya.DTrans(pya.DVector(0,0))))

array_cell.prune_subcells(-1)

path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
if not os.path.isdir(path+'\SmartKem'):
   os.makedirs(path+'\SmartKem')
with open(path+'\SmartKem\Ring_Oscillator_'+time.strftime("%Y%m%d-%H%M%S")+'.csv', 'w', newline='') as myfile:
      
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for _ in range (2):
        for rings in inverter_id_params["ring_name"]:
            if (i>=x and j>y):
                break
            else:
                for n_f in inverter_id_params["n_f"]:
                    if (i>=x and j>y):
                        break
                    else:
                        for buff in inverter_id_params["buff"]:
                            if (i>=x and j>y):
                                break
                            else:
                                if(i>=x and j>y):
                                    break
                                elif (i>=x and j<=y):
                                    j += 1
                                    i = 0
                                elif (i<x):
                                    i +=1
                                sub_pcell = ly.create_cell(rings, rings, { "pad": 1,"n_d": n_f, "buffer": buff })
                                array_cell.insert(pya.CellInstArray(sub_pcell.cell_index(), pya.DTrans(i*x_dis/ly.dbu, j*y_dis/ly.dbu)))
                                text_param_list.append([device_id, rings, i*x_dis, j*y_dis, 90*n_f, 2.5, n_f, buff])
                                device_id +=1
    wr.writerows(text_param_list)