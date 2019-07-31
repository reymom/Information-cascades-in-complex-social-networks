import numpy as np
import networkx as nx
import sys

N = 1000
w = 3.


grados = []
epsilon = []

vez = int(sys.argv[1])
inicio = vez*0.25
for ygrad in range(20):
    grados.append(2+ygrad)
    
#recorro epsilon de forma equiespaciada en el eje logaritmico
for xep in range(5):
    epsilon.append(10**(-0.05*xep-inicio))

#print "recorrere", len(grados), "grados"
#print "recorrere", len(epsilon), "epsilones"

ciclomedio = len(epsilon)*[None]

#print ciclomedio

for e in epsilon:
    ciclogrado = []
    for grado in grados:
        #veces que repetire una simulacion con un valor dado, para hacer una estadistica
        ponderaciones = 25
        resultados = []
        G = nx.gnm_random_graph(N,N*grado/2)
        vecinos = list(G.edges())
    
        #
        #modifico la lista de vecinos de forma que no tenga que recorrerla cada vez, simplemente ir al indice del vector igual al nodo cuyos vecinos quiero encontrar
        edges=N*[[]]
        for i in range(N):
            edges_i=[]
            for a in vecinos:
                if a[0] == i:
                    edges_i.append(a[1])
                if a[1] == i:
                    edges_i.append(a[0])
            edges[i] = edges_i
    #luego veremos si va mas rapido, si no vuelvo a lo anterior
    #
    
        #print "SIMULACION con el valor de epsilon", e , "y de grado", grado
        print "valor a recorrer: " 
        print "epsilon ", epsilon.index(e)+1, "/", len(epsilon)
        print "degrees ", grados.index(grado)+1, "/", len(grados)
    #hago n ponderaciones de cada simulacion
        for z in range(ponderaciones):
            
            ###EMPIEZA SIMULACION###
        
            #valores iniciales aleatorios"
            E_i = np.random.rand(N)
            theta_i = (np.exp(w*E_i)-1.)/(np.exp(w)-1.)
          

            ciclo = 0
        
            #lista de variables para cada nodo, el valor asignado al nodo es cero si este ha pasado por la treshold almenos una vez, otherwise es uno
            c = N*[1]
        
            #en cada i hay un solo paso de avanzar el mas avanzado y ver como afectan a los vecinos y vecinos de los vecinos hasta que no hay fires
            for i in range(1000000):
                #cuando todos se han activado una vez almenos, es decir cuando su controlador es cero, el ciclo cambia
                if sum(c) == 0:
                    ciclo = ciclo + 1
                    c = N*[1]
                    #print "empieza ciclo", ciclo, "en iteracion", i
                    if i == N:
                        #esto significa que cada vez que hay el primer paso de avanzar el mas avanzado, no hace fire ninguno de sus vecinos
                        #la probabilidad de que se sincronice posteriormente antes de 250 ciclos es nula, porque es una red aleatoria, y
                        #todos los grados son proximos al valor medio. Para scalefree networks esto no lo puedo poner por esto mismo
                        #print "ninguno sincronizado, no hace falta esperar"
                        ciclo = 200
                        break
                    #print "E_i =", E_i
                
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
                    if (float(encendidos)/float(N)) > 1.:
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
            
                cascadesize = float(encendidos)/float(N)
            
                if cascadesize > 0.25:
                    #print "cascade size above desired", cascadesize
                    #print "EN EL CICLO",ciclo
                    break
            
                if ciclo > 199:
                    #print "no sincroniza, lleva 200"
                    break
        
                theta_i = (np.exp(w*E_i)-1.)/(np.exp(w)-1.)
        
            resultados.append(ciclo)
            print "ponderacion num", z, "ciclos", ciclo
        ciclogrado.append(float(sum(resultados))/float(len(resultados)))
        print "sinc en el ciclo",ciclogrado[grados.index(grado)]
        
        
    ciclomedio[epsilon.index(e)] = ciclogrado
    
    
print ciclomedio
    

documento = 'resultados1000nodos15ponderaciones'+str(vez)+'.txt'
with open(documento,"w") as res:
    res.write("<k>       e       ciclo medio cascada")
    res.write("\n")
    for e in epsilon:
        for grado in grados:
            resultado = ciclomedio[epsilon.index(e)][grados.index(grado)]
            res.write(str(grado)+"     "+str(e) +"     "+str(resultado))
            res.write("\n")
