# mt.py

from tape import Tape

def simular_mt(configuracion, cadena):
    """
    Simula la Máquina de Turing con la cadena de entrada proporcionada.
    """
    # Extraer componentes de la configuración
    estados = configuracion['estados']
    estado_inicial = configuracion['estado_inicial']
    estado_final = configuracion['estado_final']
    transiciones = configuracion['transiciones']
    blank_symbol = configuracion['blank_symbol']

    # Inicializar la cinta usando la clase Tape
    tape = Tape(cadena, blank_symbol=blank_symbol)
    estado_actual = estado_inicial
    ids = []  # Lista para almacenar las descripciones instantáneas

    paso = 0  # Contador de pasos
    max_pasos = 1000  # Límite para evitar bucles infinitos

    while paso < max_pasos:
        simbolo_leido = tape.read()

        # Registrar la descripción instantánea actual
        id_actual = {
            'paso': paso,
            'estado': estado_actual,
            'cinta': tape.get_tape_contents(),
            'cabezal': tape.get_head_position()
        }
        ids.append(id_actual)

        # Verificar si se ha alcanzado el estado de aceptación
        if estado_actual == estado_final:
            aceptada = True
            return ids, aceptada

        # Obtener la transición correspondiente
        clave = (estado_actual, simbolo_leido)
        if clave in transiciones:
            nuevo_estado, simbolo_escrito, movimiento = transiciones[clave]

            # Actualizar la cinta y el estado
            tape.write(simbolo_escrito)
            estado_actual = nuevo_estado

            # Mover el cabezal
            tape.move(movimiento)
        else:
            # No hay transición definida para este par (estado, símbolo)
            aceptada = False
            return ids, aceptada

        paso += 1

    # Si se supera el número máximo de pasos, asumimos que hay un bucle infinito
    aceptada = False
    return ids, aceptada
