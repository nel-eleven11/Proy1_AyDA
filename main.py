# main.py

from parser_yaml import cargar_configuracion, validar_configuracion, procesar_configuracion
from mt import simular_mt
from utils import mostrar_ids
import os

def main():

    print("\nProyecto 3 - Teoría de la Computación")
    print("Autores:")
    print("Nelson García 22434")
    print("Rodrigo Mansilla 22611\n")
    
    while True:
        print("Máquinas de Turing Reconocedoras")
        print("Seleccione la Máquina de Turing a simular:")
        print("1. Probar MT de Fibonacci")
        print("0. Salir")
        
        seleccion = input("Ingrese el número de la opción deseada: ").strip()


        if seleccion == '0':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        elif seleccion not in ['1']:
            print("Selección inválida. Por favor, ingrese 1 o 0.\n")
            continue

        # Definir las rutas de los archivos YAML para cada máquina
        yaml_files = {
            '1': 'mt1.yaml',
        }
        
        archivo_yaml = yaml_files.get(seleccion)
        
        if not archivo_yaml:
            print("Archivo YAML no definido para la selección.\n")
            continue
        
        # Verificar que el archivo YAML existe
        if not os.path.isfile(archivo_yaml):
            print(f"Error: El archivo YAML '{archivo_yaml}' no fue encontrado.\n")
            continue
        
        try:
            # Cargar y procesar la configuración
            config = cargar_configuracion(archivo_yaml)
            validar_configuracion(config)
            configuracion_procesada = procesar_configuracion(config)

            # Menú para seleccionar categoría de cadenas basado en la máquina seleccionada
            while True:
                print("\nCategorías de Cadenas:")
                
                # Definir categorías según la máquina seleccionada
                if seleccion == '1':
                    print("1. Cadenas ACEPTADAS")
                    print("2. Cadenas RECHAZADAS")
                    print("3. Simular ambas categorías")
                elif seleccion == '2':
                    print("1. Cadenas ACEPTADAS")
                    print("2. Simular todas las cadenas ACEPTADAS")
                
                print("0. Volver al menú principal")
                
                categoria = input("Ingrese el número de la categoría deseada: ").strip()

                if categoria == '0':
                    print()
                    break
                elif seleccion == '1' and categoria not in ['1', '2', '3']:
                    print("Selección inválida. Por favor, ingrese 1, 2, 3 o '0'.\n")
                    continue
                elif seleccion == '2' and categoria not in ['1', '2']:
                    print("Selección inválida. Por favor, ingrese 1, 2 o '0'.\n")
                    continue

                # Obtener las cadenas según la categoría seleccionada
                if seleccion == '1':
                    if categoria == '1':
                        cadenas = config['accepted_strings']
                        categoria_texto = "Cadenas ACEPTADAS"
                    elif categoria == '2':
                        cadenas = config['rejected_strings']
                        categoria_texto = "Cadenas RECHAZADAS"
                    elif categoria == '3':
                        cadenas = config['accepted_strings'] + config['rejected_strings']
                        categoria_texto = "Cadenas ACEPTADAS y RECHAZADAS"
                elif seleccion == '2':
                    if categoria == '1':
                        cadenas = config['accepted_strings']
                        categoria_texto = "Cadenas ACEPTADAS"
                    elif categoria == '2':
                        cadenas = config['accepted_strings']
                        categoria_texto = "Cadenas ACEPTADAS"
                        # La opción 2 para la Máquina 2 es simular todas las cadenas aceptadas

                if not cadenas:
                    print(f"No hay cadenas definidas en la categoría '{categoria_texto}'.\n")
                    continue

                print(f"\n{categoria_texto}:")
                for idx, cadena in enumerate(cadenas, start=1):
                    print(f"{idx}. '{cadena}'")
                
                # Definir las opciones de selección de cadenas basadas en la máquina
                if seleccion == '1':
                    print("0. Simular todas las cadenas de la categoría")
                elif seleccion == '2':
                    print("0. Simular todas las cadenas ACEPTADAS")

                seleccion_cadenas = input("Seleccione las cadenas a simular (ej. 1,3,5) o '0' para todas: ").strip()

                if seleccion_cadenas == '0':
                    cadenas_seleccionadas = cadenas
                else:
                    indices = seleccion_cadenas.split(',')
                    try:
                        indices = [int(idx.strip()) for idx in indices]
                        # Para Máquina 2, aunque la opción 2 también selecciona aceptadas,
                        # nos aseguramos de que solo se seleccionen aceptadas.
                        if seleccion == '1' and categoria == '3':
                            # En caso de seleccionar ambas categorías, no hay duplicados
                            # simplemente selecciona todas las cadenas.
                            cadenas_seleccionadas = [cadenas[idx - 1] for idx in indices if 1 <= idx <= len(cadenas)]
                        else:
                            cadenas_seleccionadas = [cadenas[idx - 1] for idx in indices if 1 <= idx <= len(cadenas)]
                        if not cadenas_seleccionadas:
                            print("No se seleccionaron cadenas válidas.\n")
                            continue
                    except (ValueError, IndexError):
                        print("Entrada inválida. Por favor, ingrese números separados por comas o '0'.\n")
                        continue

                # Simular las cadenas seleccionadas
                for cadena in cadenas_seleccionadas:
                    print(f"\nSimulando cadena: '{cadena}'")
                    ids, aceptada = simular_mt(configuracion_procesada, cadena)
                    mostrar_ids(ids)
                    if aceptada:
                        print("Resultado: La cadena es ACEPTADA.")
                    else:
                        print("Resultado: La cadena es RECHAZADA.")
                    print('=' * 50)
        
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == '__main__':
    main()
