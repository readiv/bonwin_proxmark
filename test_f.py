name_file = "uin_key_ff.txt"

# 0000003c	e3fcf9dfe7f4

n_byte_uid = 0 # Номер стартового байта. Нумерация с 0,2,4,6
n_byte_key = n_byte_uid # Номер стартового байта. Нумерация с 0

key_00000000 = "00 00 00 00\tdf fc f9 df df cc"

def get_bit(uid_key: str):  # Возвращает номер байта и бит
    """ На входе строка вида 00 00 00 00\tdf fc f9 df df cc
        На выходе часть uid вырезаная в зависимости от n_byte_uid
        и приведенная к int.
        так же на выходе бит вырезаный из key в зависимости от 
        n_byte_key и mask_bit
    """
    uid = uid_key.replace(' ', '').split("\t")
    key = int(uid[1][n_byte_key: n_byte_key + 2], 16)
    uid = int(uid[0][n_byte_uid: n_byte_uid + 2], 16)
    return uid, key


def get_str_of_bit(x: int): # Возвращает текстовую строку множителей по байту. То есть элементы разложения Жигалкина
    """ На входе байт x
        На выходе строка вида b7*b5*b0
    """
    strbit = ""
    if x:
        for i in range(8):
            if x & (1 << i):
                strbit = f"*b{i}" + strbit
    else:
        strbit = "1"
    if strbit[0] == "*":
        strbit = strbit[1:]
    return strbit


def get_str_of_bit_2(x: int): # Возвращает текстовую строку множителей по байту.
    """ На входе байт x
        На выходе строка вида 01000110
    """
    strbit = ""
    for i in range(8):
        if x & (1 << i):
            strbit = "1" + strbit
        else:
            strbit = "0" + strbit
    return strbit


def func01(x: int): #Проверка 1-го байта
    if x >= 0x64:
        y = 0x20 ^ x | 0x04
    else:
        y = 0xdf ^ x | 0x04
    return y


def func02(x: int): #Проверка 2-го байта
    if x >= 0x64:
        y = 0x20 ^ x | 0x03
    else:
        y = 0xdc ^ x | 0x03
    return y


def func03(x: int): #Проверка 3-го байта
    if x >= 0x64:
        y = 0x04 ^ x & 0xfd
    else:
        y = 0xf9 ^ x & 0xfd
    return y


def func04(x: int): #Проверка 4-го байта
    if x >= 0x64:
        y = 0x02 ^ x & 0xfe
    else:
        y = 0xfc ^ x & 0xfe
    return y


def func_test(x, x1, x2, x3, x4):
    if x >= x1:
        y = x2 ^ x & x4
    else:
        y = x3 ^ x & x4
    return y


if __name__ == '__main__':
    pif = [0] * 256
    
    with open(name_file, 'r') as f:
        for line in f:
            uid, key = get_bit(line)
            pif[uid] = key

    for x1 in range(99,256,1):
        print(x1)
        for x2 in range(256):
            for x3 in range(256):
                for x4 in range(256):
                    testOk = True
                    for x in range(256):
                        if pif[x] != func_test(x, x1, x2, x3, x4):
                            testOk = False
                            break
                    if testOk:
                        print(f"x1 = {x1} \t x2 = {x2} \t x3 = {x3} \t x4 = {x4} \t ")

    # for x in range(256):
    #     print(get_str_of_bit_2(x), get_str_of_bit_2(pif[x]))


    # testOk = True
    # for x in range(256):
    #     if pif[x] != func04(x):
    #         testOk = False
    #         break
    # if testOk:
    #     print(f"ok!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
