import json

hexToBin = lambda h, l: format(int(h, 16), f'0{l}b')

with open("./instLib.json", encoding="utf-8-sig") as j:
    INSTRUCTIONS = json.load(j)
    MEMORY_INST = ["lb", "lh", "lw", "lbu", "lhu", "sb", "sh", "sw"]

    # FOLLOWING IS NOT USED ANYMORE
    SHIFT_INST = {"shamt":["sll", "srl", "sra"], "v":["sllv", "srlv", "srav"]}
    BRANCH_INST = ["beq", "bne", "blez", "bgtz"]
    RT_RSO_INST = ["jr", "mthi", "mtlo"]
    RT_RDO_INST = ["mfhi", "mflo"]
    HILO_INST = ["mult", "multu", "div", "divu"]

with open("./regLoc.json", encoding="utf-8-sig") as j:
    REGISTERS = json.load(j)
    FORMAT_REG = ["rs", "rt", "rd"]

with open("./typeForm.json", encoding="utf-8-sig") as j:
    TYPES = json.load(j)
    RDATA = TYPES["R"]
    IDATA = TYPES["I"]
    JDATA = TYPES["J"]

with open("./demo.asm") as f:
    l = f.readlines()

bins = []

for i in l:
    inst = i.split(" ")[0]
    if inst not in INSTRUCTIONS.keys():
        print(f'INSTRUCTION "{inst.strip()}" NOT FOUND ... skipping')
        bins.append(i)
        continue

    instData = INSTRUCTIONS[inst]
    paramData = i.split(" ", maxsplit=1)[1].replace(" ", "").strip().split(",")
    
    match instData["Type"]:
        case "R":
            base = {i[0]:format(0, f'0{i[1]}b') for i in zip(RDATA["order"], RDATA["size"].values())}
            base["op"] = hexToBin(instData["Opcode"], RDATA["size"]["op"])
            base["funct"] = hexToBin(instData["Funct"], RDATA["size"]["funct"])
            
            for i in zip(instData["Format"], paramData):
                if i[0] in FORMAT_REG:
                    base[i[0]] = format(REGISTERS[i[1]], f'0{RDATA["size"][i[0]]}b')
                else:
                    base[i[0]] = format(int(i[1]), f'0{RDATA["size"][i[0]]}b')

            # DEPRECATED
            # if inst in [*RT_RSO_INST, *HILO_INST]:
            #     baseR["rd"] = format(0, f'0{RDATA["size"]["rd"]}b')
            #     baseR["shamt"] = format(0, f'0{RDATA["size"]["shamt"]}b')
            #     baseR["rs"] = format(REGISTERS[paramData[0]], f'0{RDATA["size"]["rs"]}b')
            #     if inst not in RT_RSO_INST:
            #         baseR["rt"] = format(REGISTERS[paramData[1]], f'0{RDATA["size"]["rt"]}b')
            #     else:
            #         baseR["rt"] = format(0, f'0{RDATA["size"]["rt"]}b')
            # else:
            #     baseR["rd"] = format(REGISTERS[paramData[0]], f'0{RDATA["size"]["rd"]}b')
            #     if inst not in RT_RDO_INST:
            #         if inst in [*SHIFT_INST["shamt"], *SHIFT_INST["v"]]:
            #             baseR["rt"] = format(REGISTERS[paramData[1]], f'0{RDATA["size"]["rt"]}b')
            #             if inst in SHIFT_INST["shamt"]:
            #                 baseR["shamt"] = format(int(paramData[2]), f'0{RDATA["size"]["shamt"]}b')
            #                 baseR["rs"] = format(0, f'0{RDATA["size"]["rs"]}b')
            #             else:
            #                 baseR["shamt"] = format(0, f'0{RDATA["size"]["shamt"]}b')
            #                 baseR["rs"] = format(REGISTERS[paramData[2]], f'0{RDATA["size"]["rs"]}b')
            #         else: 
            #             baseR["shamt"] = format(0, f'0{RDATA["size"]["shamt"]}b')
            #             baseR["rs"] = format(REGISTERS[paramData[1]], f'0{RDATA["size"]["rs"]}b')
            #             baseR["rt"] = format(REGISTERS[paramData[2]], f'0{RDATA["size"]["rt"]}b')
            #     else:
            #         baseR["shamt"] = format(0, f'0{RDATA["size"]["shamt"]}b')
            #         baseR["rs"] = format(0, f'0{RDATA["size"]["rs"]}b')
            #         baseR["rt"] = format(0, f'0{RDATA["size"]["rt"]}b')
                
        case "I":
            base = {i[0]:format(0, f'0{i[1]}b') for i in zip(IDATA["order"], IDATA["size"].values())}
            base["op"] = hexToBin(instData["Opcode"], IDATA["size"]["op"])
            if inst in MEMORY_INST:
                irs = paramData[1].split("(")
                paramData.insert(1, irs[0])
                paramData[2] = irs[1][:-1]

            for i in zip(instData["Format"], paramData):
                if i[0] in FORMAT_REG:
                    base[i[0]] = format(REGISTERS[i[1]], f'0{IDATA["size"][i[0]]}b')
                else:
                    pdi = int(i[1])
                    base[i[0]] = format((pdi) if pdi >= 0 else (pdi & 0b1111111111111111), f'0{IDATA["size"][i[0]]}b')
                
            # DEPRECATED
            # if inst in BRANCH_INST:
            #     baseI["rs"] = format(REGISTERS[paramData[0]], f'0{IDATA["size"]["rs"]}b')
            #     if len(paramData) == 3:
            #         baseI["rt"] = format(REGISTERS[paramData[1]], f'0{IDATA["size"]["rt"]}b')
            #         pdi = int(paramData[2])
            #         baseI["i"] = format((pdi) if pdi >= 0 else (pdi & 0b1111111111111111), f'0{IDATA["size"]["i"]}b')
            #     else:
            #         baseI["rt"] = format(0, f'0{IDATA["size"]["rt"]}b')
            #         pdi = int(paramData[1])
            #         baseI["i"] = format((pdi) if pdi >= 0 else (pdi & 0b1111111111111111), f'0{IDATA["size"]["i"]}b')
            # else:
            #     baseI["rt"] = format(REGISTERS[paramData[0]], f'0{IDATA["size"]["rt"]}b')
                
            #     if inst in MEMORY_INST:
            #         d = paramData[1].split("(")
            #         pdi = int(d[0])
            #         baseI["rs"] = format(REGISTERS[d[1][:-1]], f'0{IDATA["size"]["rs"]}b')
            #         baseI["i"] = format((pdi) if pdi >= 0 else (pdi & 0b1111111111111111), f'0{IDATA["size"]["i"]}b')
            #     else:
            #         if inst == "lui":
            #             baseI["rs"] = format(0, f'0{IDATA["size"]["rs"]}b')
            #             pdi = int(paramData[1])
            #             baseI["i"] = format((pdi) if pdi >= 0 else (pdi & 0b1111111111111111), f'0{IDATA["size"]["i"]}b')
            #         baseI["rs"] = format(REGISTERS[paramData[1]], f'0{IDATA["size"]["rs"]}b')
            #         pdi = int(paramData[2])
            #         baseI["i"] = format((pdi) if pdi >= 0 else (pdi & 0b1111111111111111), f'0{IDATA["size"]["i"]}b')

        case "J":
            base = {i[0]:format(0, f'0{i[1]}b') for i in zip(JDATA["order"], JDATA["size"].values())}
            base["op"] = hexToBin(instData["Opcode"], JDATA["size"]["op"])
            pdi = int(paramData[0])
            base["ad"] = format((pdi) if pdi >= 0 else (pdi & 0b1111111111111111), f'0{JDATA["size"]["ad"]}b')
    
        case _:
            print("UNRECOGNIZED FORMAT")

    bins.append("".join(base.values())+"\n")
    print(f'R...{inst}...{base}')

with open("res.bin", "w+") as f:
    f.writelines(bins)