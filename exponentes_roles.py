import numpy as np
import matplotlib.pyplot as plt
import math

#0.005,0.01,0.03,0.05,0.08,0.09
epsilon = [0.005,0.01,0.015,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09]
N = 1000
w = 6
grado = 6 
ciclo = 200
ponderaciones = 16


mediaemes_h, mediaemes_nh = [], []
desviemes_h, desviemes_nh = [], []

mediabes_h, mediabes_nh = [], []
desvibes_h, desvibes_nh = [], []

###EXTRAIGO LOS VECTORES X, Y, error
for e in epsilon:
    print "EPSILON = ", e
    print "PONDERACIONES = ", ponderaciones
    print " "
    media_ponderaciones_h = []
    media_bes_h = []
    media_ponderaciones_nh = []
    media_bes_nh = []
    for z in range(ponderaciones):
        xh, xnh, errh = [], [], []
        yh, ynh, errnh  = [], [], []
        yhlog, ynhlog = [], []
        with open("Hubs"+str(z)+"Epsilon="+str(e)+".txt","r") as datos:
            lineas = datos.readlines()
            for linea in lineas:
                valores = linea.split("     ")
                xi = float(valores[0])
                yi = float(valores[1])
                erri = float(valores[2].strip("\n"))
                xh.append(xi)
                yh.append(yi)
                yhlog.append(math.log(float(yi)))
                errh.append(erri)
        
        with open("NonHubs"+str(z)+"Epsilon="+str(e)+".txt","r") as datos:
            lineas = datos.readlines()
            for linea in lineas:
                valores = linea.split("     ")
                xi = float(valores[0])
                yi = float(valores[1])
                erri = float(valores[2].strip("\n"))
                xnh.append(xi)
                ynh.append(yi)
                ynhlog.append(math.log(float(yi)))
                errnh.append(erri)
        
        
        
        ##PARA AJUSTAR EL EXPONENCIAL AL GRAFICO##
    
        ###REGRESION LINEAL DEL LOGARITMO DE Y
        #y = b*exp(m*x), log(y) = m*x + log(b)
        
        #6
        maximoquita = 1
        #14
        maximoquitados = 1

        ### ## ## ## ## ## # ## ## ## ## ## # ##
        ## ## ## ## ## ## HUBS ## ## ## ## ## ##
        ### ## ## ## ## ## # ## ## ## ## ## # ##
        xhquitado = xh[:]
        yhquitado = yh[:]
        yhlogqui = yhlog[:]
        #para hacer la regresion quito los q primeros puntos
        
        rh = 0
        mh = 0
        bh = 0
        
        for o in range(maximoquita):
            #del xhquitado[0]
            #del yhquitado[0]
            #del yhlogqui[0]
            
    
            nh = len(xhquitado)
            xh2 = [m**2 for m in xhquitado]
            yhlog2 = [m**2 for m in yhlogqui]
            xhlogyh = [xhquitado[i]*yhlogqui[i] for i in range(nh)]

            sumax = sum(xhquitado)
            sumax2 = sum(xh2)
            sumay = sum(yhlogqui)
            sumay2 = sum(yhlog2)
            sumaxy = sum(xhlogyh)

            #parametros recta
            mo = (sumax*sumay-nh*sumaxy)/(sumax**2-nh*sumax2)
            bo = float(sumay)/float(nh) - mo*float(sumax)/float(nh)

            #errores
            yaxb2h = [(yhlogqui[i]-mo*xhquitado[i]-bo)**2
                    for i in range(len(xhquitado))]
            alfa = (sum(yaxb2h)/(nh-2))
    
            ermh = ((alfa*nh)/(nh*sumax2-sumax**2))**0.5
            erbh = ermh*(sumax2/nh)**0.5
    
            xx = [i-(float(sumax)/float(nh)) for i in xhquitado]
            yy = [i-(float(sumay)/float(nh)) for i in yhlogqui]
            xxyy = [xx[i]*yy[i] for i in range(len(xhquitado))]
            xx2 = [m**2 for m in xx]
            yy2 = [m**2 for m in yy]

            ro = sum(xxyy)/((sum(xx2)**0.5)*(sum(yy2)**0.5))

            if ro > rh:
                rh = ro
                mh = mo
                bh = bo
                
            if rh > 0.995:
                break
            
        media_ponderaciones_h.append(mh)
        media_bes_h.append(bh)

        ## ## ## ## ## ## ## ## ## ## ## ## # ##
        ## ## ## ## ## NON-HUBS ## ## ## ## ## #
        ## ## ## ## ## ## ## ## ## ## ## ## # ##
        xnhquitado = xnh[:]
        ynhquitado = ynh[:]
        ynhlogqui = ynhlog[:]
        rnh = 0
        mnh = 0
        bnh = 0
        
        for t in range(maximoquitados):
            #para hacer la regresion quito los i primeros puntos, miro la mejor performance de r
            #del xnhquitado[0]
            #del ynhquitado[0]
            #del ynhlogqui[0]
            
            nnh = len(xnhquitado)
            xnh2 = [m**2 for m in xnhquitado]
            ynhlog2 = [m**2 for m in ynhlogqui]
            xnhlogynh = [xnhquitado[i]*ynhlogqui[i]
                        for i in range(nnh)]

            sumax = sum(xnhquitado)
            sumax2 = sum(xnh2)
            sumay = sum(ynhlogqui)
            sumay2 = sum(ynhlog2)
            sumaxy = sum(xnhlogynh)

            #parametros recta
            mt = (sumax*sumay-nnh*sumaxy)/(sumax**2-nnh*sumax2)
            bt = float(sumay)/float(nnh) - mt*float(sumax)/float(nnh)

            #errores
            yaxb2nh = [(ynhlogqui[i]-mt*xnhquitado[i]-bt)**2
                    for i in range(len(xnhquitado))]
            alfa = (sum(yaxb2nh)/(nnh-2))
    
            ermnh = ((alfa*nnh)/(nnh*sumax2-sumax**2))**0.5
            erbnh = ermnh*(sumax2/nnh)**0.5

            xx = [i-(float(sumax)/float(nnh)) for i in xnhquitado]
            yy = [i-(float(sumay)/float(nnh)) for i in ynhlogqui]
            xxyy = [xx[i]*yy[i] for i in range(len(xnhquitado))]
            xx2 = [m**2 for m in xx]
            yy2 = [m**2 for m in yy]
    
            rt = sum(xxyy)/((sum(xx2)**0.5)*(sum(yy2)**0.5))
    
            
            if rt > rnh:
                rnh = rt
                mnh = mt
                bnh = bt
                
            if rnh > 0.995:
                break

        media_ponderaciones_nh.append(mnh)
        media_bes_nh.append(bnh)
    
        #print "ponderacion num ", z
        #print "m_h = ", mh, " , b_h = ", bh
        #print "m_nh = ", mnh, " , b_nh = ", bnh
        #print " "
        
        ## ## ## ## ## ## ## ## ## ## ## ## ##
        ## ## ## ## ## GRAFICOS ## ## ## ## ##
        ## ## ## ## ## ## ## ## ## ## ## ## ##
        
        #hubs
        #xhexp = np.linspace(xhquitado[0],max(xh),100)
        xhexp = []
        yhexp = []
        for xii in range(100):
            x = xhquitado[0] + xii*(max(xh)-xhquitado[0])/99
            xhexp.append(x)
            yhexp.append(math.exp(bh)*math.exp(mh*x))
        #yhexp = np.exp(bh)*np.exp(mh*xhexp)
        #nonhubs
        #xnhexp = np.linspace(xnhquitado[0],max(xnh),100)
        xnhexp = []
        ynhexp = []
        for xiii in range(100):
            x = xnhquitado[0] + xiii*(max(xnh)-xnhquitado[0])/99
            xnhexp.append(x)
            ynhexp.append(math.exp(bnh)*math.exp(mnh*x))
        #ynhexp = np.exp(bnh)*np.exp(mnh*xnhexp)

        """
        ###HUBS I NON-HUBS EACH EPSILON###
        plt.figure(3+epsilon.index(e))
        plt.errorbar(xnh,ynh,yerr=errnh,fmt='.',label="z < 2.5")
        plt.errorbar(xh,yh,yerr=errh,fmt='.',label="z > 2.5")
        plt.plot(xnhexp,ynhexp,label="exp("+str("{0:.1f}".format(mnh))+"x) \nR= "+str("{0:.3f}".format(rnh)),alpha=0.3)
        plt.plot(xhexp,yhexp,label="exp("+str("{0:.1f}".format(mh))+"x) \nR= "+str("{0:.3f}".format(rh)),alpha=0.3)
        plt.title("<S(z)> vs. P , epsilon= " + str(e))
        plt.xlim(-0.01,1)
        plt.yscale('log')
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size")
        plt.legend(loc = 2)
        #plt.savefig("csp_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+".png")
        plt.show()
        """
        """
        ###HUBS ALL EPSILON###
        plt.figure(1)
        plt.errorbar(xh,yh,yerr=errh,fmt='.', label="epsilon = " +str(e))
        plt.legend(loc = 2)
        plt.title("<S(z)> vs. P of Hubs")
    
        plt.yscale('log')
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size")
        plt.xlim(-0.01,1)
        #plt.ylim(-0.01*max(cum_h),max(cum_h)+0.05*max(cum_h))
        
        plt.axvline(0.3,linestyle='--')
        plt.axvline(0.75,linestyle='--')
        
        #plt.savefig("csp_HUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+".png")
        plt.show()
    
        ###NON-HUBS ALL EPSILON###
        plt.figure(2)
        plt.errorbar(xnh,ynh,yerr=errnh,fmt='.',label="epsilon = " +str(e))
        plt.legend(loc = 2)
        plt.title("<S(z)> vs. P of Non-Hubs")
        
        plt.yscale('log')
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size") 
        plt.xlim(-0.01,1)
        #plt.ylim(-0.01*max(cum_nh),max(cum_nh)+0.05*max(cum_nh))
        
        plt.axvline(0.05,linestyle='--')
        plt.axvline(0.625,linestyle='--')
        plt.axvline(0.8,linestyle='--')
        #plt.savefig("csp_nonHUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+".png")
        plt.show()
        """
    
    
    print "HUBS"
    #print media_ponderaciones_h
    #print media_bes_h
    np = len(media_ponderaciones_h)
    media_mh = sum(media_ponderaciones_h)/np
    mediasmedia = [emes-media_mh for emes in media_ponderaciones_h]
    mediasmedia2 = [m**2 for m in mediasmedia]
    desvi_mh = ((1./float(np))*sum(mediasmedia2))**0.5
    print "m_h = ", media_mh, " +- ", desvi_mh
    mediaemes_h.append(media_mh)
    desviemes_h.append(desvi_mh)
    
    nbh = len(media_bes_h)
    media_bh = sum(media_bes_h)/nbh
    mediasmedib = [bes-media_bh for bes in media_bes_h] 
    mediasmedib2 = [b**2 for b in mediasmedib]
    desvi_bh = ((1./float(nbh))*sum(mediasmedib2))**0.5
    print "b_h = ", media_bh, " +- ", desvi_bh
    mediabes_h.append(media_bh)
    desvibes_h.append(desvi_bh)
    
    print " "

    print "NON-HUBS"
    #print media_ponderaciones_nh
    #print media_bes_nh
    nq = len(media_ponderaciones_nh)
    media_mnh = sum(media_ponderaciones_nh)/nq
    mediasmedis = [eme-media_mnh for eme in media_ponderaciones_nh]
    mediasmedis2 = [n**2 for n in mediasmedis]
    desvi_mnh = ((1./float(nq))*sum(mediasmedis2))**0.5
    print "m_nh = ", media_mnh, " +- ", desvi_mnh
    mediaemes_nh.append(media_mnh)
    desviemes_nh.append(desvi_mnh)
    
    nbnh = len(media_bes_nh)
    media_bnh = sum(media_bes_nh)/nbnh
    mediasmedinb = [bes-media_bnh for bes in media_bes_nh] 
    mediasmedinb2 = [b**2 for b in mediasmedinb]
    desvi_bnh = ((1./float(nbh))*sum(mediasmedinb2))**0.5
    print "b_h = ", media_bnh, " +- ", desvi_bnh
    mediabes_nh.append(media_bnh)
    desvibes_nh.append(desvi_bnh)
    
    print " "
    
   
