import Canales
import math
import simpy

class Nodo:
    """Representa un nodo basico.

    Implementada por:
    Barrientos Alvarez Jorge Miguel Aaron
    Martinez Pardo Esau

    Atributos:
    id_nodo -- identificador del nodo
    vecinos -- lista con los ids de nuestros vecinos
    canales -- tupla de la forma (canal_entrada, canal_salida)
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor basico de un Nodo."""
        self.id_nodo=id_nodo
        self.vecinos=vecinos
        self.canales=canales

    def __str__(self):
        """Regresa la representacion en cadena del nodo."""
        ret="Nodo_id: "+self.nodo_id+", vecinos: "+self.vecinos
        return ret
    
    def get_id(self) -> int:
        """Regresa el identificador del nodo."""
        return self.id_nodo
    
    def get_vecinos(self) -> list:
        """Regresa la lista de vecinos del nodo."""
        return self.id_vecinos

    def get_canal_entrada(self) -> simpy.Store:
        """Regresa el canal de entrada del nodo."""
        return self.canales[0]

    def get_canal_salida(self) -> Canales.Canal:
        """Regresa el canal de salida del nodo."""
        return self.canales[1]

class NodoBFS(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 1.

    Atributos adicionales:
    padre -- id del nodo que sera su padre en el arbol
    nivel -- entero que representa la distancia del nodo a la raiz
    hijos -- lista de ids de los nodos hijos del nodo
    msjs_esperados -- numero de mensajes que espera el nodo
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo 'bfs'."""
        Nodo.__init__(self, id_nodo, vecinos, canales)
        self.padre=-1
        self.nivel=-1
        self.hijos=[]
        self.msjs_esperados=-1

    def bfs(self, env: simpy.Environment):
        """Algoritmo de BFS."""
        #tomaremos al nodo con id=0 como el proceso distinguido
        if(self.id_nodo==0):
            self.canales[1].envia(("GO", -1, self.id_nodo), [self.id_nodo])

        while True:
            msg=yield self.canales[0].get()

            if msg[0]=="GO":
                if self.padre==-1:
                    self.padre=msg[2]
                    self.nivel=msg[1]+1
                    self.msjs_esperados=len(self.vecinos)-1
                    
                    if self.msjs_esperados==0:
                        self.canales[1].envia(("BACK", "yes", msg[1]+1, self.id_nodo), [self.padre])

                    else:
                        for vecino in self.vecinos:
                            if vecino==msg[2]:
                                continue
                            self.canales[1].envia(("GO", msg[1]+1, self.id_nodo), [vecino])

                elif self.nivel>msg[1]+1:
                    self.padre=msg[2]
                    self.nivel=msg[1]+1
                    self.msjs_esperados=len(self.vecinos)-1

                    if(self.msjs_esperados==0):
                        self.canales[1].envia(("BACK", "yes", msg[1], self.id_nodo), [self.padre])

                    else:
                        for vecino in self.vecinos:
                            if vecino==msg[2]:
                                continue
                            self.canales[1].envia(("GO", msg[1]+1, self.id_nodo), [vecino])
                
                else:
                    self.canales[1].envia(("BACK", "no", msg[1]+1, self.id_nodo), [msg[2]])
            
            
            elif msg[0]=="BACK": 
                d=msg[2]

                if d==self.nivel+1:
                    if msg[1]=="yes":
                        if msg[3] not in self.hijos:
                            self.hijos.append(msg[3])
                    
                        self.msjs_esperados-=1

                        if(self.msjs_esperados==0):
                            if(self.padre!=self.id_nodo):
                                    self.canales[1].envia(("BACK", "yes", self.nivel, self.id_nodo), [self.padre])


