def decode(vxod):
    file(vxod)
    
def file(vxod):
    file = open(vxod, 'rb')
    to_encode = bytes()
    line = True
    while line:
        line = file.readline()
        to_encode += line
    file.close()
    to_encode = to_encode[3:]
    eix = to_encode.index(b'|')
    if to_encode[eix: eix + 3] == b'|||':
       f = to_encode[0:eix]
    else:
        eix = eix + to_encode[eix:].index('|')
    byte_tex = to_encode[eix + 3:]
    f = f[1:-1]
    alphabet = f.split(b"}{")
    bit = dict()
    for i in alphabet:
        key = i[0:2]
        value = i[3:]
        value = value.decode()
        key = (chr(int.from_bytes(key, "big")))
        bit[value] = key
    byte_tex = list(byte_tex)
    for i in range(len(byte_tex)):
        num = bin(byte_tex[i])[2:]
        if len(num) != 8:
            num = "0" * (8 - len(num)) + num
        byte_tex[i] = num
    byte_tex = ''.join(byte_tex)
    real_text = ''
    stop = ''
    for i in range(len(byte_tex)):
        real_text += byte_tex[i]
        if real_text in bit:
            stop += bit[real_text]
            real_text = bit[real_text]
            if real_text == '$':
                break
            real_text = ''
    z = open(vxod.split('.')[0]+'.txt', 'w')
    z.write(stop)
    z = z.close()
