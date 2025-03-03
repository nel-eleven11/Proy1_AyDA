# main.py

from parser_yaml import cargar_configuracion, validar_configuracion, procesar_configuracion
from mt import simular_mt
from utils import mostrar_ids
import os
import cProfile
import pstats

def main():

    print("\nProyecto 1 - Análisis y Diseño de Algoritmos")
    print("Autores:")
    print("Nelson García 22434")
    print("Joaquín Puente 22296\n")
    
    print("Máquinas de Turing Reconocedoras")

    # Definir las rutas de los archivos YAML para cada máquina
    yaml_files = {
        '1': 'mt1.yaml',
    }
    
    archivo_yaml = yaml_files.get('1')
    
    if not archivo_yaml:
        print("Archivo YAML no definido para la selección.\n")
        exit(1)    
    # Verificar que el archivo YAML existe
    if not os.path.isfile(archivo_yaml):
        print(f"Error: El archivo YAML '{archivo_yaml}' no fue encontrado.\n")
        exit(1) 

    try:
        # Cargar y procesar la configuración
        config = cargar_configuracion(archivo_yaml)
        validar_configuracion(config)
        configuracion_procesada = procesar_configuracion(config)

        # Menú para seleccionar categoría de cadenas basado en la máquina seleccionada
        while True:

            enesimo = int(input('Ingrese el n número que desea de Fibbonacci (0 para salir):\n'))
            if enesimo == 0:
                print('Saliendo del programa')
                exit(0)

            cadena_sim = ''
            for i in range(enesimo):
                cadena_sim += '1' 

            # Simular las cadenas seleccionadas
            # for cadena in cadenas_seleccionadas:
            print(f"\nSimulando cadena: '{cadena_sim}'")
            profiler = cProfile.Profile()
            profiler.enable()
            ids, aceptada = simular_mt(configuracion_procesada, cadena_sim)
            profiler.disable()
            mostrar_ids(ids)
            if aceptada:
                print("Resultado: La cadena es ACEPTADA.")
            else:
                print("Resultado: La cadena es RECHAZADA.")
            print('=' * 50)
            print('===============================================')
            print(f'EL N-ESIMO NÚMERO DE FIBBONACCI: {ids[-1]['cinta'].count('1')}')
            stats = pstats.Stats(profiler).sort_stats('cumulative')
            stats.print_stats()

    except Exception as e:
        print(f"Error: {e}\n")

if __name__ == '__main__':

    main()

