# parser_yaml.py

import yaml

def cargar_configuracion(archivo_yaml):
    """
    Carga la configuración desde un archivo YAML.
    """
    try:
        with open(archivo_yaml, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo '{archivo_yaml}' no fue encontrado.")
    except yaml.YAMLError as exc:
        raise ValueError(f"Error al parsear el archivo YAML: {exc}")

def validar_configuracion(config):
    """
    Valida que la configuración cargada contiene todas las claves necesarias.
    """
    required_keys = ['q_states', 'alphabet', 'tape_alphabet', 'delta', 'accepted_strings', 'rejected_strings']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Clave requerida '{key}' no encontrada en la configuración.")

    # Validar 'q_states'
    q_states = config['q_states']
    if 'q_list' not in q_states or 'initial' not in q_states or 'final' not in q_states:
        raise ValueError("La configuración de 'q_states' debe contener 'q_list', 'initial' y 'final'.")

    # Validar 'alphabet' y 'tape_alphabet'
    if not isinstance(config['alphabet'], list):
        raise ValueError("El 'alphabet' debe ser una lista.")
    if not isinstance(config['tape_alphabet'], list):
        raise ValueError("El 'tape_alphabet' debe ser una lista.")

    # Validar 'delta'
    if not isinstance(config['delta'], list):
        raise ValueError("La 'delta' debe ser una lista de transiciones.")

    # Validar 'accepted_strings' y 'rejected_strings'
    if not isinstance(config['accepted_strings'], list):
        raise ValueError("Las 'accepted_strings' deben ser una lista de cadenas.")
    if not isinstance(config['rejected_strings'], list):
        raise ValueError("Las 'rejected_strings' deben ser una lista de cadenas.")

    # Validar que los estados y símbolos estén correctamente definidos en las transiciones
    estados = q_states['q_list']
    alfabeto_cinta = config['tape_alphabet']
    for transicion in config['delta']:
        params = transicion.get('params', {})
        output = transicion.get('output', {})

        # Validar estados
        initial_state = params.get('initial_state')
        final_state = output.get('final_state')
        if initial_state not in estados:
            raise ValueError(f"El estado inicial '{initial_state}' en una transición no está definido en 'q_list'.")
        if final_state not in estados:
            raise ValueError(f"El estado final '{final_state}' en una transición no está definido en 'q_list'.")

        # Validar símbolos de la cinta
        tape_input = params.get('tape_input')
        tape_output = output.get('tape_output')
        if tape_input not in alfabeto_cinta:
            raise ValueError(f"El símbolo de entrada '{tape_input}' en una transición no está en 'tape_alphabet'.")
        if tape_output not in alfabeto_cinta:
            raise ValueError(f"El símbolo de salida '{tape_output}' en una transición no está en 'tape_alphabet'.")

        # Validar desplazamiento
        tape_displacement = output.get('tape_displacement')
        if tape_displacement not in ['L', 'R', 'S']:
            raise ValueError(f"El desplazamiento '{tape_displacement}' en una transición debe ser 'L', 'R' o 'S'.")

def construir_diccionario_transiciones(delta):
    """
    Construye un diccionario de transiciones a partir de la lista proporcionada en la configuración.
    """
    transiciones = {}
    for transicion in delta:
        params = transicion.get('params', {})
        output = transicion.get('output', {})

        initial_state = params.get('initial_state')
        tape_input = params.get('tape_input')

        final_state = output.get('final_state')
        tape_output = output.get('tape_output')
        tape_displacement = output.get('tape_displacement')

        clave = (initial_state, tape_input)
        valor = (final_state, tape_output, tape_displacement)

        if clave in transiciones:
            raise ValueError(f"Transición duplicada para el par {clave}.")

        transiciones[clave] = valor

    return transiciones

def procesar_configuracion(config):
    """
    Procesa la configuración y extrae los componentes necesarios para la simulación.
    """
    q_states = config['q_states']
    estados = q_states['q_list']
    estado_inicial = q_states['initial']
    estado_final = q_states['final']
    alfabeto = config['alphabet']
    alfabeto_cinta = config['tape_alphabet']
    delta = config['delta']
    #cadenas_aceptadas = config['accepted_strings']
    #cadenas_rechazadas = config['rejected_strings']
    blank_symbol = config.get('blank_symbol', '_')

    # Construir el diccionario de transiciones
    transiciones = construir_diccionario_transiciones(delta)

    configuracion_procesada = {
        'estados': estados,
        'estado_inicial': estado_inicial,
        'estado_final': estado_final,
        'alfabeto': alfabeto,
        'alfabeto_cinta': alfabeto_cinta,
        'transiciones': transiciones,
        #'accepted_strings': cadenas_aceptadas,
        #'rejected_strings': cadenas_rechazadas,
        'blank_symbol': blank_symbol
    }

    return configuracion_procesada
