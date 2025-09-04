import math
import random

def f(p):
  if(len(p)==1):
    return p[0]
  return (((p[0]*f(p[1:]))+1)%2)*(p[0]+f(p[1:]))

def conv(x,b):
  if(x==0):
    z=[]
    for i in range(b):
      z.append(0)
    return z
  m=x
  c=math.floor(math.log(x)/math.log(2))
  r=[]
  while (c>-1):
    v=(m>=2**c)+0
    m-=v*2**c
    r.append(v)
    c-=1
  while(len(r)<b):
    r.insert(0,0)
  return r
  
def genD(p):
  r=[]
  for i in range(2**p):
    di=conv(i,p)
    r.append([di,f(di)])
  return r
pS=2
oS=2
d=genD(pS)

def act(x):
  return 1/(1+math.exp(-x))

def genM(l,r):
  m=[]
  for i in range(len(l)):
    m.append([])
    for j in range(l[i]):
      c=[]
      b=0
      if (i>0):
        for k in range(l[i-1]):
          w=(r%2)*random.random()
          c.append(w)
        b=(r%2)*random.random()  
      m[i].append([0,c,b])
  return m

def startSims(s):
  n=[]
  for i in range(s):
    n.append(genM([pS,3,oS],1))
  return n

simN=10
m=startSims(simN)

def nS(l,c,m):
  r=0
  for i in range(len(m[l][c][1])):
    r+=act(m[l-1][i][0]*m[l][c][1][i])
  if(len(m[l][c][1])>0):
    r/=len(m[l][c][1])
  return r

def predict(p,m):
  for i in range(len(m[0])):
    m[0][i][0]=p[i]
  for i in range(len(m)):
    for j in range(len(m[i])):
      m[i][j][0]=nS(i,j,m)+m[i][j][2]
  
  return [x[0] for x in m[-1]]

def cost(p,o):
  s=0
  for i in range(len(o)):
    s+=((i&f(p))-o[i])**2
  s/=len(o)
  return math.sqrt(s)
def mCost(m):
  s=0
  for i in range(2**len(m[0])):
    p=conv(i,len(m[0]))
    s+=cost(p,predict(p,m))
  return s

eS=0.1

def update(md,ref,e):
  for i in range(1,len(md[ref])):
    for j in range(len(md[ref][i])):
      for k in range(len(md[ref][i][j][1])):
        md[ref][i][j][1][k]+=e*(random.random()-1/2)
        md[ref][i][j][2]+=e*(random.random()-1/2)
      
  return True

def nextG(m,s):
  costs=[]
  for i in range(len(m)):
    costs.append([i,mCost(m[i])])
  costs.sort(key=lambda x: x[1])
  return [x[0] for x in costs[:s]]
  
nG=nextG(m,3)

def pick(l):
  r=random.random()*len(l)*(len(l)+1)/2
  print(r)
  return len(l)-math.ceil((-1+math.sqrt(1+8*r))/2)
  # return math.floor((2*len(l)+1+math.sqrt((2*len(l)+1)cos()**2-8*r))/2)
  
def uPick(l):
  return math.floor(random.random()*len(l))

def genNext(s,m,n,v):
  r=[]
  for i in range(n):
    ref=s[uPick(s)]
    update(m,ref,v)
    r.append(m[ref])
  return r

def aCost(md):
  s=0
  for i in range(len(md)):
    s+=mCost(md[i])
  return s/len(md)

def iterate(m,n,v):
  for i in range(n):
    m=genNext(nG,m,len(m),v)
    print(aCost(m))
  return True
print(aCost(m))
iterate(m,15,0.01)
