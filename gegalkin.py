# -*- coding: utf-8 -*-
name_file = "uin_key_ff.txt"

# 0000003c	e3fcf9dfe7f4

n_byte_uid = 0 # Номер стартового байта. Нумерация 0,2,4,6
n_byte_key = n_byte_uid # Номер стартового байта. Нумерация с 0

key_00000000 = "00 00 00 00\tdf fc f9 df df cc"


def get_bit(uid_key: str, i_mask_bit: int = 0 ):  # Возвращает номер байта и бит
    """ На входе строка вида 00 00 00 00\tdf fc f9 df df cc
        На выходе часть uid вырезаная в зависимости от n_byte_uid
        и приведенная к int.
        так же на выходе бит вырезаный из key в зависимости от 
        n_byte_key и i_mask_bit
    """
    uid = uid_key.replace(' ', '').split("\t")
    key = 0
    if int(uid[1][n_byte_key: n_byte_key + 2], 16) & (1 << i_mask_bit):
        key = 1
    uid = int(uid[0][n_byte_uid: n_byte_uid + 2], 16)
    return uid, key

def get_subscript_unicode(n):
    codes = {
        0 : u"\u2080",
        1 : u"\u2081",
        2 : u"\u2082",
        3 : u"\u2083",
        4 : u"\u2084",
        5 : u"\u2085",
        6 : u"\u2086",
        7 : u"\u2087",
        8 : u"\u2088",
        9 : u"\u2089"
    }
    return codes[n]


def get_str_of_bit(x: int): # Возвращает текстовую строку множителей по байту. То есть элементы разложения Жигалкина
    """ На входе байт x
        На выходе строка вида b7*b5*b0
    """
    strbit = ""
    if x:
        for i in range(8):
            if x & (1 << i):
                strbit = u"x" + get_subscript_unicode(i) + strbit
    else:
        strbit = "1"
    # if strbit[0:3] == " * ":
    #     strbit = strbit[3:]
    return strbit


def get_str_of_bit_2(x: int): # Возвращает текстовую строку множителей по байту. То есть элементы разложения Жигалкина
    """ На входе байт x
        На выходе строка вида 01000110
    """
    strbit = f" - {x}"
    for i in range(8):
        if x & (1 << i):
            strbit = "1" + strbit
        else:
            strbit = "0" + strbit
    return strbit
        


if __name__ == '__main__':
    # print(get_str_of_bit(255))
    for i_mask_bit in range(8):
        pif = []
        for i in range(256, 0, -1):
            pif.append([0] * i)
        # print(pif[0])
        # print("\n")

        with open(name_file, 'r') as f:
            for line in f:
                uid, key = get_bit(line, i_mask_bit)
                if uid: 
                    pif[0][uid] = key

        uid, key = get_bit(key_00000000, i_mask_bit)
        pif[0][uid] = key

        #Считаем треугольник пифагора

        for row in range(1, 256):
            for i in range(256 - row):
                if pif[row - 1][i] != pif[row - 1][i + 1]:
                    pif[row][i] = 1

        sy = u"y" + get_subscript_unicode(i_mask_bit) + u" =" 
        for row in range(256):
            if pif[row][0]:
                if sy[-1] == "=":
                    sy += " " + get_str_of_bit(row)
                else:
                    sy += u"\u2295" + get_str_of_bit(row)

        print("==============================================================")
        print(sy)

        with open('byte02.txt', 'a', encoding='utf-16') as f:
            f.write(sy + '\n\n')


