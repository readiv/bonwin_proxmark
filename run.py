from subprocess import Popen, PIPE
from time import sleep, time
from random import randint
com_port = "com5"


class Profiler(object):
    def __enter__(self):
        self._startTime = time()
         
    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time() - self._startTime))


def get_key(uin):
    key = ""
    try:
        with Popen(["c:\\ProxSpace\\bonwin_proxmark\\iceman\\win64\\proxmark3.exe", com_port],
                   stdout=PIPE, stdin=PIPE, bufsize=-1) as pm3:
            pm3.stdin.write(bytes(f'hf mf sim u {uin} i x e\n', 'cp866'))
            output = pm3.communicate(timeout=20)[0].decode('cp866')
            # print(output)
            output = output.split("\n")
            for line in output:
                if line.find("|015| ") != -1:
                    key = line.split("|")[2].strip()
        if len(key) == 12:
            key = key[:2] + " " + key[2:4] + " " + key[4:6] + " " + key[6:8] + " " + key[8:10] + " " + key[10:] 
    except:
        pass
    return key


if __name__ == '__main__':
    with Profiler() as p:

        # for k in range(0, 8, 2):
        #     for duin in range(1, 256):
        #         uin = hex(duin).split('x')[1]
        #         for j in range(k):
        #             uin = uin + '0'
        #         while len(uin) != 8:
        #             uin = '0' + uin


        # for duin in range(0, 256):
        #     uin = hex(duin).split('x')[1]
        #     while len(uin) != 2:
        #         uin = '0' + uin
        #     uin = uin + uin
        #     uin = uin + uin     
        
        # for duin in range(0, 1000):
        #     uin = ""
        #     for k in range(4):
        #         uint = hex(randint(0,255)).split('x')[1]
        #         while len(uint) != 2:
        #             uint = '0' + uint
        #         uin += uint     

        # for k in range(0, 8, 2):
        #     for nbit in range(0, 8):
        #         uin = hex(1 << nbit).split('x')[1]
        #         for j in range(k):
        #             uin = uin + '0'
        #         while len(uin) != 8:
        #             uin = '0' + uin    
        # 

        for duin in range(1,256):
            uinb = hex(duin).split('x')[1]
            while len(uinb) != 2:
                uinb = '0' + uinb

            for i in range(16):
                uin = "00000000"
                if i:
                    for j in range(4):
                        if i & (1 << j): 
                            uin = uin[0 : 6 - 2 * j ] + uinb + uin[8 - 2 * j : ]

                    key = ""
                    flag = 0
                    while key == "":
                        key = get_key(uin)
                        # sleep(4)
                        flag += 1
                        if flag > 1:
                            print(f"Неудача: Попытка №{flag}")
                        if flag >= 39:
                            raise SystemExit
                else:
                    key = "de fc f9 df de cc"

                with open('uin_key.txt', 'a', encoding='utf-8') as f:
                    f.write(uin + "\t" + key + '\n')
                    print(uin + "\t" + key)
