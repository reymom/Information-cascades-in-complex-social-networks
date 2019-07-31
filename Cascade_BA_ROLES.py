#Cascade Size in function of the role of the node selected
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from mpl_toolkits.mplot3d import Axes3D
import collections
import community

N = 1000
w = 6.
grado = 6
epsilon = [0.015,0.02,0.025]
#0.03: 50
#0.05: 700
#0.07: 1000
#0.08: 1500

ponderaciones = 25

for e in epsilon:
    print "EPSILON=", e
    print " "
    for zeta in range(ponderaciones):
        z = zeta
        print "ponderacion numero ", z
        ## ## ## ## ## ## ## ## CONSTRUCCION DE LA RED, CALCULO VECINOS Y GRADOS INDIVIDUALES ## ## ## ## ## ## ## ##
    
        G = nx.barabasi_albert_graph(N,grado/2)
        maindegree = float(sum(dict(G.degree()).values()))/float(G.number_of_nodes())
        vecinos = list(G.edges())
    
        #redefino los vecinos de una forma mas optima (en cada indice i del vector salen los vecinos del nodo i)
        edges=N*[[]]
        grad=[]
        for i in range(N):
            edges_i=[]
            for a in vecinos:
                if a[0] == i:
                    edges_i.append(a[1])
                if a[1] == i:
                    edges_i.append(a[0])
            edges[i] = edges_i
            grad.append(len(edges_i))
    
    
        ## ## ## ## ## ## ## ## CLASIFICACION DE LOS NODOS SEGUN SU ROL ## ## ## ## ## ## ## ##
    
        ##particion en modulos (comunidades), louvain algoritm
        partition_G = community.best_partition(G)
    
        ##a que modulo pertenece el nodo numerado por el indice del vector
        modulo_nodo_G = partition_G.values()
    
        ##cantidad de modulos que han salido
        num_mod_G = max(modulo_nodo_G) + 1
    
    
        ##############calculos

        z_G = N*[None]
        p_G = N*[None]
    
        #grado medio por modulo
        sumas_intergrados_G = num_mod_G*[0.]
        num_nodos_mod_G = num_mod_G*[0.]
        intralinks_G = N*[0.]

        for i in range(N):
            m = modulo_nodo_G[i]
            num_nodos_mod_G[m] = num_nodos_mod_G[m] + 1.
            for neig in edges[i]:
                if modulo_nodo_G[neig] == m:
                    intralinks_G[i] = intralinks_G[i] + 1.
            sumas_intergrados_G[m] = sumas_intergrados_G[m] + intralinks_G[i]

        media_G = []
        for m in range(num_mod_G):
            media_G.append(float(sumas_intergrados_G[m])/float(num_nodos_mod_G[m]))
    
        #desviacion estandar por modulo
        deviation_G = num_mod_G*[0.]
        for i in range(N):
            m = modulo_nodo_G[i]
            deviation_G[m] = deviation_G[m] + (intralinks_G[i]-media_G[m])**2
        for m in range(num_mod_G):
            deviation_G[m] = (deviation_G[m]/num_nodos_mod_G[m])**(0.5)
        
        ##CALCULO Z
        for i in range(N):
            m = modulo_nodo_G[i]
            if intralinks_G[i] != 0. and deviation_G[m] != 0.:
                z_G[i] = (intralinks_G[i]-media_G[m])/deviation_G[m]
    
        ##CALCULO P
        for i in range(N):
            suma = 0.
            m_i = modulo_nodo_G[i]
            if grad[i] != 0:
                for m in range(num_mod_G):
                    link_hacia_mod_m = 0.
                    for neig in edges[i]:
                        if modulo_nodo_G[neig] == m:
                            link_hacia_mod_m = link_hacia_mod_m + 1.
                    suma = suma + (link_hacia_mod_m/float(grad[i]))**2
                p_G[i] = 1.-suma
    
        """
        print "Informacion nodos de la red con N = ", N
        print " "
        print "Kmax (nodo num", grad.index(max(grad)) ,")= ", max(grad), ", Kmin (nodo num", grad.index(min(grad)) ,")= ", min(grad)
        print "Zmax (nodo num", z_G.index(max(z_G)) ,")= ", max(z_G), ", Zmin (nodo num", z_G.index(min(z_G)) ,")= ", min(z_G)
        print "Pmax (nodo num", p_G.index(max(p_G)) ,")= ", max(p_G), ", Pmin (nodo num", p_G.index(min(p_G)) ,")= ", min(p_G)
        print " "
        print "Modulos resultantes en la particion: ", num_mod_G
        print " "
        """
    
        #para hacer el grafico ordenare los vectores de forma que p_G y z_G se borran, los copio para poder hacer mas simulaciones con otros epsilon
        pcopio = p_G[:]
        zcopio = z_G[:]
    
        ## ## ## ## ## ## ## ## EMPIEZAN SIMULACIONES ESCOBANDO PARAMETRO SELECCIONADO ## ## ## ## ## ## ## ##
    
        p_G = pcopio[:]
        z_G = zcopio[:]
        #print "SIMULACION epsilon = ", e, " ", (epsilon.index(e)+1),"/",len(epsilon)
        
        
        #para GRAFICAR LUEGO
        sizes = N*[0]
        vez_media = N*[0]
        
    
        ### ## ## ## ## ## ## ##
        ###EMPIEZA SIMULACION###
        ### ## ## ## ## ## ## ##
        
        #valores iniciales aleatorios"
        E_i = np.random.rand(N)
        theta_i = (np.exp(w*E_i)-1.)/(np.exp(w)-1.)
          
        ciclo = 0
        
        #lista de variables para cada nodo, el valor asignado al nodo es cero si este ha pasado por la treshold almenos una vez, otherwise es uno
        c = N*[1]
        cascadamayor = []
        nodogatillo = []
        
        #en cada i hay un solo paso de avanzar el mas avanzado y ver como afectan a los vecinos y vecinos de los vecinos hasta que no hay fires
        for i in range(1000000):
            #cuando todos se han activado una vez almenos, es decir cuando su controlador es cero, el ciclo cambia
            if sum(c) == 0:
                ciclo = ciclo + 1
                c = N*[1]
                indicemax = cascadamayor.index(max(cascadamayor))
                nodo_num = nodogatillo[indicemax]
                #print " "
                #print "La mayor cascada en ciclo", ciclo-1, ", ha medido", max(cascadamayor)
                #print "Provocada por nodo numero", nodo_num
                #print "k =", grad[nodo_num]
                #print "(z,P) = ", "(", z_G[nodo_num], ",", p_G[nodo_num], ")"
                del cascadamayor[cascadamayor.index(max(cascadamayor))]
                if len(cascadamayor) > 1:
                    indicemax = cascadamayor.index(max(cascadamayor))
                    nodo_num = nodogatillo[indicemax]
                    #print "La segunda mayor ha medido", max(cascadamayor)
                    #print "Provocada por nodo numero", nodo_num
                    #print "k =", grad[nodo_num]
                    #print "(z,P) = ", "(", z_G[nodo_num], ",", p_G[nodo_num], ")"
                if ciclo == 55:
                    print "50 %"
                
                cascadamayor = []
                nodogatillo = []

                
            ##PRIMER PASO##
            #AVANZO TODOS LOS NODOS HASTA QUE EL MAS AVANZADO LLEGA A LA TRESHOLD"
            Dt = 1. - max(theta_i)
            imax = np.argmax(theta_i)
            #print "Nodo mas avanzado: ", "E _", imax, "=", E_i[imax]

            #el mas avanzado llega a 1, sus vecinos se desplazan el tiempo correspondiente
            for j in range(N):
                if j != imax:
                    E_i[j] = 1./w * np.log(1.+(np.exp(w)-1.)*(theta_i[j]+Dt))

            #EMITE INFORMACION Y SE RESETEA SU CICLO
            E_i[imax] = 0.
            c[imax] = 0
            #print "primer fuego el", imax
            
            #TODOS LOS VECINOS RECIBEN LA INFORMACION
            #los avanzo todos, y
            #los vecinos que van a hacer fire al avanzarse, los pongo en una lista, porque pulsaran al unisono y emitiran informacion simultaneamente
            
            
            #asi se hace, y tiene que ser mas optimo en principio, con la nueva lista de vecinos que he definido con nueva estructura
            fuego = []
            for ki in edges[imax]:
                if (E_i[ki] + e) >= 1.:
                    E_i[ki] = 0.
                    c[ki] = 0
                    fuego.append(ki)
                if (E_i[ki] + e) < 1:
                    E_i[ki] = E_i[ki] + e
                

            ##SEGUNDO PASO##
            #dado el primer fire, tenemos una lista de los vecinos que van a emitir debido al aumento de este primer fire
            #ahora iteraremos este proceso, actualizando la lista de vecinos que van a hacer fire cada vez
            #lo haremos hasta que esta lista, que son los que haran fire, este vacia, hasta que nadie vaya a hacer fire
            
            #variable que controlara cuantos nodos hacen fuego en una iteracion dada i (tamano de la cascada de informacion)
            encendidos = 1
            haranfire = len(fuego)
            bucles = 0
            while haranfire>0:
                bucles = bucles + 1
                encendidos = encendidos + haranfire
                
                #esto no se porque lo pones, las cascadas pueden recorrer mas de una vez la red
                
                if (float(encendidos)/float(N)) >= N:
                    #print "sinc abs en el ciclo", ciclo
                    break
                
                
                #print "en bucle numero", bucles, "haran fuego", fuego

                for firingnode in fuego:
                    for kf in edges[firingnode]:
                        if kf not in fuego:
                            E_i[kf] = E_i[kf] + e
                            
                #vuelvo a mirar los que haran fire
                fuego = []
                for energia in E_i:
                    if energia > 1:
                        nodofuego = E_i.tolist().index(energia)
                        #print "finalmente fuego", nodofuego
                        E_i[nodofuego] = 0.
                        c[nodofuego] = 0
                        fuego.append(nodofuego)
                haranfire = len(fuego)
                #print "RESUMEN FUEGOS en esta iteracion", encendidos
                
                        
                #print "es cierto que ha breaked"
    
            
            cascadesize = encendidos
            
            #para imprimir cascada mayor en cada ciclo y grado del nodo que la ha provocado
            cascadamayor.append(cascadesize)
            #print len(cascadamayor)
            nodogatillo.append(imax)
            
            
            #para los graficos de luego
            sizes[imax] = sizes[imax] + cascadesize
            vez_media[imax] = vez_media[imax] + 1
            
            
            #cuantos ciclos corro
            if e > 0.065:
                if ciclo >= 200:
                    break
            if e < 0.065:
                if ciclo >= 110:
                    break

                
            theta_i = (np.exp(w*E_i)-1.)/(np.exp(w)-1.)



        
        ## ## ## ## ## ## ## ## ##
        ###GRAFICO 1.1 ZP SPACE###
        ## ## ## ## ## ## ## ## ##
        
        #eje x: p_G
        #eje y: z_G
        #eje z o color: sizemid
        

        #sizemedia
        sizemid = []
        for n in range(len(p_G)):
            if sizes[n] != 0:
                sizemid.append(float(sizes[n])/float(vez_media[n]))
            if sizes[n] == 0:
                sizemid.append(0)
                
        #elimino los ceros
        c = collections.Counter(sizemid)
        llevas = 0
        quedan = c[0]
        while quedan > 0:
            llevas = llevas + 1
            elimino = sizemid.index(0)
            del sizemid[elimino]
            del p_G[elimino]
            del z_G[elimino]
            c = collections.Counter(sizemid)
            quedan = c[0]
        
        #Minimo y maximo de cascadesize
        minimosize = max(sizemid)
        for a in range(len(sizemid)):
            if sizemid[a] < minimosize:
                minimosize = sizemid[a]
        print "Cascada media minima=", minimosize 
        print "Cascada media maxima= ", max(sizemid)
        print " "
        
        copia_p_G = p_G[:]
        copia_z_G = z_G[:]
        copia_sizemid = sizemid[:]
        
        #maximo
        solosipasa = 10
        if max(copia_z_G) > 10:
            solosipasa = max(copia_z_G)
            
            
            
        ##    ##    
        ## ZP ##
        ##    ##
        
        """
        plt.figure(z+100*epsilon.index(e))
        plt.scatter(copia_p_G,copia_z_G,c=copia_sizemid,marker='.',cmap='autumn_r')
        plt.title("zP diagram")
        plt.xlabel("Participation coeficient")
        plt.ylabel("Whithin-module degree")
        plt.xlim(-0.009,1)
        plt.ylim(-2.5,solosipasa)
        cl = plt.colorbar()
        cl.ax.set_title("<S>")
        plt.savefig("cszp_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+".png")
        #plt.show()
        

        plt.figure(6969 + epsilon.index(e))
        plt.scatter(copia_p_G,copia_z_G,c=copia_sizemid,norm=LogNorm(vmin=1,vmax=max(copia_sizemid)),marker='.',cmap='autumn_r')
        plt.title("zP diagram")
        plt.xlabel("Participation coeficient")
        plt.ylabel("Whithin-module degree")
        plt.xlim(-0.009,1)
        plt.ylim(-2.5,solosipasa)
        cl = plt.colorbar()
        cl.ax.set_title("<S>")
        plt.savefig("cszp_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+"log.png")
        #plt.show()
        """
        # ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        ##GRAFICO 1.4 ZP CON ALTURA EN VEZ DE COLOR, Y CUMULATIVO EN P##
        # ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        
        #Importante, en lo de cumulativo por la zona de hub y no hub no lo hiciste asi y luego hacer un lio que flipas
        #A parta, trabaja sobre copias, que luego borras originales y copias desordenadamente
        #ORDENO LOS RESULTADOS POR P CRECIENTE
        """

        #ordenado
        pG = copia_p_G[:]
        zG = copia_z_G[:]
        sG = copia_sizemid[:]
        Po,Zo,So = [], [], []
        while len(pG) > 0:  
            izmierda = pG.index(min(pG))
            Po.append(min(pG))
            Zo.append(zG[izmierda]) 
            So.append(sG[izmierda])
            del pG[izmierda], zG[izmierda], sG[izmierda]
            
        #cumulativo en p
        Scum = len(So)*[0]
        for i in range(len(Po)):
            repep = 0
            for j in range(len(Po)-i-1):
                if Po[i+j+1] == Po[i]:
                    repep = repep + 1
                if Po[i+j+1] =! Po[i]:
                    break
            for q in range(repep+1):
                if Zo[q
                
                    
            for k in range(i+1):
                if Zo[k] <= Zo[i]+0.1 and Zo[k] >= Zo[i]-0.1:
                    Scum[i] = Scum[i] + So[k]

        
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_trisurf(Po, Zo, Scum, linewidth=0.1,antialiased=True)
        plt.title("zP vs Cum_S(z)")
        plt.xlabel("Participation coeficient")
        plt.ylabel("Whithin-module degree")
        plt.xlim(0,1)
        plt.ylim(-2.5,solosipasa)
        ax.zaxis.set_scale('log')
        #cl = plt.colorbar()
        #cl.ax.set_title("<S>")
        #plt.savefig("cszp_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+".png")
        plt.show()
        """
        
        
        
        ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        ###GRAFICO 1.3 SUPERFICIES DE ROLES 3D###
        ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        
        #HUBS: z>=2.5
        #regiones p = 0.3, 0.75
        #NON-HUBS: z<2.5
        #regiones p =0.05, 0.625, 0.8
        #a partir de copia_p_G, copia_z_G, copia_sizemid
        
        R1, R2, R3, R4, R5, R6, R7 = [], [], [], [], [], [], []
        s1, s2, s3, s4, s5, s6, s7 = [], [], [], [], [], [], []
        
        #AGRUPO LAS MEDIDAS DE LOS NODOS POR REGIONES
        for i in range(len(copia_z_G)):
            if copia_z_G[i] >= 2.5:
                if copia_p_G[i] < 0.3:
                    R5.append(copia_sizemid[i])
                if copia_p_G[i] >= 0.3 and copia_p_G[i] < 0.75:
                    R6.append(copia_sizemid[i])
                if copia_p_G[i] >= 0.75:
                    R7.append(copia_sizemid[i])
            if copia_z_G[i] < 2.5:
                if copia_p_G[i] < 0.05:
                    R1.append(copia_sizemid[i])
                if copia_p_G[i] >= 0.05 and copia_p_G[i] < 0.625:
                    R2.append(copia_sizemid[i])
                if copia_p_G[i] >= 0.625 and copia_p_G[i] < 0.8:
                    R3.append(copia_sizemid[i])
                if copia_p_G[i] >= 0.8:
                    R4.append(copia_sizemid[i])
        #MEDIA
        mR1,mR2,mR3,mR4,mR5,mR6,mR7 = 0,0,0,0,0,0,0
        if len(R1) > 0:
            mR1 = sum(R1)/len(R1)
        if len(R2) > 0:
            mR2 = sum(R2)/len(R2)
        if len(R3) > 0:
            mR3 = sum(R3)/len(R3)
        if len(R4) > 0:
            mR4 = sum(R4)/len(R4)
        if len(R5) > 0:
            mR5 = sum(R5)/len(R5)
        if len(R6) > 0:
            mR6 = sum(R6)/len(R6)
        if len(R7) > 0:
            mR7 = sum(R7)/len(R7)
            
        #DESVIACION ESTANDAR
        d1,d2,d3,d4,d5,d6,d7 = 0,0,0,0,0,0,0
        if len(R1) > 0:
            for medida in R1:
                d1 = d1 + (medida-mR1)**2
            d1 = ((1./(float(len(R1))))*d1)**0.5
        if len(R2) > 0:
            for medida in R2:
                d2 = d2 + (medida-mR2)**2
            d2 = ((1./(float(len(R2))))*d2)**0.5
        if len(R3) > 0:
            for medida in R3:
                d3 = d3 + (medida-mR3)**2
            d3 = ((1./(float(len(R3))))*d3)**0.5
        if len(R4) > 0:
            for medida in R4:
                d4 = d4 + (medida-mR4)**2
            d4 = ((1./(float(len(R4))))*d4)**0.5
        if len(R5) > 0:
            for medida in R5:
                d5 = d5 + (medida-mR5)**2
            d5 = ((1./(float(len(R5))))*d5)**0.5
        if len(R6) > 0:
            for medida in R6:
                d6 = d6 + (medida-mR6)**2
            d6 = ((1./(float(len(R6))))*d6)**0.5
        if len(R7) > 0:
            for medida in R7:
                d7 = d7 + (medida-mR7)**2
            d7 = ((1./(float(len(R7))))*d7)**0.5

        #eje x
        Ax=[]
        incx = 0.025
        n_x = int(1./incx)
        x = 0.
        for a in range(n_x+1):
            Ax.append(x)
            x = x + incx
        #eje y
        Ay = []
        incy = 2.5
        n_y = int(12.5/incy)
        y = -2.5
        for a in range(n_y+1):
            Ay.append(y)
            y = y + incy
        #eje z
        mROL = []
        dROL = []
        y = -2.5
        for ejey in range(n_y+1):
            x = 0.
            vectorm = []
            vectord = []
            for ejex in range(n_x+1):
                if y < 2.5:
                    if x < 0.05:
                        vectorm.append(mR1)
                        vectord.append(d1)
                    if x >= 0.05 and x < 0.625:
                        vectorm.append(mR2)
                        vectord.append(d2)
                    if x >= 0.625 and x < 0.8:
                        vectorm.append(mR3)
                        vectord.append(d3)
                    if x >= 0.8:
                        vectorm.append(mR4)
                        vectord.append(d4)
                if y >= 2.5:
                    if x < 0.3:
                        vectorm.append(mR5)
                        vectord.append(d5)
                    if x >= 0.3 and x < 0.75:
                        vectorm.append(mR6)
                        vectord.append(d6)
                    if x >= 0.75:
                        vectorm.append(mR7)
                        vectord.append(d7)
                x = x + incx
            y = y + incy
            mROL.append(vectorm)
            dROL.append(vectord)
    
        #print "R1= ", mR1, "R2= ", mR2, "R3= ",mR3, "R4= ", mR4,"R5= ",mR5,"R6= ",mR6,"R7=",mR7
        #print "d1= ", d1, "d2= ", d2,"d3= ", d3,"d4= ", d4,"d5= ", d5,"d6= ", d6,"d7= ", d7
        
        #maximos y minimos para graficos
        
        maximor = max(mROL[0])
        if max(mROL[-1]) > maximor:
            maximor = max(mROL[-1])
        maximod = max(dROL[0])
        if max(dROL[-1]) > maximod:
            maximod = max(dROL[-1])
        
        minimor = 10000000
        valores = [mR1,mR2,mR3,mR4,mR5,mR6,mR7]
        for v in valores:
            if v != 0:
                if v<minimor:
                    minimor = v
        minimod = 10000000
        valores = [d1,d2,d3,d4,d5,d6,d7]
        for v in valores:
            if v != 0:
                if v<minimod:
                    minimod = v
                    
                    
        ##     ##
        ## <S> ##
        ##     ##
        """
        plt.figure(12345+epsilon.index(e)*13)
        im = plt.pcolor(Ax,Ay,mROL,norm=LogNorm(vmin=1,vmax=maximor), cmap=('hot_r'))
        cl = plt.colorbar()
        cl.ax.set_title("<S>")
        plt.axis([0, 1, -2.5, 10])
        plt.axvline(0.3,5./12.5,1,color='green')
        plt.axvline(0.75,5./12.5,1,color='green')
        plt.axvline(0.05,0,5./12.5,color='green')
        plt.axvline(0.625,0,5./12.5,color='green')
        plt.axvline(0.8,0,5./12.5,color='green')
        plt.axhline(y=2.5, color='green')
        plt.savefig("<S>ofROLES_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"logcolor.png")
        #plt.show()
   
        
        plt.figure(123459+epsilon.index(e)*18)
        im = plt.pcolor(Ax,Ay,mROL,norm=LogNorm(vmin=minimor,vmax=maximor), cmap=('hot_r'))
        cl = plt.colorbar()
        cl.ax.set_title("<S>")
        plt.axis([0, 1, -2.5, 10])
        plt.axvline(0.3,5./12.5,1,color='green')
        plt.axvline(0.75,5./12.5,1,color='green')
        plt.axvline(0.05,0,5./12.5,color='green')
        plt.axvline(0.625,0,5./12.5,color='green')
        plt.axvline(0.8,0,5./12.5,color='green')
        plt.axhline(y=2.5, color='green')
        plt.savefig("<S>ofROLES_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"logcolorMIN.png")
        #plt.show()
        
        
        plt.figure(13254)
        im = plt.pcolor(Ax,Ay,mROL,vmin=0,vmax=maximor, cmap=('hot_r'))
        cl = plt.colorbar()
        cl.ax.set_title("<S>")
        plt.axis([0, 1, -2.5, 10])
        plt.axvline(0.3,5./12.5,1,color='green')
        plt.axvline(0.75,5./12.5,1,color='green')
        plt.axvline(0.05,0,5./12.5,color='green')
        plt.axvline(0.625,0,5./12.5,color='green')
        plt.axvline(0.8,0,5./12.5,color='green')
        plt.axhline(y=2.5, color='green')
        plt.savefig("<S>ofROLES_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+".png")
        #plt.show()
        plt.figure(132549)
        im = plt.pcolor(Ax,Ay,mROL,vmin=minimor,vmax=maximor, cmap=('hot_r'))
        cl = plt.colorbar()
        cl.ax.set_title("<S>")
        plt.axis([0, 1, -2.5, 10])
        plt.axvline(0.3,5./12.5,1,color='green')
        plt.axvline(0.75,5./12.5,1,color='green')
        plt.axvline(0.05,0,5./12.5,color='green')
        plt.axvline(0.625,0,5./12.5,color='green')
        plt.axvline(0.8,0,5./12.5,color='green')
        plt.axhline(y=2.5, color='green')
        plt.savefig("<S>ofROLES_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"MIN.png")
        
        ##           ##
        ## DEVIATION ##
        ##           ##
        
        plt.figure(54321)
        plt.pcolor(Ax,Ay,dROL,norm=LogNorm(vmin=1,vmax=maximod), cmap=('hot_r'))
        cl = plt.colorbar()
        cl.ax.set_title("dev_S")
        plt.axis([0, 1, -2.5, 10])
        plt.axvline(0.3,5./12.5,1,color='green')
        plt.axvline(0.75,5./12.5,1,color='green')
        plt.axvline(0.05,0,5./12.5,color='green')
        plt.axvline(0.625,0,5./12.5,color='green')
        plt.axvline(0.8,0,5./12.5,color='green')
        plt.axhline(y=2.5, color='green')
        plt.savefig("SizeDEVIATIONofROLES_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"logcolor.png")
        #plt.show()
        plt.figure(543291)
        plt.pcolor(Ax,Ay,dROL,norm=LogNorm(vmin=minimor,vmax=maximod), cmap=('hot_r'))
        cl = plt.colorbar()
        cl.ax.set_title("dev_S")
        plt.axis([0, 1, -2.5, 10])
        plt.axvline(0.3,5./12.5,1,color='green')
        plt.axvline(0.75,5./12.5,1,color='green')
        plt.axvline(0.05,0,5./12.5,color='green')
        plt.axvline(0.625,0,5./12.5,color='green')
        plt.axvline(0.8,0,5./12.5,color='green')
        plt.axhline(y=2.5, color='green')
        plt.savefig("SizeDEVIATIONofROLES_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"logcolorMIN.png")
        
        plt.figure(53412+232*epsilon.index(e))
        plt.pcolor(Ax,Ay,dROL,vmin=0,vmax=maximod, cmap=('hot_r'))
        cl = plt.colorbar()
        cl.ax.set_title("dev_S")
        plt.axis([0, 1, -2.5, 10])
        plt.axvline(0.3,5./12.5,1,color='green')
        plt.axvline(0.75,5./12.5,1,color='green')
        plt.axvline(0.05,0,5./12.5,color='green')
        plt.axvline(0.625,0,5./12.5,color='green')
        plt.axvline(0.8,0,5./12.5,color='green')
        plt.axhline(y=2.5, color='green')
        plt.savefig("SizeDEVIATIONofROLES_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+".png")
        #plt.show()

        
        plt.figure(539412)
        plt.pcolor(Ax,Ay,dROL,vmin=minimor,vmax=maximod, cmap=('hot_r'))
        cl = plt.colorbar()
        cl.ax.set_title("dev_S")
        plt.axis([0, 1, -2.5, 10])
        plt.axvline(0.3,5./12.5,1,color='green')
        plt.axvline(0.75,5./12.5,1,color='green')
        plt.axvline(0.05,0,5./12.5,color='green')
        plt.axvline(0.625,0,5./12.5,color='green')
        plt.axvline(0.8,0,5./12.5,color='green')
        plt.axhline(y=2.5, color='green')
        plt.savefig("SizeDEVIATIONofROLES_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"MIN.png")
        """
        ##GRAFICO 2 SEPARADOS Y JUNTOS Y UNA PRUEBA CON UN SOLO Z, CUMULATIVE SIZE##
        ##GRAFICO 2 CascadeSizeForP CSP##
        #Sumatorio por todo rango de z en zona No-Hub y zona Hub (por separado, dos graficos), hacer media
        
        #eje x: p_G
        #eje y: <S(sum(z)>
        
        #print collections.Counter(p_G)
        
        #Ordenacion optima, vector dentro de vector indica los mismos p
        #En verdad z_h y z_nh no lo necesitas, se suman todos
        p_h, z_h, s_h = [], [], []
        p_nh, z_nh, s_nh = [], [], []
        cuanto = 0
        while len(p_G) > 0:
            para_p_h, para_z_h, para_s_h = [], [], []
            para_p_nh, para_z_nh, para_s_nh = [], [], []
            elimina = []
            cuanto = cuanto + 1
            for i in range(len(p_G)):
                if p_G[i] == p_G[0]:
                    if z_G[i] >= 2.5:
                        para_p_h.append(p_G[i])
                        para_z_h.append(z_G[i])
                        para_s_h.append(sizemid[i])
                        elimina.append(p_G[i])
                    if z_G[i] < 2.5:
                        para_p_nh.append(p_G[i])
                        para_z_nh.append(z_G[i])
                        para_s_nh.append(sizemid[i])
                        elimina.append(p_G[i])
            
            if len(para_p_h) > 0:
                p_h.append(para_p_h)
                z_h.append(para_z_h)
                s_h.append(para_s_h)
            if len(para_p_nh) > 0:
                p_nh.append(para_p_nh)
                z_nh.append(para_z_nh)
                s_nh.append(para_s_nh)
            
            for p in elimina:
                j = p_G.index(p)
                del p_G[j], z_G[j], sizemid[j]
        
        
        #MEDIA, DESVIACION ESTANDAR
        pmedia_h, smedia_h, desviacion_h = [], [], []
        pmedia_nh, smedia_nh, desviacion_nh = [], [], []
        
        
        for n in range(len(p_h)):
            pmedia_h.append(p_h[n][0])
            smedia_h.append(float(sum(s_h[n]))/float(len(s_h[n])))
            desvh = 0.
            for s_i in s_h[n]:
                desvh = desvh + (s_i-smedia_h[n])**2
            desviacion_h.append(((1./float(N-1))*desvh)**0.5)
        for n in range(len(p_nh)):
            pmedia_nh.append(p_nh[n][0])
            smedia_nh.append(float(sum(s_nh[n]))/float(len(s_nh[n])))
            desvnh = 0.
            for s_i in s_nh[n]:
                desvnh = desvnh + (s_i-smedia_nh[n])**2
            desviacion_nh.append(((1./float(N-1))*desvnh)**0.5)
            
        #print len(pmedia_h),len(smedia_h),len(desviacion_h)
        #print len(pmedia_nh),len(smedia_nh),len(desviacion_nh)
               
        
        copia_P = pmedia_h[:]
        copia_S = smedia_h[:]
        copia_D = desviacion_h[:]
        
        #ordenado        
        p_ord_h = []
        s_ord_h = []
        d_ord_h = []
        while len(pmedia_h) > 0:
            izmierda = pmedia_h.index(min(pmedia_h))
            p_ord_h.append(min(pmedia_h))
            s_ord_h.append(smedia_h[izmierda])
            d_ord_h.append(desviacion_h[izmierda])
            del pmedia_h[izmierda], smedia_h[izmierda], desviacion_h[izmierda]
        p_ord_nh = []
        s_ord_nh = []
        d_ord_nh = []
        while len(pmedia_nh) > 0:
            izmierda = pmedia_nh.index(min(pmedia_nh))
            p_ord_nh.append(min(pmedia_nh))
            s_ord_nh.append(smedia_nh[izmierda])
            d_ord_nh.append(desviacion_nh[izmierda])
            del pmedia_nh[izmierda], smedia_nh[izmierda], desviacion_nh[izmierda]
            
            
        #cumulativos
        cum_h = len(s_ord_h)*[0]
        cum_h[0] = s_ord_h[0]
        for a in range(len(s_ord_h)):
            if a >= 1:
                cum_h[a] = cum_h[a-1] + s_ord_h[a]
        cum_nh = len(s_ord_nh)*[0]
        cum_nh[0] = s_ord_nh[0]
        for a in range(len(s_ord_nh)):
            if a >= 1:
                cum_nh[a] = cum_nh[a-1] + s_ord_nh[a]
        
        ##COPIO A TEXTO PARA CARACTERIZAR LOS EXPONENTES
        documento = 'Hubs'+str(z)+'Epsilon='+str(e)+'.txt'
        with open(documento,"w") as res:
            #res.write("p       <S>")
            #res.write("\n")
            for i in range(len(p_ord_h)):
                res.write(str(p_ord_h[i])+"     "+str(cum_h[i])+"     "+str(d_ord_h[i]))
                if i != len(p_ord_h)-1:
                    res.write("\n")
                
        documento = 'NonHubs'+str(z)+'Epsilon='+str(e)+'.txt'
        with open(documento,"w") as res:
            #res.write("p       <S>")
            #res.write("\n")
            for i in range(len(p_ord_nh)):
                res.write(str(p_ord_nh[i])+"     "+str(cum_nh[i])+"     "+str(d_ord_nh[i]))
                if i != len(p_ord_nh)-1:
                    res.write("\n")

        
        
        ## ## ## ## ## ## ## ## ## ## ## ##
        """
        plt.figure(2*z+1)
        plt.errorbar(p_ord_h,cum_h,yerr=d_ord_h,fmt='.',label="epsilon = " +str(e))
        plt.legend(loc = 2)
        plt.title("<S(z)> vs. P of Hubs")
        
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size")
        plt.xlim(-0.01,1)
        #plt.ylim(-0.01*max(cum_h),max(cum_h)+0.05*max(cum_h))
        
        #plt.text(0.1195, 0.95*max(cum_h), 'R5', alpha = 0.4, color='brown', size = 'xx-large')
        plt.axvline(0.3,linestyle='--')
        #plt.text(0.495, 0.95*max(cum_h), 'R6', alpha = 0.4, color='brown', size = 'xx-large')
        plt.axvline(0.75,linestyle='--')
        #plt.text(0.85, min(cum_h)+0.05*max(cum_h), 'R7', alpha = 0.4, color='brown', size = 'xx-large')
        
        plt.savefig("csp_HUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+".png")
        #plt.show()
        

        plt.figure(5*z+2)
        plt.errorbar(p_ord_h,cum_h,yerr=d_ord_h,fmt='.', label="epsilon = " +str(e))
        plt.legend(loc = 2)
        plt.title("<S(z)> vs. P of Hubs")
        
        plt.yscale('log')
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size")
        plt.xlim(-0.01,1)
        #plt.ylim(-0.01*max(cum_h),max(cum_h)+0.05*max(cum_h))
        
        #plt.text(0.1195, 0.95*max(cum_h), 'R5', alpha = 0.4, color='brown', size = 'xx-large')
        plt.axvline(0.3,linestyle='--')
        #plt.text(0.495, 0.95*max(cum_h), 'R6', alpha = 0.4, color='brown', size = 'xx-large')
        plt.axvline(0.75,linestyle='--')
        #plt.text(0.85, min(cum_h)+0.05*max(cum_h), 'R7', alpha = 0.4, color='brown', size = 'xx-large')
        
        plt.savefig("csp_HUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+"log.png")
        #plt.show()

        ## ## ## ## ## ## ## ## ## ## ## ##
        
        plt.figure(10*z+4)
        plt.errorbar(p_ord_nh,cum_nh,yerr=d_ord_nh,fmt='.',label="epsilon = " +str(e))
        plt.legend(loc = 2)
        plt.title("<S(z)> vs. P of Non-Hubs")
        
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size") 
        plt.xlim(-0.01,1)
        #plt.ylim(-0.01*max(cum_nh),max(cum_nh)+0.05*max(cum_nh))
        
        #plt.text(-0.005, 0.95*max(cum_nh), 'R1', alpha = 0.4, color='brown', size = 'large')
        plt.axvline(0.05,linestyle='--')
        #plt.text(0.31, 0.95*max(cum_nh), 'R2', alpha = 0.4, color='brown', size = 'xx-large')
        plt.axvline(0.625,linestyle='--')
        #plt.text(0.68, 0.95*max(cum_nh), 'R3', alpha = 0.4, color='brown', size = 'xx-large')
        plt.axvline(0.8,linestyle='--')
        #plt.text(0.87, min(cum_h)+0.05*max(cum_h), 'R4', alpha = 0.4, color='brown', size = 'xx-large')
        
        plt.savefig("csp_nonHUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+".png")
        #plt.show()
        

        plt.figure(15*z+5)
        plt.errorbar(p_ord_nh,cum_nh,yerr=d_ord_nh,fmt='.',label="epsilon = " +str(e))
        plt.legend(loc = 2)
        plt.title("<S(z)> vs. P of Non-Hubs")
        
        plt.yscale('log')
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size") 
        plt.xlim(-0.01,1)
        #plt.ylim(-0.01*max(cum_nh),max(cum_nh)+0.05*max(cum_nh))
        
        #plt.text(-0.005, 0.95*max(cum_nh), 'R1', alpha = 0.4, color='brown', size = 'large')
        plt.axvline(0.05,linestyle='--')
        #plt.text(0.31, 0.95*max(cum_nh), 'R2', alpha = 0.4, color='brown', size = 'xx-large')
        plt.axvline(0.625,linestyle='--')
        #plt.text(0.68, 0.95*max(cum_nh), 'R3', alpha = 0.4, color='brown', size = 'xx-large')
        plt.axvline(0.8,linestyle='--')
        #plt.text(0.87, min(cum_h)+0.05*max(cum_h), 'R4', alpha = 0.4, color='brown', size = 'xx-large')
        
        plt.savefig("csp_nonHUBS_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+"log.png")
        #plt.show()

        
        ## ## ## ## ## ## ## ## ## ## ## ##
        plt.figure(20*z+7+epsilon.index(e)+9089252215152)
        plt.errorbar(p_ord_nh,cum_nh,yerr=d_ord_nh, fmt='.', label="z < 2.5")
        plt.errorbar(p_ord_h,cum_h,yerr=d_ord_h,fmt='.', label="z > 2.5")
        plt.title("<S(z)> vs. P")
        
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size") 
        plt.xlim(0,1)
        
        plt.legend(loc = 2)
        plt.savefig("csp_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+".png")
        #plt.show()
        
        plt.figure(2*z+20*epsilon.index(e)+21+521512513215)
        plt.errorbar(p_ord_nh,cum_nh,yerr=d_ord_nh, fmt='.', label="z < 2.5")
        plt.errorbar(p_ord_h,cum_h,yerr=d_ord_h,fmt='.', label="z > 2.5")
        plt.title("<S(z)> vs. P")
        
        plt.yscale('log')
        plt.xlabel("Participation coeficient")
        plt.ylabel("Cumulative Average Cascade Size") 
        plt.xlim(0,1)
        
        plt.legend(loc = 2)
        plt.savefig("csp_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"e"+str(ciclo)+"c"+"pondera_num_"+str(z+1)+"log.png")
        """