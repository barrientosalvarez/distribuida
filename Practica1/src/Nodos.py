import Canales
import simpy

class Nodo:
    """Representa un nodo basico.
    Hecho por:
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
        return "id= "+str(self.id_nodo)+", vecinos= "+str(self.vecinos)+", canales= "+str(self.canales)
    
    def get_id(self) -> int:
        """Regresa el identificador del nodo."""
        return self.id_nodo
    
    def get_vecinos(self) -> list:
        """Regresa la lista de vecinos del nodo."""
        return self.vecinos

    def get_canal_entrada(self) -> simpy.Store:
        """Regresa el canal de entrada del nodo."""
        return self.canales[0]

    def get_canal_salida(self) -> Canales.Canal:
        """Regresa el canal de salida del nodo."""
        return self.canales[1]

class NodoVecinos(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 1.

    Atributos adicionales:
    vecinos_de_vecinos -- lista con los ids de los vecinos de nuestros vecinos
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        Nodo.__init__(self, id_nodo, vecinos, canales)
        self.vecinos_de_vecinos=[]

    def conoce_vecinos(self, env: simpy.Environment):
        """Algoritmo para conocer a los vecinos de mis vecinos."""
        self.canales[1].envia(self.vecinos, self.vecinos)

        while True:
            msg=yield self.canales[0].get()
            for vecino in msg:
                if vecino not in self.vecinos_de_vecinos:
                    self.vecinos_de_vecinos.append(vecino)


class NodoArbolGenerador(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 2.

    Atributos adicionales:
    madre -- id del nodo madre dentro del arbol
    hijas -- lista de nodos hijas del nodo actual
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo arbol generador."""
        Nodo.__init__(self, id_nodo, vecinos, canales)

        self.madre=-1
        self.hijas=[]
        self.expected_msg=-1
        self.condition=True

    def genera_arbol(self, env: simpy.Environment):
        """Algoritmo para producir el arbol generador."""

        #Tomaremos al nodo distinguido como el nodo con id=0
        if self.id_nodo==0 and self.condition:
            self.condition=False
            self.madre=0
            self.expected_msg=len(self.vecinos)
            self.canales[1].envia(("GO", self.id_nodo), self.vecinos)

        #else:
            #self.madre=-1

        while True:
            msg = yield self.canales[0].get()
            if msg[0]=="GO":
                if self.madre==-1:
                    self.madre=msg[1]
                    self.expected_msg=len(self.vecinos)-1
                    if self.expected_msg==0:
                        self.canales[1].envia(("BACK", [self.id_nodo], self.id_nodo), [msg[1]])
                    else:
                        for vecino in self.vecinos:
                            if vecino==msg[1]:
                                continue
                            self.canales[1].envia(("GO", self.id_nodo), [vecino])
                else:
                    self.canales[1].envia(("BACK",[], self.id_nodo), [msg[1]])

            elif msg[0]=="BACK":
                self.expected_msg-=1
                if(not(not msg[1])):
                    if msg[2] not in self.hijas:
                        self.hijas.append(msg[2])

                if self.expected_msg==0:
                    if self.madre!=self.id_nodo:
                        self.canales[1].envia(("BACK", [self.id_nodo], self.id_nodo), [self.madre])



class NodoBroadcast(Nodo):
    """Nodo que implementa el algoritmo del ejercicio 3.

    Atributos adicionales:
    mensaje -- cadena con el mensaje que se distribuye
    """
    def __init__(self, id_nodo: int, vecinos: list, canales: tuple):
        """Constructor para el nodo broadcast."""
        Nodo.__init__(self, id_nodo, vecinos, canales)
        self.mensaje=""
        self.condition=True

    def broadcast(self, env: simpy.Store):
        """Algoritmo de broadcast."""
        if self.id_nodo==0 and self.condition:
            self.mensaje="Test message"
            data=self.mensaje
            self.canales[1].envia(("GO", data), self.vecinos)

        while True:
            msg=yield self.canales[0].get()
            if msg[0]=="GO":
                self.mensaje=msg[1]
                data=self.mensaje
                self.canales[1].envia(("GO", data), self.vecinos)
            













