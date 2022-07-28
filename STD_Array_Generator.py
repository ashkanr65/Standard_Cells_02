# $description: Standard cell Array generator
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
text_param_list.append(["device_id", "device design", "X", "Y", "Drive Width", "Drive Length","number of fingers", "Mod"])
# array_cell is created if it doesn't exist, otherwise we just grab a reference to the existing cell
array_cell = ly.cell("TOP")
inverter_id_params ={
    "n_f": [1, 2, 3, 4],
    "one_positions":['Inverter_V2','NAND2_v2','NOR2_v2','XOR_V2' ],
    "two_positions":['DLatch_v2','DFF_V2','DFFR_V2','DFFS_V2', 'MUX_2_V2'],
    "four_positions":["NAND3_v2", "NOR3_v2","AOI21_v2"],
    "seven_positions":["AOI31_v2", "NOR4_v2","AOI211_v2"],
    "Mod_2":[0, 1],
    "Mod_4":[0, 1, 2, 3],
    "Mod_7":[['0','0','1','1'], ['0','1','0','1'],['1','0','0','1'],['0','1','1','0'],['1','0','1','0'],['1','1','0','0'],['1','1','1','1']]  
    }
device_id = 0
i = 0
j = 0
x_dis = 1000
y_dis = 600
x = 19
y = 15
if array_cell is None:
  print("Creating array_cell")
  array_cell = ly.create_cell("TOP")
  pya.CellView().active().cell.insert(pya.DCellInstArray(array_cell.cell_index(), pya.DTrans(pya.DVector(0,0))))

array_cell.prune_subcells(-1)

# path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# if not os.path.isdir(path+'\SmartKem'):
#    os.makedirs(path+'\SmartKem')
# with open(path+'\SmartKem\STD_Cell_V2_'+time.strftime("%Y%m%d-%H%M%S")+'.csv', 'w', newline='') as myfile:
      
#   wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
while(not(i>=x and j>y)):
    for ones in inverter_id_params["one_positions"]:
        if (i>=x and j>y):
            break
        else:
            for n_f in inverter_id_params["n_f"]:
                if (i>=x and j>y):
                    break
                else:
                    sub_pcell = ly.create_cell(ones, "STD_Cell_V2", { "pad": 1,"n_d": n_f })
                    array_cell.insert(pya.CellInstArray(sub_pcell.cell_index(), pya.DTrans(i*x_dis/ly.dbu, j*y_dis/ly.dbu)))
                    # text_param_list.append([device_id, i*x_dis, j*y_dis, w_d*n_d, l_d, c, l_l, r, bgp_yn, o, vgs, bgd_Vdd])
                    device_id +=1
                    if(i>=x and j>y):
                        break
                    elif (i>=x and j<=y):
                        j += 1
                        i = 0
                    elif (i<x):
                        i +=1
    for n_f in inverter_id_params["n_f"]:
        if (i>=x and j>y):
            break
        else:
            for TF in inverter_id_params["Mod_2"]:
                if (i>=x and j>y):
                    break
                else:
                    for twos in inverter_id_params["two_positions"]:
                        if (i>=x and j>y):
                            break
                        else:
                            if twos == 'MUX_2_V2':
                                sub_pcell = ly.create_cell(twos, "STD_Cell_V2", { "pad": 1,"n_d": n_f, "sel": TF})
                                array_cell.insert(pya.CellInstArray(sub_pcell.cell_index(), pya.DTrans(i*x_dis/ly.dbu, j*y_dis/ly.dbu)))
                                # text_param_list.append([device_id, i*x_dis, j*y_dis, w_d*n_d, l_d, c, l_l, r, bgp_yn, o, vgs, bgd_Vdd])
                                device_id +=1
                                if(i>=x and j>y):
                                    break
                                elif (i>=x and j<=y):
                                    j += 1
                                    i = 0
                                elif (i<x):
                                    i +=1
                            else:
                                sub_pcell = ly.create_cell(twos, "STD_Cell_V2", { "pad": 1,"n_d": n_f, "q": TF})
                                array_cell.insert(pya.CellInstArray(sub_pcell.cell_index(), pya.DTrans(i*x_dis/ly.dbu, j*y_dis/ly.dbu)))
                                # text_param_list.append([device_id, i*x_dis, j*y_dis, w_d*n_d, l_d, c, l_l, r, bgp_yn, o, vgs, bgd_Vdd])
                                device_id +=1
                                if(i>=x and j>y):
                                    break
                                elif (i>=x and j<=y):
                                    j += 1
                                    i = 0
                                elif (i<x):
                                    i +=1
    for n_f in inverter_id_params["n_f"]:
        if (i>=x and j>y):
            break
        else:
            for M4 in inverter_id_params["Mod_4"]:
                if (i>=x and j>y):
                    break
                else:
                    for fours in inverter_id_params["four_positions"]:
                        if (i>=x and j>y):
                            break
                        else:
                            sub_pcell = ly.create_cell(fours, "STD_Cell_V2", { "pad": 1,"n_d": n_f, "AO": M4})
                            array_cell.insert(pya.CellInstArray(sub_pcell.cell_index(), pya.DTrans(i*x_dis/ly.dbu, j*y_dis/ly.dbu)))
                            # text_param_list.append([device_id, i*x_dis, j*y_dis, w_d*n_d, l_d, c, l_l, r, bgp_yn, o, vgs, bgd_Vdd])
                            device_id +=1
                            if(i>=x and j>y):
                                break
                            elif (i>=x and j<=y):
                                j += 1
                                i = 0
                            elif (i<x):
                                i +=1

    for n_f in inverter_id_params["n_f"]:
        if (i>=x and j>y):
            break
        else:
            for s1 in inverter_id_params["Mod_2"]:
                if (i>=x and j>y):
                    break
                else:
                    for s0 in inverter_id_params["Mod_2"]:
                        if (i>=x and j>y):
                            break
                        else:
                            sub_pcell = ly.create_cell("MUX_4_V2", "STD_Cell_V2", { "pad": 1,"n_d": n_f, "sel0": s0, "sel1":s1})
                            array_cell.insert(pya.CellInstArray(sub_pcell.cell_index(), pya.DTrans(i*x_dis/ly.dbu, j*y_dis/ly.dbu)))
                            # text_param_list.append([device_id, i*x_dis, j*y_dis, w_d*n_d, l_d, c, l_l, r, bgp_yn, o, vgs, bgd_Vdd])
                            device_id +=1
                            if(i>=x and j>y):
                                break
                            elif (i>=x and j<=y):
                                j += 1
                                i = 0
                            elif (i<x):
                                i +=1
    for seven in inverter_id_params["seven_positions"]:
        if (i>=x and j>y):
            break
        else:
            for n_f in inverter_id_params["n_f"]:
                if (i>=x and j>y):
                    break
                else:
                    for AO in inverter_id_params["Mod_7"]:
                        if (i>=x and j>y):
                            break
                        else:
                            sub_pcell = ly.create_cell(seven, "STD_Cell_V2", { "pad": 1,"n_d": n_f, "AO": AO})
                            array_cell.insert(pya.CellInstArray(sub_pcell.cell_index(), pya.DTrans(i*x_dis/ly.dbu, j*y_dis/ly.dbu)))
                            # text_param_list.append([device_id, i*x_dis, j*y_dis, w_d*n_d, l_d, c, l_l, r, bgp_yn, o, vgs, bgd_Vdd])
                            device_id +=1
                            if(i>=x and j>y):
                                break
                            elif (i>=x and j<=y):
                                j += 1
                                i = 0
                            elif (i<x):
                                i +=1
    #   wr.writerows(text_param_list)