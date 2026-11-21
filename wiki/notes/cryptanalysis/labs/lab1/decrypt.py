import string
from copy import *
from collections import defaultdict
from itertools import permutations
def crypt_once(I, II, III, T, st0, st1, st2, ch):
    """
    在指定三个转子位置下，只加密一个字符。
    Args:
        I: 快速转子
        II:   中速转子
        III:  慢速转子
        T:     反射器
        st0: 快速转子当前位置
        st1: 中速转子当前位置
        st2: 慢速转子当前位置
        ch: 输入字符，如 'A'
    Return:
        加密后的字符，如 'G'
    """

    # A -> 0, B -> 1, ...
    x = ord(ch) - ord('A')

    rotors = [I, II, III]
    positions = [st0, st1, st2]
    rotor_left = []
    rotor_right = []
    # 根据当前位置旋转三个转子
    for rotor, pos in zip(rotors, positions):
        pos %= 26
        left = list(range(26))
        left = left[pos:] + left[:pos]
        right = rotor[pos:] + rotor[:pos]
        rotor_left.append(left)
        rotor_right.append(right)
    # 过三轮
    for i in range(3):
        x = rotor_right[i].index(
            rotor_left[i][x]
        )
    x = T[x]
    #逆向过三轮
    for i in range(2, -1, -1):
        x = rotor_left[i].index(
            rotor_right[i][x]
        )
    return chr(x + ord('A'))
def find_crib(c,m):
    """
        查找crib
        Args:   
            m: 明文字符串
            c: 密文字符串
        Return:
            cribs: 所有可用cribs    
    """
    
    # find the crib
    cribs = []
    maxl = len(c) - len(m) + 1
    ccount = 0 #密文起始点
    flag = 0
    while(ccount < maxl):
        temp_c = c[ccount : ccount + len(m)]
        ccount = ccount + 1
        for i in range(len(m)):
            if m[i] == temp_c[i]: # 有重复的, 一定不是crib
                flag = 1
                break
        if flag == 0:
            cribs.append(temp_c)
        else:
            flag = 0
    return cribs            


def build_graph(c,m):  #邻接表
    """
        查找crib
        Args:   
            m: 明文字符串
            c: 密文字符串
        Return:
            graph: 用于dfs的图, 边权为位置    
    """
    graph = {}
  # 遍历所有的边
    for l,uv  in  enumerate(zip(c,m)):
        u, v=uv
    # 如果u不在字典中, 就创建一个空列表
        if u not in graph:
            graph[u] = []
    # 把(v, l)这个元组添加到u的邻接列表中, 边权l是边的坐标 坐标就是索引，l=0就是c的第一个字母
        graph[u].append((v, l))
    for l, uv in  enumerate(zip(m,c)):
        u, v=uv  
    # 如果u不在字典中, 就创建一个空列表
        if u not in graph:
            graph[u] = []
    # 把(v, l)这个元组添加到u的邻接列表中, 边权l是边的坐标
        graph[u].append((v, l))
  # 返回字典
    return graph


def dfs(graph,pos,st,path,locs): # 从左到右依次为构建的无向图, 输入位置字符, 开始位置字符和坐标, 路径, 记录的环路构成边的坐标
    """
        查找crics
        Args:   
            graph: build graph得到的图
            pos: 当前遍历的字符
            st:开始位置字符和坐标
            path:路径
            locs:记录的环路构成边的坐标
        Return:
            ans: 所有可用crics    
    """

    ans=[]
    for i,l in graph[pos]:
        if i in path :
            tmp=(path[path.index(i):]+[i],locs[path.index(i):]+[l])
            if len(set(tmp[1]))>=2 and st[0] not in tmp[0][1:-1] and tmp[1][-1]==st[1]:
                ans+=[(tuple(tmp[0]),tuple(tmp[1]))]
            continue
        ans+=dfs(graph,i,st,path+[i],locs+[l])
    return ans
def dec(c, K1, K2, I, II, III, T):
    result = ""
    for loc,ch in enumerate(c):
        if ch not in K1:
            result += "?"
            continue
        trans = K1[ch]
        trans = crypt_once(I,II,III,T,K2[0]-loc,K2[1],K2[2],trans)
        if trans not in K1:
            result += "?"
            continue
        result += K1[trans]
    return result

I = [7, 19, 3, 22, 11, 25, 14, 1, 16, 23, 8, 20, 5, 17, 12, 9, 24, 6, 15, 2, 18, 21, 4, 13, 10, 0]
II = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]
III = [0, 23, 5, 12, 18, 3, 21, 9, 14, 1, 17, 6, 24, 11, 20, 4, 15, 8, 22, 7, 19, 13, 2, 16, 10, 25]
T = [5, 3, 7, 1, 8, 0, 9, 2, 4, 6, 12, 14, 10, 15, 11, 13, 18, 20, 16, 21, 17, 19, 24, 25, 22, 23]

