import random


class mapa:
    def __init__(self, filas, columnas, num_baches, num_caminos_empedrados, num_arboles):
        self.filas = filas
        self.columnas = columnas
        self.punto_inicio = None
        self.punto_fin = None
        self.num_baches = num_baches
        self.num_caminos_empedrados = num_caminos_empedrados
        self.num_arboles = num_arboles
        self.matriz = [[' ' for _ in range(self.columnas)]
                       for _ in range(self.filas)]

    # Función para colocar obstáculos en la matriz

    def colocar_obstaculos(self):
        matriz = self.matriz
        filas = self.filas
        columnas = self.columnas

        # Colocar baches (costo 2)
        for _ in range(self.num_baches):
            while True:
                fila = random.randint(0, filas - 1)
                columna = random.randint(0, columnas - 1)
                if matriz[fila][columna] == ' ':
                    matriz[fila][columna] = '#'
                    break

        # Colocar caminos empedrados (costo 1)
        for _ in range(self.num_caminos_empedrados):
            while True:
                fila = random.randint(0, filas - 1)
                columna = random.randint(0, columnas - 1)
                if matriz[fila][columna] == ' ':
                    matriz[fila][columna] = '+'
                    break

        # Colocar árboles (impenetrables)
        for _ in range(self.num_arboles):
            while True:
                try:
                    fila = int(
                        input("Ingrese una fila para el árbol (de 0 a {}): ".format(filas - 1)))
                    columna = int(
                        input("Ingrese una columna para el árbol (de 0 a {}): ".format(columnas - 1)))
                    if 0 <= fila < filas and 0 <= columna < columnas:
                        if matriz[fila][columna] == ' ':
                            matriz[fila][columna] = '&'
                            break
                        else:
                            print("Coordenadas ya ocupadas. Inténtalo de nuevo.")
                    else:
                        print("Coordenadas fuera de rango. Inténtalo de nuevo.")
                except ValueError:
                    print("Por favor, ingrese números válidos para la fila y columna.")

        return matriz

    # Función para colocar puntos de inicio y fin en bordes opuestos

    def colocar_puntos_inicio_fin(self):
        matriz = self.matriz
        filas = self.filas
        columnas = self.columnas

        while True:
            # Pedir al usuario las coordenadas del punto de partida
            print("\nIngrese las coordenadas del punto de partida:")
            try:
                fila_inicio = int(
                    input("Por favor, ingrese la fila del punto de partida: "))
                columna_inicio = int(
                    input("Por favor, ingrese la columna del punto de partida: "))
            except ValueError:
                print("Por favor, ingrese números válidos para la fila y columna.")
                continue

            if fila_inicio < 0 or fila_inicio >= filas or columna_inicio < 0 or columna_inicio >= columnas or matriz[fila_inicio][columna_inicio] != ' ':
                print("Coordenadas fuera de rango o ya ocupadas. Inténtelo de nuevo.")
                continue
            break
        while True:
            # Pedir al usuario las coordenadas del punto de llegada
            print("\nIngrese las coordenadas del punto de llegada:")
            try:
                fila_fin = int(
                    input("Por favor, ingrese la fila del punto de llegada: "))
                columna_fin = int(
                    input("Por favor, ingrese la columna del punto de llegada: "))
            except ValueError:
                print("Por favor, ingrese números válidos para la fila y columna.")
                continue

            if fila_fin < 0 or fila_fin >= filas or columna_fin < 0 or columna_fin >= columnas or matriz[fila_fin][columna_fin] != ' ':
                print("Coordenadas fuera de rango o ya ocupadas. Inténtelo de nuevo.")
                continue
            self.punto_inicio = (fila_inicio, columna_inicio)
            self.punto_fin = (fila_fin, columna_fin)
            matriz[fila_inicio][columna_inicio] = 'S'
            matriz[fila_fin][columna_fin] = 'E'
            break

        return matriz, self.punto_fin, self.punto_fin

 # funcion para sacar obstaculos
    def eliminarobstaculos(self):
        matriz = self.matriz
        self.fila_eliminar = int(
            input('Selecciona la fila del obstaculo que quieres eliminar: '))
        self.columna_eliminar = int(
            input('Selecciona la columna del obstaculo a eliminar: '))
        matriz[self.fila_eliminar][self.columna_eliminar] = ' '


