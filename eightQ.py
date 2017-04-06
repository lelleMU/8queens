#这是一个产生八皇后问题求解的Python程序
import random
import math
from datetime import datetime
def computeH(state):
    h1=0
    for i in range(8):
        for j in range(8):
            if (state[i]==state[j]):
                h1+=1
            if (abs(state[i]-state[j])==abs(i-j)):
                h1+=1
    return h1/2-8

        
class eightqueen:
    #state=[0 for i in range(8)]
    #H=0
    def __init__(self):
        self.state=[0 for i in range(8)]
        self.time_reset=0
        for i in range(8):
            self.state[i]=random.randint(1,8)
        self.H=computeH(self.state)
    def Reset(self):
        self.time_reset+=1
        for i in range(8):
            self.state[i]=random.randint(1,8)
        self.H=computeH(self.state)
    def Set(self,p):
        for i in range(8):
            self.state[i]=p[i]
        self.H=computeH(self.state)
    
    def printstate(self):
        for i in range(8):
            if i<7:                
                print(self.state[i],end = ' ')
            else:
                print(self.state[i])
                
    def move(self,move):
        self.state[move[0]]=move[1]
        self.H=computeH(self.state)

def climbing(state):
    h=computeH(state)
    move=[-1,0]
    for i in range(8):
        for value in range(1,9):
            state_t=state.copy()
            state_t[i]=value
            h_t=computeH(state_t)
            if h_t<h:
                move[0]=i
                move[1]=value
                h=h_t
    return move

def climb(a):
    while climbing(a.state)[0]>=0:
        a.move(climbing(a.state))
    if a.H==0:
        print('find solution')
        a.printstate()
        return True
    else:
        print('fail to find')
        return False
def ifsame(astate,bstate):
    aself=astate.copy()
    roll_right=[0  for i in range(8)]
    roll_left=[0  for i in range(8)]
    roll_upsidedown=[0  for i in range(8)]
    #sym_rl=[0  for i in range(8)]
    #sym_ud=[0  for i in range(8)]
    #sym_cen=[0  for i in range(8)]
    for i in range(8):
        value=astate[i]
        roll_right[value-1]=8-i
        roll_left[8-value]=i+1
        roll_upsidedown[7-i]=9-value
        #sym_rl[i]=9-value 
        #sym_ud[7-i]=value
        #sym_cen[8-value]=8-i
    if bstate==roll_right or bstate==roll_left or bstate==roll_upsidedown or\
       bstate==aself:
        return True
    else:
        return False
        
        
            
def resetclimb(a):
    while climbing(a.state)[0]>=0:
        a.move(climbing(a.state))
    if a.H==0:
        #print('reset',a.time_reset,'times to find solution')
        #a.printstate()
        return True
    else:
        a.Reset()
        resetclimb(a)

def sim_annealing(a):
    T=1
    while T>0:
        state_t=a.state.copy()     
        randomi=random.randint(0,7)
        randomv=random.randint(1,8)
        state_t[randomi]=randomv
        e=a.H-computeH(state_t)
        if e>=0:
            a.move([randomi,randomv])
        else:
            if(random.random()<math.e**(e/T)):
                a.move([randomi,randomv])
        T=T-0.0001
        if a.H==0:
            break
    '''if a.H==0:
        print('find solution')
        a.printstate()'''
    if a.H!=0:
        a.Reset()
        sim_annealing(a)

def removesameones(a):
    removelist=[]
    num=len(a)
    for i in range(num):
        for j in range(num):
            if i<j:
                if ifsame(a[i],a[j]):
                    removelist.append(j)
                    #print('state',i+1,'and state',j+1,'is the same one')
            else:
                pass
    a_new=[a[i] for i in range(num) if i not in removelist]
    return a_new

class population:
    def __init__(self,num_start):
        self.popu=[]
        self.num=num_start
        for i in range(num_start):
            b=eightqueen()
            self.popu.append(b.state)
        self.selected_p=getselected_p(self.popu)
        self.T=1
    def siftings (self):
        total=0
        for each in self.selected_p:
            total+=each
        self.popu=[each for each in self.popu if (28-computeH(each))>(total/self.num)]
        self.selected_p=[each for each in self.selected_p if each>(total/self.num)]
        self.num=len(self.popu)
       
        
    def new_generation(self):
        #self.siftings()
        popu_new=[]
        for i in range(int(self.num/2)):
            popu_new.append(variation(crossover(select(self.selected_p,self.popu))[0],self.T))
            popu_new.append(variation(crossover(select(self.selected_p,self.popu))[1],self.T))
        self.popu=popu_new.copy()
        #self.num=self.num+int(self.num/2)*2
        self.num=len(self.popu)
        self.selected_p=getselected_p(self.popu)
        self.T-=0.0001
                

def select(selected_p,popu):
    s_range=[0]
    selected=[]
    num=0
    for i in range(len(selected_p)):
            s_range.append(selected_p[i]+s_range[i])
    while(num<2):
        a=random.sample(range(int(s_range[-1])),1)
        for i in range(len(selected_p)):
            if s_range[i]<=a[0]<s_range[i+1]:
                if(popu[i] not in selected):
                    selected.append(popu[i])
                    num+=1
                break
    
    return selected
                
    
def variation(state,T):
    #变异 变异概率初步定在0.1 往好的方向变异
    if T>0:
        state_t=state.copy()     
        randomi=random.randint(0,7)
        randomv=random.randint(1,8)
        state_t[randomi]=randomv
        e=computeH(state)-computeH(state_t)
        if(random.random()<0.1):
            if e>=0:
                state=state_t
            else:
                if(random.random()<math.e**(e/T)):
                    state=state_t
    
        return state

def getselected_p(population):
    fitness=[]
    fit_total=0
    for each in population:
        fit=28-computeH(each)
        #if fit<5:#直接筛选
           # fit=0
        fit_total+=fit
        fitness.append(fit)    
    selected_p=[each for each in fitness]
    return selected_p

def crossover(a):
    #繁殖产生后代
    c=[]
    c.append([each for each in a[0][:3]]+[each for each in a[1][3:]])
    c.append([each for each in a[1][:3]]+[each for each in a[0][3:]])
    return c
           
def genetic(num_start):
    start=datetime.now()
    breakflag=0
    a=population(num_start)
    while True:
        for j in range(a.num):
            if a.selected_p[j]==28:
                print(a.popu[j])
                breakflag=1
                end=datetime.now()
                print('用时',end-start)
                break
        if breakflag==1:
            break
        a.new_generation()
            
    

def generatesolution(num,flag):#flag是1的时候选用重启爬山法，是2则用模拟退火
    a=[]                                     #是3则用遗传算法
    n=0                                    #num是产生问题解决个数
    num_total=0
    if flag==2:
        while n<num:
            b=eightqueen()
            sim_annealing(b)
            num_total+=1
            a.append(b.state)
            a=removesameones(a).copy()
            n=len(a)
            
        
    if flag==1:
        while n<num:
            b=eightqueen()
            resetclimb(b)
            num_total+=1
            a.append(b.state)
            a=removesameones(a).copy()
            n=len(a)
    num_remove=num_total-num
    print('remove',num_remove,'repeating solutions')
        
    return a
        
        
        
    
    


	
    
    
    




