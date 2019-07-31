import numpy as np
import matplotlib.pyplot as plt
import math

N_m = 100    #number of modules

xt = []
y = []
ytlog = []

ycum = 1
for i in range(N_m):
    ycum = ycum + i
    xt.append(1-(1./float(i+1)))
    y.append(ycum)
    ytlog.append(math.log(float(ycum)))


x = xt[:]
ylog = ytlog[:]

for i in range(98):
    del x[-1]
    del ylog[-1]

#exponente
n = len(x)

x2 = [xi**2 for xi in x]
ylog2 = [yi**2 for yi in ylog]
xlogy = [x[i]*ylog[i] for i in range(n)]

sumax = sum(x)
sumax2 = sum(x2)
sumay = sum(ylog)
sumay2 = sum(ylog2)
sumaxy = sum(xlogy)

#parametros recta
m = (sumax*sumay-n*sumaxy)/(sumax**2-n*sumax2)
b = float(sumay)/float(n) - m*float(sumax)/float(n)

xexp = []
yexp = []
for xii in range(100):
    xd = 0.2 + xii*(0.5)/99
    xexp.append(xd)
    yexp.append(math.exp(b+1)*math.exp(m*xd))



plt.figure(1)
plt.plot(xt,y,label="")
#plt.plot(xexp,yexp,label="exp("+str("{0:.1f}".format(m))+")",alpha=0.3)
plt.title("P(<S>) vs <S>")
plt.yscale('log')
plt.xlabel("P")
plt.ylabel("<S>")
plt.xlim(0.01,1)
plt.legend(loc=2)
#plt.savefig("csp_HUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+".png")
plt.show()