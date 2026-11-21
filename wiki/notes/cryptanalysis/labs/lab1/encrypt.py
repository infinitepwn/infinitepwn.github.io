from copy import *
import random
import time
class myEnigma:
    def __init__(self, rotors, reflector) -> None:
        """
        初始化转子及反射器
        Args:
            rotors: 转子列表, 从高速到低速
            reflector: 反射器
        """
        self.Rotor_left  = [[i for i in range(26)] for j in range(len(rotors))]
        self.Rotor_right = copy(rotors)
        self.rotors      = copy(rotors)
        self.reflector   = reflector

    def setRotor(self, K2):
        """
        设置转子密钥
        Args:
            K2: 转子位置密钥
        """
        self.count = 0
        for i in range(len(self.Rotor_left)):
            self.Rotor_right[i] = self.Rotor_right[i][K2[i]:] + self.Rotor_right[i][:K2[i]]
            self.Rotor_left[i] = self.Rotor_left[i][K2[i]:] + self.Rotor_left[i][:K2[i]]
    
    def resetRotor(self):
        """
        重制转子位置
        """
        self.count = 0
        self.Rotor_left  = [[i for i in range(26)] for j in range(len(self.rotors))]
        self.Rotor_right = copy(self.rotors)
        
    def updateRotor(self):
        """
        模拟转动一次
        """   
        self.count = self.count + 1
        self.Rotor_left[0]  = self.Rotor_left[0][25:] + self.Rotor_left[0][:25]
        self.Rotor_right[0] = self.Rotor_right[0][25:] + self.Rotor_right[0][:25]
        if self.count % 26 == 0:    #快速转子每转26次, 中速转子转一次, 即左移一次
            self.Rotor_left[1] = self.Rotor_left[1][25:] + self.Rotor_left[1][:25]
            self.Rotor_right[1] = self.Rotor_right[1][25:] + self.Rotor_right[1][:25]
        if self.count % (26*26) == 0: #中速转子每转26次, 慢速转子转一次, 即左移一次
            self.Rotor_left[2] = self.Rotor_left[2][25:] + self.Rotor_left[2][:25]
            self.Rotor_right[2] = self.Rotor_right[2][25:] + self.Rotor_right[2][:25]
        
    def encrypt(self, plaintext,  K1):
        """
        主加密功能
        Args:   
            plaintext: 明文字符串
            K1: 插线板密钥
        Return:
            c: 密文字符串    
        """
        plaintext = plaintext.upper()#统一大写
        plaintext = list(plaintext)
        ciphertext = []
        for m in plaintext:
            m = ord(m) - ord('A')
            m = K1[m]#过接线板
            for i in range(3):
                m = self.Rotor_right[i].index(self.Rotor_left[i][m])#过转子
            m = self.reflector[m]#过反射器
            for i in range(3):
                m = self.Rotor_left[2 - i].index(self.Rotor_right[2 - i][m])#逆向过转子
            m = K1[m]#过接线板
            self.updateRotor()#每加密一个字母, 更新转子
            ciphertext.append(chr(m + ord('A')))
        return ''.join(ciphertext)

random.seed(202698) # 设置日期为种子

def _generate_random_m(n=6):
    # 生成随机明文供测试
    # n表示明文长度，默认与测试明文长度相同
    temp = []
    for i in range(n):
        temp.append(chr(random.randint(0,25) % 26 + ord('A')))
    return ''.join(temp)

def test_efficiency(S,QUICK,MID,SLOW,T,K2,n=1000):
    # 进行n=1000次加密随机明文测试效率
    E=myEnigma([QUICK, MID, SLOW], T)
    E.setRotor(K2)
    M = [_generate_random_m() for _ in range(n)]
    print("开始测试Enigma加密效率...")
    start = time.perf_counter()
    for m in M:
        c = E.encrypt(m,S)
    end = time.perf_counter()
    print(f"{n}次加密完成，总耗时:{end-start:.4f} s")
    print(f"平均每秒加:{n/(end-start):.1f}条")


if __name__=="__main__": 
    ## S = [AV BS CG MN OX]
    S = [21,18,6,3,4,5,2,7,8,9,10,11,13,12,23,15,16,17,1,19,20,0,22,14,24,25]
    QUICK = [7, 19, 3, 22, 11, 25, 14, 1, 16, 23, 8, 20, 5, 17, 12, 9, 24, 6, 15, 2, 18, 21, 4, 13, 10, 0]
    MID = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]
    SLOW = [0, 23, 5, 12, 18, 3, 21, 9, 14, 1, 17, 6, 24, 11, 20, 4, 15, 8, 22, 7, 19, 13, 2, 16, 10, 25]
    T = [5, 3, 7, 1, 8, 0, 9, 2, 4, 6, 12, 14, 10, 15, 11, 13, 18, 20, 16, 21, 17, 19, 24, 25, 22, 23]
    K2 = [8,9,10]
    # E=myEnigma([QUICK, MID, SLOW], T)
    # E.setRotor(K2)
    # plaintext="WETTER"
    # ciphertext=E.encrypt(plaintext, S)
    # print(ciphertext)
    test_efficiency(S,QUICK,MID,SLOW,T,K2)

    