###
plt.figure(101)
plt.errorbar(epsilon,mediaemes_h,yerr=desviemes_h,fmt='.',label="z > 2.5 = ")
plt.errorbar(epsilon,mediaemes_nh,yerr=desviemes_nh,fmt='.',label="z < 2.5 = ")
plt.legend(loc = 2)
plt.title("<m> vs. epsilon")
        
#plt.yscale('log')
plt.xlabel("epsilon")
plt.ylabel("exponent") 
#plt.xlim(-0.01,1)
#plt.ylim(-0.01*max(cum_nh),max(cum_nh)+0.05*max(cum_nh))
        
#plt.savefig("csp_nonHUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+".png")
plt.show()


plt.figure(102)
plt.errorbar(epsilon,mediabes_h,yerr=desvibes_h,fmt='.',label="z > 2.5 = ")
plt.errorbar(epsilon,mediabes_nh,yerr=desvibes_nh,fmt='.',label="z < 2.5 = ")
plt.legend(loc = 2)
plt.title("<b> vs. epsilon")
        
#plt.yscale('log')
plt.xlabel("epsilon")
plt.ylabel("exponent") 
#plt.xlim(-0.01,1)
#plt.ylim(-0.01*max(cum_nh),max(cum_nh)+0.05*max(cum_nh))
        
#plt.savefig("csp_nonHUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+".png")
plt.show()
