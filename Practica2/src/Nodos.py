import Canales
import math
import simpy

class Nodo:
    """Representa un nodo basico.

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
        returns self.id_nodo
    
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
        Nodo.__init__(id_nodo, vecinos, canales)
        self.padre=-1
        self.nivel=-1
        self.hijos=[]
        self.msjs_esperados=-1

    def bfs(self, env: simpy.Environment):
        """Algoritmo de BFS."""
