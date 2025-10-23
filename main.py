from tqdm import tqdm
import time
import clasesAuxiliares as ca

# Pregunta por el tamaño del tablero; 
# Crea y muestra el tablero del jugador:
######################################################################################

while True:
    print()
    tamano_tablero = input("Introduce el tamaño del tablero: ")
    try:
        tablero_jugador = ca.Tablero(tamano_tablero) # Eleva una excepción si no se pasa un tamaño válido
        break
    except Exception as e:
        print(e, " - Inténtalo de nuevo")

tamano_tablero_int = tablero_jugador.tamano_tablero
tablero_jugador.set_barcos_aleatoriamente()

print()
print("_______________________ TABLERO JUGADOR _______________________")
print()
print(tablero_jugador.get_representacion_tablero_defendido())


## Crea y muestra el tablero del oponente:
######################################################################################

tablero_maquina = ca.Tablero(tamano_tablero) # Eleva una excepción si no se pasa un tamaño válido
tablero_maquina.set_barcos_aleatoriamente()

print()
print("_______________________ TABLERO OPONENTE _______________________")
print()
print(tablero_maquina.get_representacion_tablero_defendido())

## Comienza los turnos:
######################################################################################
turno_count = 0

while True:
    turno_count += 1

    print()
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print(f"TURNO '{turno_count}'")
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print()


    partida_terminada = False

    ## Turno del jugador:
    while True:
        disparo_jugador = ca.Utils.get_disparo_jugador(tamano_tablero_int)
        resultado = tablero_maquina.set_disparo(disparo_jugador)

        print()
        print(f"{resultado} - Tu tablero de ataque queda así:")
        print()
        print(tablero_maquina.get_representacion_tablero_para_el_oponente())
        print()
        print('________________________________________________________________________________________________')
        print()

        if (not tablero_maquina.get_quedan_barcos_por_hundir()):
            print("HAS GANADO!!! No quedan más barcos por hundir")
            print()
            partida_terminada = True
            break

        if resultado == ca.ResultadoDisparo.AGUA.value:
            break # el resultado Agua no da derecho a continuar el turno del jugador, salimos del bucle

    if partida_terminada:
        break
    
    ## Turno de la máquina:
    while True:
        # Simula que el oponente está pensando con una barra de progreso
        for i in tqdm(range(200), desc="Tu oponente está pensando..."):
            time.sleep(0.01)

        disparo_maquina = ca.Utils.get_disparo_maquina(tablero_jugador)
        resultado = tablero_jugador.set_disparo(disparo_maquina)

        print()
        print(f"Tu oponente ha disparado a la coordenada {disparo_maquina.letra_columna} {disparo_maquina.numero_fila}")
        print()
        print(f"El resultado ha sido {resultado} - Tu oponente puede ver esta parte de tu tablero:")
        print()
        print(tablero_jugador.get_representacion_tablero_para_el_oponente())
        print()
        print('________________________________________________________________________________________________')
        print()

        if (not tablero_jugador.get_quedan_barcos_por_hundir()):
            print("HAS PERDIDO!!! No te queda ningún barco a flote")
            partida_terminada = True
            break

        if resultado == ca.ResultadoDisparo.AGUA.value:
            break # el resultado Agua no da derecho a continuar el turno del jugador, salimos del bucle

        time.sleep(5) ## Esperar para dar tiempo a ver la pantalla

    if partida_terminada:
        break