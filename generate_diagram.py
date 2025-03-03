import yaml
from graphviz import Digraph

# Cargar la configuración desde el archivo YAML
with open('mt1.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Extraer los estados y las transiciones
states = config['q_states']['q_list']
initial_state = config['q_states']['initial']
final_state = config['q_states']['final']
transitions = config['delta']

# Crear el grafo dirigido
dot = Digraph(comment="Diagrama de la Máquina de Turing")

# Agregar nodos (estados)
for state in states:
    # Distinguir el estado inicial y final
    if state == final_state:
        dot.node(state, state, shape='doublecircle')
    elif state == initial_state:
        dot.node(state, state, style='filled', fillcolor='lightgrey')
    else:
        dot.node(state, state)

# Agregar aristas (transiciones)
for trans in transitions:
    ini = trans['params']['initial_state']
    tape_in = trans['params']['tape_input']
    fin = trans['output']['final_state']
    tape_out = trans['output']['tape_output']
    displacement = trans['output']['tape_displacement']
    label = f"{tape_in} / {tape_out}, {displacement}"
    dot.edge(ini, fin, label=label)

# Guardar y/o visualizar el diagrama
dot.render('turing_machine_diagram', format='png', view=False)
