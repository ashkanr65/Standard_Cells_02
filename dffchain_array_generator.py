# $description: DFF Array generator
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
text_param_list.append(["device_id", "device design", "X", "Y", "Drive Width", "Drive Length","number of fingers"])
# array_cell is created if it doesn't exist, otherwise we just grab a reference to the existing cell
array_cell = ly.cell("TOP")
inverter_id_params ={
    "n_f": [1, 2, 3, 4],
    "cell_name":['DFF_chain' ],
    }
device_id = 0
i = -1
j = 0
x_dis = 1715
y_dis = 1050
x = 10
y = 9
if array_cell is None:
  print("Creating array_cell")
  array_cell = ly.create_cell("TOP")
  pya.CellView().active().cell.insert(pya.DCellInstArray(array_cell.cell_index(), pya.DTrans(pya.DVector(0,0))))

array_cell.prune_subcells(-1)

path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
if not os.path.isdir(path+'\SmartKem'):
   os.makedirs(path+'\SmartKem')
with open(path+'\SmartKem\dffchain_'+time.strftime("%Y%m%d-%H%M%S")+'.csv', 'w', newline='') as myfile:
      
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for _ in range (2):

        for dffchain in inverter_id_params["cell_name"]:
            if (i>=x and j>y):
                break
            else:
                for n_f in inverter_id_params["n_f"]:
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
                        sub_pcell = ly.create_cell(dffchain, dffchain, { "pad": 1,"n_d": n_f, "name": "1_"+"%03d"%device_id, "s": 2.5, "via": 2.5, "o": 5})
                        array_cell.insert(pya.CellInstArray(sub_pcell.cell_index(), pya.DTrans(i*x_dis/ly.dbu, j*y_dis/ly.dbu)))
                        text_param_list.append(["1_"+"%03d"%device_id, dffchain, i*x_dis, j*y_dis, 90*n_f, 2.5, n_f])
                        device_id +=1
    wr.writerows(text_param_list)