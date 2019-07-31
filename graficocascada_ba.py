from prettyplotlib import plt
import numpy as np

#datos a graficar
e = []
k = []
c = []

z = []


for epsilon in range(54):
    e.append(10**(-0.05*epsilon))
for grado in range(20):
    k.append(2+grado)

with open("ciclos_ba.txt","r") as datos:
    lineas = datos.readlines()
    for linea in lineas:
        valores = linea.split("     ")
        ciclo = valores[2]
        ciclo.strip("\n")
        #print "k", valores[0], "epsilon", valores[1], "ciclo", ciclo
        if float(ciclo) > 175.:
            ciclo = 175.
        if float(ciclo) == 0:
            ciclo = -25.
        #print int(valores[0])%2
        c.append(float(ciclo))
        

for medios in range(len(c)):
    mee = medios%2
    if mee == 1:
        print "viejo-1=", c[medios-1]
        print "viejo0=", c[medios]
        nuevo_c = (c[medios] + c[medios-1])/2.
        c[medios-1] = nuevo_c
        c[medios] = nuevo_c
        print "nuevo-1=", c[medios-1]
        print "nuevo0=", c[medios]

#print len(k)
#print len(e)
#print len(c)


for b in range(len(k)):
    za = []
    for a in range(len(e)):
        if a != len(e)-1:
            za.append(c[b+len(k)*a])
    z.append(za)
    
z = np.array(z)

#print z

#se consegue x e y (matrices) directamente conseguia
#X,Y = np.meshgrid(e,k)

#   print z


fig, ax = plt.subplots()

cax = ax.pcolor(e,k,z,vmin=-25,vmax=175., cmap=('hot_r'))
plt.xscale('log')
plt.axis([1, 0.00223872113857, 2, 21])
plt.ylabel('<k>', rotation='vertical')
plt.xlabel(u'\u03B5')
plt.yticks([2,4,6,8,10,12,14,16,18,20])
cbar = fig.colorbar(cax,ticks=[0,25,50,75,100,125,150,175])
cbar.ax.set_yticklabels([0,25,50,75,100,125,150,'N.C.'])


plt.show()

