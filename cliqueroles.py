#cascadas cliques

import numpy as np
import matplotlib.pyplot as plt
import math


#1 nodo conexion total 4-clique
e = []
p1, p2, p3, p4, p5 = [],[],[],[],[]

eps = 0.
for i in range(200):
    pro1 = (1. - eps)**4
    pro2 = 4.*eps*(1.-2.*eps)**3
    pro3 = 6.*eps**2*(1.-3.*eps)**2*(1.+2.*(1.-2.*eps)**3/(1.-eps)**3)
    pro4 = 4.*eps**3*(1.-4.*eps)*( 1. + 3.*(1.-3.*eps)**2/(1.-2.*eps)**2 + 3.*(1.-2.*eps)**3/(1.-eps)**3 + 6.*(1.-2.*eps)*(1.-3.*eps)**2/(1.-eps)**3 )
    pro51 = 1. +  4.*(1.-2.*eps)**3/(1.-eps)**3  +  12.*(1.-2.*eps)*(1.-3.*eps)**2/(1.-eps)**3
    pro52 = 12.*(1.-2.*eps)**3*(1.-4.*eps)/((1.-eps)**3*(1.-3.*eps)) + 12.*(1.-3.*eps)*(1.-4.*eps)/(1.-2.*eps)**2
    pro53 = 6.*(1.-3.*eps)**2/(1.-2.*eps)**2  +  4.*(1.-4.*eps)/(1.-3.*eps)  +  24.*(1.-2.*eps)*(1.-3.*eps)*(1.-4.*eps)/(1.-3.*eps)**3
    pro5 = eps**4*(pro51+pro52+pro53)
    eps = eps + 0.001

    e.append(eps)
    p1.append(pro1)
    p2.append(pro2)
    p3.append(pro3)
    p4.append(pro4)
    p5.append(pro5)

plt.figure(1)
plt.title('P(S) vs epsilon')
plt.plot(e,p1,'-',label='p(1)')
plt.plot(e,p2,'-',label='p(2)')
plt.plot(e,p3,'-',label='p(3)')
plt.plot(e,p4,'-',label='p(4)')
plt.plot(e,p5,'-',label='p(5)')
#plt.xlim(0,1)
#plt.savefig(".png")
plt.legend()
#plt.show()


#cascade size distribution
#veo que todos decrecen exponencialmente, diferentes pendientes
e = []
P_S = []

eps = 0.
for i in range(10):
    eps = eps + 0.01
    e.append(eps)
    
    pro1 = (1. - eps)**4
    pro2 = 4.*eps*(1.-2.*eps)**3
    pro3 = 6.*eps**2*(1.-3.*eps)**2*(1.+2.*(1.-2.*eps)**3/(1.-eps)**3)
    pro4 = 4.*eps**3*(1.-4.*eps)*( 1. + 3.*(1.-3.*eps)**2/(1.-2.*eps)**2 + 3.*(1.-2.*eps)**3/(1.-eps)**3 + 6.*(1.-2.*eps)*(1.-3.*eps)**2/(1.-eps)**3 )
    pro51 = 1. +  4.*(1.-2.*eps)**3/(1.-eps)**3  +  12.*(1.-2.*eps)*(1.-3.*eps)**2/(1.-eps)**3
    pro52 = 12.*(1.-2.*eps)**3*(1.-4.*eps)/((1.-eps)**3*(1.-3.*eps)) + 12.*(1.-3.*eps)*(1.-4.*eps)/(1.-2.*eps)**2
    pro53 = 6.*(1.-3.*eps)**2/(1.-2.*eps)**2  +  4.*(1.-4.*eps)/(1.-3.*eps)  +  24.*(1.-2.*eps)*(1.-3.*eps)*(1.-4.*eps)/(1.-3.*eps)**3
    pro5 = eps**4*(pro51+pro52+pro53)
    
    P_S.append([pro1,pro2,pro3,pro4,pro5])
    P_e = []
S = [1,2,3,4,5]
    
plt.figure(2)
plt.title('P(S) vs S')
for i in range(10):
    plt.plot(S,P_S[i],'.',label='epsilon='+str(e[i]))
plt.xlim(0,6)
plt.yscale('log')

#plt.savefig(".png")
plt.legend()
#plt.show()


#calculo la media
#integro, la media sera el punto al que la superficie es la mitad

integral = 0.
for i in range(5):
    integral = integral + P_S[1][i]*1.
    if integral >= 0.5:
        print i
        break

    
    


