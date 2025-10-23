from enum import Enum
import random
import numpy as np


##############################################################################################
##############################################################################################

class Constants:
    COLUMNAS_PERMITIDAS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    TAMANO_MINIMO_TABLERO = 6
    TAMANO_MAXIMO_TABLERO = len(COLUMNAS_PERMITIDAS)
    ESLORA_DE_LOS_BARCOS_DE_UNA_PARTIDA = [4, 3, 3, 2, 2, 2]
    #ESLORA_DE_LOS_BARCOS_DE_UNA_PARTIDA = [2]


##############################################################################################
##############################################################################################

class Orientacion(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

##############################################################################################
##############################################################################################

class Casilla(Enum):
    AGUA = "O"
    TOCADO = "X"
    INCOGNITA = " "
    BARCO = "X"


##############################################################################################
##############################################################################################

class ResultadoDisparo(Enum):
    AGUA = "AGUA !!"
    TOCADO = "TOCADO !!"
    HUNDIDO = "HUNDIDO !!"

##############################################################################################
##############################################################################################

class Barco:

    def __init__(self, eslora: int, letra_columna_top_left: str, numero_fila_top_left: int, orientacion: Orientacion):
        # En caso de ser necesario, podemos hacer primero la verificación de que los valores son válidos; asumiremos que este constructor se llama con valores válidos

        self.eslora = eslora

        indice_top_left = [Utils.get_indice_fila(numero_fila_top_left), Utils.get_indice_columna(letra_columna_top_left)]
        tupla_indice_top_left = tuple(indice_top_left)

        self.posiciones_en_tablero = [tupla_indice_top_left]
        self.posiciones_tocadas_en_tablero = [False]

        for i in range(1, eslora):
            if orientacion == Orientacion.HORIZONTAL:
                nueva_tupla_indice = ((indice_top_left[0] + i, indice_top_left[1]))
                self.posiciones_en_tablero.append(nueva_tupla_indice)

            elif orientacion == Orientacion.VERTICAL:
                nueva_tupla_indice = ((indice_top_left[0], indice_top_left[1] + i))
                self.posiciones_en_tablero.append(nueva_tupla_indice)
                
            self.posiciones_tocadas_en_tablero.append(False) # En la creación ningún barco está tocado

    ##############################################################################################
    
    def set_posicion_tocada(self, tupla_posicion: tuple):
        barco_index = self.posiciones_en_tablero.index(tupla_posicion)
        self.posiciones_tocadas_en_tablero[barco_index] = True

    ##############################################################################################
    
    def get_esta_hundido(self):
        return np.all(self.posiciones_tocadas_en_tablero) ## Si todas las posiciones están tocadas, esá hundido
    
    ##############################################################################################
    
    def get_tuplas_de_posicion_tocadas(self):
        tuplas_de_posicion_tocadas = []

        for index,is_posicion_tocada in enumerate(self.posiciones_tocadas_en_tablero):
            if is_posicion_tocada:
                tupla_tocada = self.posiciones_en_tablero[index]
                tuplas_de_posicion_tocadas.append(tupla_tocada)

        return tuplas_de_posicion_tocadas


##############################################################################################
##############################################################################################

class Disparo:

    def __init__(self, tamano_tablero: int, letra_columna: str, numero_fila: str):
        # Ponemos todo en mayúsculas
        letra_columna = letra_columna.upper()
        posibles_columnas_para_tamano_tablero = [letra.upper() for letra in Constants.COLUMNAS_PERMITIDAS[0:tamano_tablero]]

        if not isinstance(tamano_tablero, int):
            raise Exception("tamano_tablero debe ser un valor entero")
        elif  Constants.TAMANO_MINIMO_TABLERO > tamano_tablero  or tamano_tablero > Constants.TAMANO_MAXIMO_TABLERO:
            raise Exception(f"El tamaño del tablero debe estar comprendido entre {Constants.TAMANO_MINIMO_TABLERO} y {len(Constants.TAMANO_MAXIMO_TABLERO)}")
        elif not isinstance(letra_columna, str) or len(letra_columna) != 1:
            raise Exception("La columna debe ser una letra, y sólo una")
        elif letra_columna.upper() not in posibles_columnas_para_tamano_tablero:
            raise Exception ("La letra de la columna debe estar comprendida entre las siguientes:", posibles_columnas_para_tamano_tablero)
        
        try:
            numero_fila_int = int(numero_fila)
        except:
            raise Exception("El numero de fila introducido debe ser numérico")
        
        if 1 > numero_fila_int  or numero_fila_int > tamano_tablero:
            raise Exception("El número de fila introducida no puede ser menor de 1 ni mayor que el tamaño del tablero")

        self.fila_index = Utils.get_indice_fila(numero_fila_int)
        self.columna_index = Utils.get_indice_columna(letra_columna)
        self.letra_columna = letra_columna
        self.numero_fila = numero_fila

    ##############################################################################################
    
    def get_tupla_posicion(self):
        return tuple([self.fila_index, self.columna_index])


##############################################################################################
##############################################################################################

class Tablero:
    tablero: np.array
    barcos: list[Barco]
    disparos_recibidos: list[Disparo]
    tamano_tablero: int

    def __init__(self, tamano_tablero: str):
        try:
            tamano_tablero = int(tamano_tablero)
        except:
            raise Exception("El tamaño del tablero debe ser numérico")
        
        # Check valid size
        if Constants.TAMANO_MINIMO_TABLERO > tamano_tablero  or tamano_tablero > Constants.TAMANO_MAXIMO_TABLERO:
            raise Exception(f"El tamaño del tablero debe estar comprendido entre {Constants.TAMANO_MINIMO_TABLERO} y {Constants.TAMANO_MAXIMO_TABLERO} (ambos incluidos)")
        
        self.tamano_tablero = tamano_tablero
        self.tablero = np.full((tamano_tablero,tamano_tablero), Casilla.INCOGNITA.value, dtype=object)
        self.barcos = []
        self.disparos_recibidos = []

    ##############################################################################################

    def get_tuplas_posicion_sin_disparo(self):
        all_position_tuples = list(np.ndindex(self.tamano_tablero, self.tamano_tablero))
        disparo_position_tuples = []

        for disparo in self.disparos_recibidos:
            disparo_position_tuples.append(disparo.get_tupla_posicion())

        tuplas_de_posicion_sin_disparo = set(all_position_tuples) - set(disparo_position_tuples)

        return list(tuplas_de_posicion_sin_disparo)

    ##############################################################################################

    def set_disparo(self, disparo: Disparo):
        self.disparos_recibidos.append(disparo)

        tupla_posicion = disparo.get_tupla_posicion()
        contenido_casilla = self.tablero[tupla_posicion]

        if isinstance(contenido_casilla, Barco):
            barco = contenido_casilla
            barco.set_posicion_tocada(tupla_posicion)

            if barco.get_esta_hundido():
                return ResultadoDisparo.HUNDIDO.value
            else:
                return ResultadoDisparo.TOCADO.value

        ## Si llegamos hasta aquí, no es un barco y por lo tanto es agua
        self.tablero[tupla_posicion] = Casilla.AGUA.value

        return ResultadoDisparo.AGUA.value

    ##############################################################################################

    def set_barcos_aleatoriamente(self):
        ## Nos aseguramos de añadir primero los barcos de mayor eslora; si los dejamos para el final puede que no nos entren
        eslora_de_barcos_a_crear = sorted(Constants.ESLORA_DE_LOS_BARCOS_DE_UNA_PARTIDA, reverse = True)

        for eslora in eslora_de_barcos_a_crear:
            while True: ## Repetir hasta encontrar un barco que entre en el tablero
                barco_aleatorio = Utils.get_barco_aleatorio(eslora, self.tamano_tablero)

                try:
                    self.add_barco(barco_aleatorio)
                    break ## Salir del bucle while para 
                except Exception as e:
                    print(e)

    ##############################################################################################

    def get_quedan_barcos_por_hundir(self) -> bool:
        for barco in self.barcos:
            if not barco.get_esta_hundido():
                return True
            
        return False ## Todos los barcos están hundidos
    
    ##############################################################################################

    def get_representacion_tablero_para_el_oponente(self) -> np.array:
        representacion_tablero = self.tablero.copy() # hacemos una copia para no modificar el original
        representacion_tablero.fill(Casilla.INCOGNITA.value) # Ocultamos todas las casillas

        ## antes de procesar los tocados, marcamos todos los disparos como agua
        for disparo in self.disparos_recibidos:
            tupla_posicion = disparo.get_tupla_posicion()
            representacion_tablero[tupla_posicion] = Casilla.AGUA.value 

        ## A continuación, representamos todos los tocados (sobreescribirá algunas que hayamos marcado previamente como AGUA)
        for barco in self.barcos:
            for tupla_posicion_tocada in barco.get_tuplas_de_posicion_tocadas():
                representacion_tablero[tupla_posicion_tocada] = Casilla.TOCADO.value 

        return self.get_representacion_con_coordenadas(representacion_tablero)

    ##############################################################################################

    def get_representacion_tablero_defendido(self) -> np.array:
        representacion_tablero = self.tablero.copy()

        is_barco = np.vectorize(lambda x: isinstance(x, Barco))
        mask = is_barco(representacion_tablero)
        representacion_tablero[mask] = Casilla.BARCO.value

        return self.get_representacion_con_coordenadas(representacion_tablero)
    
    ##############################################################################################
    
    def get_representacion_con_coordenadas(self, tablero: np.array):
        vector_letras_columnas = self.get_vector_letras_columnas()
        array_2d_numeros_fila = self.get_array_2d_numeros_filas()

        tablero_con_columnas = np.vstack([vector_letras_columnas, tablero])
        tablero_con_filas_y_columnas = np.hstack([array_2d_numeros_fila, tablero_con_columnas])

        return tablero_con_filas_y_columnas
    
    ##############################################################################################
    
    def get_vector_letras_columnas(self):
        return np.array(Constants.COLUMNAS_PERMITIDAS[0:self.tamano_tablero])
    
    ##############################################################################################
    
    def get_array_2d_numeros_filas(self):
        vector_numeros_fila = np.arange(0,self.tamano_tablero+1)
        vector_numeros_fila = vector_numeros_fila.astype(str) ## convierte el vector de int a vector de str
        if len(vector_numeros_fila) > 10:
            vector_numeros_fila = np.char.zfill(vector_numeros_fila, 2)  # Añade un 0 por la izquierda a las filas hasta el 9 para que todas las filas se muestren con 2 dígitos
            vector_numeros_fila[vector_numeros_fila == "00"] = "  " # Reemplaza el "00" por dos espacios (acabará siendo la casilla top_left)
        else:
            vector_numeros_fila[vector_numeros_fila == "0"] = " " # Reemplaza el "0" por un espacio (acabará siendo la casilla top_left)

        return vector_numeros_fila.reshape(-1,1) ## retorna los valores en un array bidimensional de 1 columna

    ##############################################################################################
    
    def add_barco(self, barco: Barco):
        tablero_temporal = self.tablero.copy()
        for fila_index,columna_index in barco.posiciones_en_tablero:
            try:
                contenido_casilla = tablero_temporal[fila_index][columna_index] ## elevará excepción si no existe en el tablero; puede ocurrir cuando se intenta meter un barco de eslora grande con un punto de origen muy debajo a la derecha

                if isinstance(contenido_casilla, Barco):
                    raise Exception(f"Ya existe un barco en la posición ({fila_index},{columna_index})")
                    
                tablero_temporal[fila_index][columna_index] = barco

            except Exception as e:
                raise Exception('Este barco no entra en el tablero') # pasará habitualmente cuando estemos añadiendo barcos aleatorios

        # si llegamos hasta aquí es porque hemos podido añadir el barco entero, así que asignamos tablero_temporal al tablero real
        self.tablero = tablero_temporal
        self.barcos.append(barco)

##############################################################################################
##############################################################################################

class Utils:

    def get_disparo_jugador(tamano_tablero: int):
        while True:
            print()
            columna_a_disparar = input("Introduce la letra de la columna a la que disparar (A, B, C, ...): ")
            fila_a_disparar = input("Introduce el número de la fila a la que disparar (1, 2, 3, ...): ")

            try:
                disparo = Disparo(tamano_tablero, columna_a_disparar, fila_a_disparar)
                return disparo
            except Exception as e:
                print(f"{e} - Por favor, inténtalo de nuevo")

    ##############################################################################################
    
    def get_disparo_maquina(tablero_jugador: Tablero):
        tuplas_posicion_sin_disparo = tablero_jugador.get_tuplas_posicion_sin_disparo()
        tupla_posicion_disponible_random =  random.choice(tuplas_posicion_sin_disparo)

        letra_columna = Utils.get_letra_coordenada(tupla_posicion_disponible_random[1])
        numero_fila = Utils.get_numero_coordenada(tupla_posicion_disponible_random[0])

        ## Asumimos que aquí no obtendremos una excepción ya que hemos elegido entre las coordenadas que el tablero nos indica están libres
        return Disparo(tablero_jugador.tamano_tablero, letra_columna, numero_fila)
    
    ##############################################################################################
    
    def get_indice_columna(letra_columna: str):
        return Constants.COLUMNAS_PERMITIDAS.index(letra_columna)
    
    ##############################################################################################
    
    def get_indice_fila(numero_fila: int):
        return numero_fila - 1
    
    ##############################################################################################
    
    def get_letra_coordenada(indice: int):
        return Constants.COLUMNAS_PERMITIDAS[indice]
    
    ##############################################################################################
    
    def get_numero_coordenada(indice: int):
        return indice + 1
    
    ##############################################################################################
    
    def get_barco_aleatorio(eslora: int, tamano_tablero: int):
        valores_de_columna_posibles = Constants.COLUMNAS_PERMITIDAS[0:tamano_tablero]
        valores_de_fila_posibles = list(range(1,tamano_tablero+1))

        return Barco(
            eslora,
            random.choice(valores_de_columna_posibles),
            random.choice(valores_de_fila_posibles),
            random.choice(list(Orientacion))
        )