class calculadoraderutas:
    def __init__(self, instancia_mapa):
        self.mapa = instancia_mapa
        self.filas = instancia_mapa.filas
        self.columnas = instancia_mapa.columnas
        self.punto_inicio = instancia_mapa.punto_inicio
        self.punto_fin = instancia_mapa.punto_fin
        self.matriz = instancia_mapa.matriz

    # funcion para calcular heuristica
    def heuristica(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # la poderosa A*
    def a_estrella(self):
        filas = self.filas
        columnas = self.columnas

        # Movimientos posibles (arriba, abajo, izquierda, derecha)
        movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Inicializar la lista abierta y la cerrada
        conjunto_abierto = [(0, self.punto_inicio)]
        puntaje_g = {self.punto_inicio: 0}
        puntaje_f = {self.punto_inicio: self.heuristica(
            self.punto_inicio, self.punto_fin)}
        viene_de = {}

        while conjunto_abierto:
            # Obtener el nodo con la menor puntuación f
            conjunto_abierto.sort()
            _, actual = conjunto_abierto.pop(0)

            if actual == self.punto_fin:
                # Reconstruir el camino
                camino = []
                while actual in viene_de:
                    camino.append(actual)
                    actual = viene_de[actual]
                camino.append(self.punto_inicio)
                camino.reverse()
                return camino

            for dx, dy in movimientos:
                vecino = (actual[0] + dx, actual[1] + dy)

                if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                    if self.matriz[vecino[0]][vecino[1]] != '&':  # No atravesar árboles
                        # Costo del vecino
                        if self.matriz[vecino[0]][vecino[1]] == 'E':
                            costo_vecino = 0  # Punto de llegada
                        elif self.matriz[vecino[0]][vecino[1]] == '+':
                            costo_vecino = 2  # Camino empedrado
                        elif self.matriz[vecino[0]][vecino[1]] == '#':
                            costo_vecino = 3  # Bache
                        else:
                            costo_vecino = 1  # Espacio vacío

                        puntaje_g_tentativo = puntaje_g[actual] + costo_vecino

                        if vecino not in puntaje_g or puntaje_g_tentativo < puntaje_g[vecino]:
                            viene_de[vecino] = actual
                            puntaje_g[vecino] = puntaje_g_tentativo
                            puntaje_f[vecino] = puntaje_g_tentativo + \
                                self.heuristica(vecino, self.punto_fin)
                            if vecino not in [n for _, n in conjunto_abierto]:
                                conjunto_abierto.append(
                                    (puntaje_f[vecino], vecino))

        return None  # No se encontró un camino

# Función para imprimir la matriz con bordes


def imprimir_matriz(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])

    # Imprimir la parte superior del borde
    print('╔' + '═' * (columnas * 2 - 1) + '╗')

    # Imprimir el contenido de la matriz
    for fila in matriz:
        print('║', end='')
        for valor in fila:
            print(f' {valor}', end='')
        print(' ║')

    # Imprimir la parte inferior del borde
    print('╚' + '═' * (columnas * 2 - 1) + '╝')


# Flujo del codigo

alto_mapita = mapa(15, 15, 25, 30, 5)
alto_mapita.colocar_obstaculos()
alto_mapita.colocar_puntos_inicio_fin()
imprimir_matriz(alto_mapita.matriz)
# Ya al A*
ruta_calculadora = calculadoraderutas(alto_mapita)
camino = ruta_calculadora.a_estrella()
if camino:
    print("\nCamino encontrado:")
    matriz_camino = [list(fila) for fila in alto_mapita.matriz]
    for paso in camino[1:-1]:
        matriz_camino[paso[0]][paso[1]] = '*'
    imprimir_matriz(matriz_camino)
else:
    print("\nNo se encontró un camino válido.")
