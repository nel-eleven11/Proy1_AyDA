# utils.py

def mostrar_ids(ids):
    """
    Muestra las descripciones instantáneas almacenadas durante la simulación.

    :param ids: Lista de descripciones instantáneas.
    """
    for id in ids:
        paso = id['paso']
        estado = id['estado']
        cinta = id['cinta']
        cabezal = id['cabezal']
        print(f"Paso {paso}:")
        print(f"Estado: {estado}")
        print(f"Cinta: {cinta}")
        # Mostrar el cabezal como un símbolo '^' debajo de la posición actual
        cabezal_visual = ' ' * cabezal + '^'
        print(f"       {cabezal_visual}")
        print('-' * 50)
