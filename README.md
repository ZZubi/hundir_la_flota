# Hundir la Flota en Python 🚢

Este proyecto implementa el clásico juego de mesa **Hundir la Flota** utilizando programación orientada a objetos (POO) en Python, separando la lógica del tablero, los barcos y la interacción.

## Clases Clave Involucradas

El código utiliza varias clases para modelar las entidades del juego, más allá de las clases de utilidad (`Constants`, `Orientacion`, `Casilla`, `ResultadoDisparo`, `Utils`). Las tres clases principales que estructuran el juego son:

### 1. `Barco` ⚓

* **Propósito:** Es la clase de **modelo de datos** para una embarcación individual.
* **Responsabilidad:** Almacena la **eslora** (longitud) del barco y una lista de las **posiciones exactas** que ocupa en el tablero. Mantiene un registro de qué partes del barco han sido **tocadas** (`posiciones_tocadas_en_tablero`) y provee el método para determinar si el barco ha sido **hundido** (`get_esta_hundido`).

### 2. `Disparo` 💥

* **Propósito:** Es la clase que **modela una acción** del jugador o de la máquina.
* **Responsabilidad:** Almacenar las coordenadas de un disparo (letra de columna y número de fila), asegurando que las coordenadas sean **válidas** para el tamaño del tablero actual. Permite obtener la tupla de índices (`(fila_index, columna_index)`) que el `Tablero` necesita para procesar el impacto.

### 3. `Tablero` 🗺️

* **Propósito:** Es la clase central que contiene la **lógica del juego** y el **estado general** de la partida para un jugador.
* **Responsabilidad:**
    * **Almacenar:** Contiene la matriz **NumPy** (`self.tablero`) que representa la cuadrícula y la lista de objetos `Barco` y `Disparo` que se han realizado.
    * **Gestión de Barcos:** Se encarga de la **colocación de barcos** aleatoriamente (`set_barcos_aleatoriamente`) y de verificar si quedan barcos por hundir (`get_quedan_barcos_por_hundir`).
    * **Procesar Disparos:** Contiene la lógica para **recibir un disparo** (`set_disparo`), determinar el resultado (`AGUA`, `TOCADO`, `HUNDIDO`) y actualizar el estado de los barcos afectados.
    * **Representación:** Genera la **vista del tablero** para el jugador que lo defiende (mostrando sus barcos) y la vista de ataque para el oponente (ocultando los barcos no tocados).

## Flujo Principal del Juego

1.  Se solicitan las dimensiones del tablero y se inicializan dos instancias de **`Tablero`** (uno para el jugador y otro para la máquina).
2.  Ambos tableros se pueblan con instancias de **`Barco`** de manera aleatoria.
3.  El juego entra en un bucle de turnos:
    * El jugador crea un **`Disparo`** con coordenadas válidas.
    * El disparo se aplica al **`Tablero`** de la máquina, que devuelve el resultado.
    * La máquina genera un **`Disparo`** aleatorio.
    * El disparo se aplica al **`Tablero`** del jugador, que devuelve el resultado.
4.  La partida continúa hasta que el método `get_quedan_barcos_por_hundir()` de uno de los tableros retorna `False`, declarando un ganador.