if __name__=="__main__": 
    m="WETTERVORHERSAGEHEUTE"
    c="EWGZDSATLWNEDBBCJUNGW"
    cribs=find_crib(c,m)
    print("总的crib数量: ", len(cribs))
    for crib in cribs:
        print()
        print("当前crib为: ", crib)
        ans=set()  # 保存当前crib中包含的所有环路
        graph=build_graph(crib,m)
        visited=[0]*len(m)
        for i in range(len(m)):
            if visited[i]==1:
                continue    
            ansi=dfs(graph,m[i],(m[i],i),[m[i]],[])
            for find_ins in ansi:
                for loc in find_ins[1]: # 防止重复计算
                    visited[loc]=1    
            ans|=set(ansi)        
        print("当前crib包含的所有环路有: ", ans)
        rotors = {'I': I, 'II': II, 'III': III}

        for num,names in enumerate(permutations(rotors), 1):
            I, II, III = [rotors[name] for name in names]
            print(f"【{num}】当前扰频器组合为:", *names)
            guess = {}
            guess_all_K2 = {(i, j, k) for i in range(26) for j in range(26) for k in range(26)} # 从所有备选中进行筛选
            for case in ans:
                guess_case = {} #存放这个case用的K2
                for i in range(26):
                    for j in range(26):
                        for k in range(26):
                            K2 = (i,j,k) #遍历k2
                            paths = []
                            for check in string.ascii_uppercase:
                                trans = check
                                path = [trans]
                                for z in case[1]:
                                    trans = crypt_once(I, II, III, T, (i-z)%26, j, k, trans)
                                    path.append(trans)
                                if trans == check:
                                    paths.append(path)
                            if paths:
                                guess_case[K2] = paths
                guess_all_K2 &= set(guess_case) #把每次case的K2都取交集
                guess[case] = guess_case   #记录路径，guess[case][K2]就能查找这个环的路径
            print("通过环路猜测的K2密钥个数: ",len(guess_all_K2))
            guess_K2_K1 = {}
            for K2 in guess_all_K2:
                all_K1 = [{}]   #整体的K1,每个case我们能找到一些K1，相当于先存到这里，然后再下一个case里直接对这个测试
                for case in ans:  #找环路,要在每个环路里面找K1
                    possible_K1 = []
                    for path in guess[case][K2]:   #找L0,L1,..
                        for K1_now in all_K1: #初始就是{}，空集
                            flag = True
                            K1 = K1_now.copy() #我们后面会改K1，这里得copy一下
                            for real,pluged in zip(case[0],path):
                                if real not in K1: #如果K1里没有这个明文，就加进去，然后让他和Li连接
                                    K1[real] = pluged
                                elif K1[real] != pluged: #如果有了，但是不是Li，那就矛盾了
                                    flag = False
                                    break
                                if pluged not in K1:  #反过来对Li也是一样的
                                    K1[pluged] = real
                                elif K1[pluged] != real:
                                    flag = False
                                    break
                            if flag:
                                possible_K1.append(K1) #找到符合这个环路的K1
                    all_K1 = possible_K1  #把可能的K1放进去
                    if len(all_K1) == 0:
                        break
                if len(all_K1) > 0:
                    guess_K2_K1[K2] = all_K1
            print("通过环路及与环路相关的接线板设置无冲突, 猜测的K2密钥个数: ",len(guess_K2_K1))
            #带回去推出其他接线板
            final_guess = {}
            for K2 in guess_K2_K1: #固定K2
                for K1 in guess_K2_K1[K2]:  #从K2中取出K1
                    K1_now = K1.copy()
                    ok = True
                    flag = True
                    while flag and ok: #ok是用来看K1有没有矛盾的，有矛盾直接退出，flag就是看有没有更新状态
                        flag = False
                        for loc,pair in enumerate(zip(crib,m)):  #明密文对
                            known = set(pair) & set(K1_now) #取交集，就是找K1里已经有的字母
                            if len(known) != 1: #pair里面就两个字母，如果不等于1，那就是2，就是说都知道，那就不用回复了
                                continue
                            known_char = list(known)[0]
                            unknown_char = pair[0] if pair[1] == known_char else pair[1] #看明密文里面那个不知道
                            plug = crypt_once(I,II,III,T,K2[0]-(loc%26),K2[1],K2[2],K1_now[known_char]) #计算中间状态
                            if unknown_char in K1_now:
                                if K1_now[unknown_char] != plug: #这个中间状态和不知道的那个是相连的，如果不想等，就矛盾
                                    ok = False
                                    break
                            elif plug in K1_now:
                                if K1_now[plug] != unknown_char:
                                    ok = False
                                    break
                            else:
                                K1_now[unknown_char] = plug #如果两个在K1里都没有记录，那就直接添加
                                K1_now[plug] = unknown_char
                                flag = True  #因为获取了K1的新信息，所以flag=1，需要重新看一遍
                        #如果没有获取新信息，说明没法再更新了，直接退出
                    if ok:
                        if K2 not in final_guess:
                            final_guess[K2] = []
                        final_guess[K2].append(K1_now)  #如果没有矛盾就加进去
            print("通过环路及所有可能的接线板无冲突, 猜测的K2密钥个数: ",len(final_guess))
            print("其中接线板总数不超过6条的密钥为: ")
            for K2 in final_guess:
                for K1_now in final_guess[K2]:
                    count = 0
                    K1 = [-1]*26
                    for i in K1_now:
                        if K1_now[i] != i:
                            count += 1
                        K1[ord(i)-ord("A")] = ord(K1_now[i])-ord("A")
                    if count//2 > 6:
                        continue

                    # 已经确定用了6条线，那么剩下的字母只能是不接线
                    if count//2 == 6:
                        for j in range(26):
                            if K1[j] == -1:
                                K1[j] = j
                                ch = chr(j+ord("A"))
                                K1_now[ch] = ch

                    plaintext = dec(c,K1_now,K2,I,II,III,T)
                    print(K2,K1,"接线板条数",count//2)
                    print("解密结果:",plaintext)
                    print("是否正确:",plaintext == m)
