import json

with open("project.geom", "r") as f:
    datos = json.load(f)


class Lvl:
    def __init__(self, lvl_id, H, cols, beams):
        self.lvl_id = lvl_id
        self.H = H
        self.cols = cols
        self.beams = beams


class Beam:
    def __init__(self, lvl_id, beam_id, node_i, node_f):
        self.lvl_id = lvl_id
        self.beam_id = beam_id
        self.node_i = node_i
        self.node_f = node_f


class Column:
    def __init__(self, lvl_id, column_id, node_b, node_t):
        self.lvl_id = lvl_id
        self.column_id = column_id
        self.node_b = node_b
        self.node_t = node_t


class Node:
    def __init__(self, lvl_id, x_dim, y_dim, z_dim):
        self.lvl_id = lvl_id
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim

def Crear_listas():
    pisos=[]
    columnas = []
    vigas = []
    obnodos =[]
    return(pisos,columnas,vigas,obnodos)

Crear_listas()


def Generar_pisos(datos,Lvl,pisos):
    # este método crea los objetos piso y los agrupa en una lista
    h=0
    for lvl_id in reversed(datos["pisos"]):
        h = datos["pisos"][lvl_id]+h
        col = list(datos["col_piso"][lvl_id].keys())
        beam = list(datos["vig_piso"][lvl_id].keys())
        piso = Lvl(lvl_id, h, col, beam)
        pisos.append(piso)
    return(pisos)
Generar_pisos(datos, Lvl,pisos)




def Extraer_objetos(pisos,Beam,Node,Column,Lvl,vigas,columnas,obnodos):

    
    Extraer_vigas(datos, Beam, pisos, vigas)

    Extraer_columnas(datos,Column,pisos,columnas)

    Extraer_nodos(pisos,datos,Node,obnodos)

    return(columnas,vigas,obnodos)

Extraer_objetos(pisos,Beam,Node,Column,Lvl)


def Extraer_vigas(datos, Beam, pisos,vigas):
    # este método crea los objetos viga en cada piso y los agrupa en una lista
    for n in pisos:
        for b in n.beams:  # b es una viga perteneciente al piso n
            nodoi = datos["vigas"][b][0]
            nodod = datos["vigas"][b][1]
            viga = Beam(n.lvl_id, b, nodoi, nodod)
            vigas.append(viga)
    return(vigas)
    
def Extraer_columnas(datos,Column,pisos,columnas):
    # este método crea los objetos columna para cada piso y los agrupa en una lista

    for n in pisos:
        for b in n.cols:
            nodob = datos["columnas"][b][0]
            nodot = datos["columnas"][b][1]
            columna = Column(n.lvl_id, b, nodob, nodot)
            columnas.append(columna)
    # parámetros de un objeto columna específico
    # print(columnas[1].__dict__)
    return(columnas)

def Extraer_nodos(pisos, datos, Node, obnodos):
    # este método crea los objetos nodo para cada piso y los agrupa en una lista
    for n in pisos:
        z = n.H
        nodos = []
        for b in n.beams:
            nodos.append(datos["vigas"][b][0])
            nodos.append(datos["vigas"][b][1])
        res = []
        [res.append(x) for x in nodos if x not in res]
        print(res)
        for nodox in res:
            x = datos["nodos"][nodox][0]
            y = datos["nodos"][nodox][1]
            nodo = Node(n.lvl_id, nodox, x, y, z)
            # visualiza la creación de objetos nodo
            # print(nodo)
            obnodos.append(nodo)
    return(obnodos)


#print()
## número de nodos creados, número de nodos en el archivo .geom
print(len(obnodos),len(datos["nodos"]),len(pisos),len(pisos[1].beams),len(pisos[2].beams))
## parámetros de un nodo específico
#print(obnodos[-1].__dict__)



    