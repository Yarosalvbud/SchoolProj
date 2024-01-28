from collections import Counter
import math
def encode(vxod):
    massiv = file(vxod)
    cycle(massiv, vxod)
    
def file(vxod):
    f = open(vxod, 'r', encoding='utf8').readlines()
    massiv = ''
    for s in f:
        massiv += s
    return massiv  
def to_two(a):
        s = ''
        while a != 1.0 and a < 2:
            if int(a) == 0:
                a = a * 2
                s += str(int(a))
            elif int(a) == 1:
                a = (a - int(a)) * 2
                s += str(int(a))
            if a == 0:
                return "0." + str(a) + "00000000000000000000"
        return "0." + s + "000000000000000000000"
def to_ten(a):
        c = 0
        for i in range(len(a)):
            c += int(a[i]) * (2 ** (len(a) - 1 - i))
        return c
    
def cycle(massiv, vxod):
    percent = len(massiv)
    stroka = massiv
    massiv += '$'
    massiv = Counter(massiv)
    massiv = dict(massiv)
    massiv = dict(sorted(massiv.items(), key=lambda item: item[1], reverse=True))
    for i in massiv:
        massiv[i] = massiv[i] / percent
    values_ = []
    
    for i in massiv:
        values_.append(massiv[i])
    new_values = values_.copy()
    values_[1] = values_[0]
    values_[0] = 0.0
    
    for i in range(len(values_)):
        values_[i] = sum(new_values[0:i])
        
    for i in range(len(values_)):
        values_[i] = to_two(values_[i])
    
    for i in range(len(new_values)):
        new_values[i] = abs(math.log2(new_values[i]))
        new_values[i] = math.ceil(new_values[i])
    
    for i in range(len(values_)):
        values_[i] = values_[i][2:]
        values_[i] = values_[i][0:new_values[i]]
    
    keys_ = []
    for elem in massiv:
        keys_.append(elem)
    
    final_s = dict()
    for elem in range(len(keys_)):
        final_s[keys_[elem]] = values_[elem]
    stroka = list(stroka)
    string = ''
    new_massiv = dict()
    
    for i in range(len(keys_)):
        new_massiv[keys_[i]] = values_[i]
        
    for i in stroka:
        string += new_massiv[i]
    stroka = string
    
    for i in range(len(stroka)):
        if len(stroka) % 8 != 0:
            stroka += "0"
    knife = []
    for i in range(0, len(stroka), 8):
        knife.append(stroka[i:i+8])
    to_bit = []
    for i in range(len(knife)):
        to_bit.append(to_ten(knife[i]))
    z = open(vxod.split('.')[0]+'.prar', 'wb')
    to_byte = bytes(to_bit)
    z.write('|||'.encode())
    for i in range(len(keys_)):
        z.write("{".encode() + (ord(keys_[i])).to_bytes(2, 'big') + ":".encode() + values_[i].encode() + "}".encode())
    z.write('|||'.encode())
    z.write(to_byte)
    z.close()
