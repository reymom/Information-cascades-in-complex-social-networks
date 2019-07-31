#Cascade Size in function of the edges a nodes initiateing a firing has
#Cascade Size Distribution
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import collections

N = 1000
w = 3.
grado = 3
#e = 0.025
#epsilon = [0.025,0.01,0.003,0.0025,0.002,0.0015]
epsilon = [0.09, 0.07, 0.05, 0.04, 0.03, 0.025]

ponderaciones = 1

#maximo para el grafico
maximo = 0.
minimo = 500.

for z in range(ponderaciones):
    G = nx.barabasi_albert_graph(N,grado/2)
    maindegree = float(sum(dict(G.degree()).values()))/float(G.number_of_nodes())
    vecinos = list(G.edges())

    edges=N*[[]]
    grad = []
    for i in range(N):
        edges_i=[]
        for a in vecinos:
            if a[0] == i:
                edges_i.append(a[1])
            if a[1] == i:
                edges_i.append(a[0])
        edges[i] = edges_i
        grad.append(len(edges_i))
    
    numepsilon = 0
    for e in epsilon:
        #para orden graficos
        numepsilon = numepsilon + 1
        print "SIMULACION epsilon = ", e, " ", (epsilon.index(e)+1),"/",len(epsilon)
        
        #para csd
        cascada_ciclo = [1./float(N)]
        ciclos = [0]
        cs = []
        
        #para csfne
        sizes = (max(grad)+1)*[0]
        vez_media = (max(grad)+1)*[0]
    
            
        ###EMPIEZA SIMULACION###

        #valores iniciales aleatorios"
        E_i = np.random.rand(N)
        theta_i = (np.exp(w*E_i)-1.)/(np.exp(w)-1.)
          
        ciclo = 0
        
        #lista de variables para cada nodo, el valor asignado al nodo es cero si este ha pasado por la treshold almenos una vez, otherwise es uno
        c = N*[1]
        cascadamayor = []
        gradogatillo= []
        #en cada i hay un solo paso de avanzar el mas avanzado y ver como afectan a los vecinos y vecinos de los vecinos hasta que no hay fires
        for i in range(1000000):
            #cuando todos se han activado una vez almenos, es decir cuando su controlador es cero, el ciclo cambia
            if sum(c) == 0:
                ciclo = ciclo + 1
                c = N*[1]
                print "la mayor cascada del ciclo", ciclo-1, ", provocada por nodo de grado ", gradogatillo[cascadamayor.index(max(cascadamayor))], ", ha medido", max(cascadamayor)
                cascadamayor = []
                gradogatillo = []

                
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
                if (float(encendidos)/float(N)) >= 1.:
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
            gradogatillo.append(len(edges[imax]))
            
            #para csd
            cs.append(cascadesize)
            
            #para csfne
            sizes[len(edges[imax])] = sizes[len(edges[imax])] + cascadesize
            vez_media[len(edges[imax])] = vez_media[len(edges[imax])] + 1
            
            
            #cuantos ciclos corro
            if ciclo >= 750:
                break
    
        
        
            theta_i = (np.exp(w*E_i)-1.)/(np.exp(w)-1.)



        ##GRAFICO CumulativeCascadeSize CSD##
        frecuencias = collections.Counter(cs)
        siz=[]
        frec = []
        for tupla in range(len(frecuencias.items())):
            siz.append(frecuencias.items()[tupla][0])
            frec.append(frecuencias.items()[tupla][1])
            
        cascade_size = []
        probabilidad_acumulada = []
        norma = float(len(cs))
        acumula = 0.
        rango = len(frec)
        for a in range(rango):
            rightsize = max(siz)
            #print "sizes", size
            imax = siz.index(rightsize)
            #print "frecs", frec
            rightfrec = frec[imax]
            acumula = acumula + float(rightfrec)/norma
            probabilidad_acumulada.append(acumula)
            cascade_size.append(rightsize)
            del frec[imax]
            siz.remove(rightsize)
            
        
    
        ##GRAFICO CumulativeCascadeSizeForNodesEdges CSFNE##

        #para grafico como antes pero con acumulados
        num = []
        cum = (max(grad)+1)*[0]
        for n in range(len(sizes)):
            num.append(n)
            if n == 0:
                sizes[n] = 0.
            if n >= 1:
                if vez_media[n] != 0:
                    cum[n] = float(sizes[n])/float(vez_media[n]) + cum[n-1]
                if vez_media[n] == 0:
                    cum[n] = cum[n-1]
    

        for numero in num:
            if numero not in grad:
                indice = num.index(numero)
                del num[indice]
                del cum[indice]


        
        mini = min(cum)
        while mini == 0:
            indixe = cum.index(mini)
            del num[indixe]
            del cum[indixe]
            mini = min(cum)
        
        if max(cum) > maximo:
            maximo = max(cum)
        if min(cum) < minimo:
            minimo = min(cum)



        ##GRAFICO CumulativeCascadeSize CSD##
        
        plt.figure(2*z+2*ponderaciones+2*len(epsilon)+696969)
        plt.title("CascadeSizeDistribution")
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("S")
        plt.ylabel("P(S)")   
        plt.plot(cascade_size,probabilidad_acumulada,'.',label="epsilon = " +str(e))
        plt.legend(loc = 3)
        plt.savefig("CSD_0_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"ciclos_ponderacion"+str(z)+".png")
        
        plt.figure(2*z+2*ponderaciones+2*len(epsilon)+1+10*numepsilon)
        plt.title("CascadeSizeDistribution")
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("S")
        plt.ylabel("P(S)")   
        plt.plot(cascade_size,probabilidad_acumulada,'.',label="epsilon = " +str(e))
        plt.legend(loc = 3)
        plt.savefig("CSD_"+str(numepsilon)+"_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"ciclos_ponderacion"+str(z)+".png")
        
        
        
        ##GRAFICOS CumulativeCascadeSizeForNodesEdges CSFNE##
        
        plt.figure(z)
        plt.plot(num,cum,'.',label="epsilon = " +str(e))
        plt.ylim(minimo,maximo)
        plt.xlabel("Node's Degree")
        plt.ylabel("CumulativeCascade size")   
        plt.title("CumulativeCascadeSizeForNodesEdges")
        plt.legend(loc = 2)
        plt.savefig("CSFNE_0_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"ciclos_cumul_ponderacion"+str(z)+".png")
    
        plt.figure(z+numepsilon)
        plt.plot(num,cum,'.',label="epsilon = " +str(e))
        plt.ylim(min(cum),max(cum))
        plt.xlabel("Node's Degree")
        plt.ylabel("CumulativeCascade size")   
        plt.title("CumulativeCascadeSizeForNodesEdges")
        plt.legend(loc = 2)
        plt.savefig("CSFNE_"+str(numepsilon)+"_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(e)+"epsilon"+str(ciclo)+"ciclos_cumul_ponderacion"+str(z)+".png")
        
        plt.figure(z+ponderaciones+len(epsilon))
        plt.plot(num,cum,'.',label="epsilon = " +str(e))
        plt.xscale('log')
        plt.ylim(minimo,maximo)
        plt.xlabel("Node's Degree")
        plt.ylabel("CumulativeCascade size")   
        plt.title("CumulativeCascadeSizeForNodesEdges")
        plt.legend(loc = 2)
        plt.savefig("CSFNE_"+str(len(epsilon)+1)+"_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"ciclos_cumulog_ponderacion"+str(z)+".png")
        
        plt.figure(z+2*ponderaciones+2*len(epsilon))
        plt.plot(num,cum,'.',label="epsilon = " +str(e))
        plt.xscale('log')
        plt.yscale('log')
        plt.ylim(minimo,maximo)
        plt.xlabel("Node's Degree")
        plt.ylabel("CumulativeCascade size")   
        plt.title("CumulativeCascadeSizeForNodesEdges")
        plt.legend(loc = 2)
        plt.savefig("CSFNE_"+str(len(epsilon)+2)+"_"+str(N)+"N"+str(w)+"w"+str(grado)+"k"+str(ciclo)+"ciclos_cumuloglog_ponderacion"+str(z)+".png")