from prettyplotlib import plt
import numpy as np

#datos a graficar
e = []
k = []
c = []

#si hago matrices
#x = []
#y = []
z = []


for epsilon in range(81):
    e.append(10**(-0.05*epsilon))
for grado in range(20):
    k.append(2+grado)

#si lo hiciera con matrices
"""
for a in range(len(k)):
    x.append(e)
for b in k:
    y.append(len(k)*[b])
"""


with open("ciclos_random.txt","r") as datos:
    lineas = datos.readlines()
    for linea in lineas:
        valores = linea.split("     ")
        ciclo = valores[2]
        ciclo.strip("\n")
        print valores[0], valores[1], ciclo
        if float(ciclo) > 175.:
            ciclo = 175.
        if float(ciclo) == 0:
            ciclo = -25.
        
        c.append(float(ciclo))
            
            
            
print len(k)
print len(e)
print len(c)


for b in range(len(k)):
    za = []
    for a in range(len(e)):
        if a != len(e)-1:
            za.append(c[b+len(k)*a])
    z.append(za)
    
z = np.array(z)

#se consegue x e y (matrices) directamente conseguia
#X,Y = np.meshgrid(e,k)

#   print z

fig, ax = plt.subplots()

cax = ax.pcolor(e,k,z,vmin=-25,vmax=175., cmap=('hot_r'))
plt.xscale('log')
plt.axis([1, 0.0001, 2, 21])
plt.yticks([2,4,6,8,10,12,14,16,18,20])
plt.ylabel('<k>',rotation='vertical')
ax.minorticks_on()
ax.tick_params(axis='y',which='minor',direction='out')
cbar = fig.colorbar(cax,ticks=[0,25,50,75,100,125,150,175])
cbar.ax.set_yticklabels([0,25,50,75,100,125,150,'N.C'])


plt.show()