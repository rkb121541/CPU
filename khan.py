# Rishi Bidarkota, Joseph DePalo
# I pledge my honor that I have abided by the Stevens Honor System.

import sys

opcodes = {
    "ADD" : "10000",
    "ADDI" : "11000",
    "SUB" : "10100",
    "SUBI" : "11100",
    "LDRI" : "11001",
    "LDR" : "10001",
    "STRI" : "01010",
    "STR" : "00010"
    }

registers = {
    "R0" : "00",
    "R1" : "01",
    "R2" : "10",
    "R3" : "11"
    }

def stripper(s):
    l = s.split(",")
    for i in range(0, len(l)):
        l[i] = l[i].strip()
    return l

def padOnes(r):
    q = ""
    for i in range(0, 7 - len(r)):
        q += "1"
    return q + r
    
def toBinary(l):
    s = ""

    if l[0].upper() == "ADD":
        s += opcodes[l[0].upper()]
        s += registers[l[3].upper()]
        s += "00000"
        s += registers[l[2].upper()]
        s += registers[l[1].upper()]


    elif l[0].upper() == "ADDI":

        if (int(l[3]) > (pow(2,6) - 1)) or (int(l[3]) < -(pow(2,6))):
            raise ValueError("Number must be able to be represented in 7 bits.")
        
        s += opcodes[l[0].upper()]

        if int(l[3]) < 0:
            q = int(l[3]) + 128
            r = bin(q)[2:]
            s += padOnes(r)
        else:
            s += bin(int(l[3]))[2:].zfill(7)
            
        s += registers[l[2].upper()]
        s += registers[l[1].upper()]

    elif l[0].upper() == "SUB":
        s += opcodes[l[0].upper()]
        s += registers[l[3].upper()]
        s += "00000"
        s += registers[l[2].upper()]
        s += registers[l[1].upper()]

    elif l[0].upper() == "SUBI":

        if (int(l[3]) > (pow(2,6) - 1)) or (int(l[3]) < -(pow(2,6))):
            raise ValueError("Number must be able to be represented in 7 bits.")
        
        s += opcodes[l[0].upper()]

        if int(l[3]) < 0:
            q = int(l[3]) + 128
            r = bin(q)[2:]
            s += padOnes(r)
        else:
            s += bin(int(l[3]))[2:].zfill(7)
        
        s += registers[l[2].upper()]
        s += registers[l[1].upper()]

    elif l[0].upper() == "LDRI":
        
        if (int(l[3]) > (pow(2,6) - 1)) or (int(l[3]) < -(pow(2,6))):
            raise ValueError("Number must be able to be represented in 7 bits.")

        s += opcodes[l[0].upper()]

        if int(l[3]) < 0:
            q = int(l[3]) + 128
            r = bin(q)[2:]
            s += padOnes(r)
        else:
            s += bin(int(l[3]))[2:].zfill(7)
        
        s += registers[l[2].upper()]
        s += registers[l[1].upper()]

    elif l[0].upper() == "LDR":
        s += opcodes[l[0]]
        s += registers[l[3]]
        s += "00000"
        s += registers[l[2]]
        s += registers[l[1]]

    elif l[0].upper() == "STRI":
        
        if (int(l[3]) > (pow(2,6) - 1)) or (int(l[3]) < -(pow(2,6))):
            raise ValueError("The immediate (imm7) must be able to be represented in 7 bits.")

        s += opcodes[l[0].upper()]

        if int(l[3]) < 0:
            q = int(l[3]) + 128
            r = bin(q)[2:]
            s += padOnes(r)
        else:
            s += bin(int(l[3]))[2:].zfill(7)

        s += registers[l[2].upper()]
        s += registers[l[1].upper()]

    elif l[0].upper() == "STR":
        s += opcodes[l[0].upper()]
        s += registers[l[3].upper()]
        s += "00000"
        s += registers[l[2].upper()]
        s += registers[l[1].upper()]

    else:
        raise SyntaxError("invalid syntax.")
        
    return s


        
def toHex(b):
    h = hex(int(b, 2))[2:]
    return h



def main():

    if len(sys.argv) != 2 or sys.argv[1][-2:] != ".s":
        raise TypeError("Wrong number of arguments passed. Must be one .s file.")
    
    makeFile = open("output.txt", "w")
    makeFile.write("v3.0 hex words addressed")
    
    readFile = open(sys.argv[1], "r")
    allLines = readFile.readlines()

    table = list(allLines)

    w1 = []

    for i in range(0, len(table)):
        l = stripper(table[i])
        if l == [""]:
            continue
        else:
            b = toBinary(l)
            c = toHex(b)

            w1 += [c]
        
    w2 = []

    for j in range(0, len(w1)):
        w2 += [w1[j][:2]]
        w2 += [w1[j][2:]]
        
    d = len(w2)
    e = d // 16
    f = d % 16

    m = 0
    lineCount = 0

    if d == 0:
        makeFile.write("\n" + hex(lineCount)[2:].zfill(4) + ": ")
        for k in range(0, 16):
            makeFile.write("00 ")

    else:

        while m < d:
    
            if m % 16 == 0:    
                makeFile.write("\n" + hex(lineCount)[2:].zfill(4) + ": ")
                makeFile.write(w2[m] + " ")
                lineCount += 16
                
            else:
                makeFile.write(w2[m] + " ")
                
            m += 1


    if m % 16 != 0:

        for p in range(0, 16 - (m % 16)):
            makeFile.write("00 ")

    makeFile.close()
    readFile.close()

    return

if __name__ == "__main__":
    main()
