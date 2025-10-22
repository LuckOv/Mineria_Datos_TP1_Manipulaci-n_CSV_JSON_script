# main.py
from funcionesCSV_v3 import (
    csv_a_diccionarios, agregar_registro, borrar_por_indice, modificar_interactivo,
    json_a_diccionarios, agregar_registro_json, borrar_por_indice_json, modificar_interactivo_json
)
import os
import csv
import json

def determinar_formato(archivo):
    """Determina si el archivo es CSV o JSON por su extensión"""
    if archivo.lower().endswith('.json'):
        return 'json'
    elif archivo.lower().endswith('.csv'):
        return 'csv'
    else:
        return None

def mostrar_menu(archivo_actual, formato_actual):
    """Muestra el menú principal actualizado"""
    print("\n" + "="*50)
    print("GESTOR DE ARCHIVOS CSV/JSON")
    print("="*50)
    if archivo_actual:
        print(f"Archivo actual: {archivo_actual} ({formato_actual.upper()})")
    else:
        print("Archivo actual: Ninguno")
    print("="*50)
    print("1. Cargar archivo (CSV/JSON)")
    print("2. Leer y mostrar registros")
    print("3. Agregar nuevo registro")
    print("4. Borrar registro")
    print("5. Modificar registro")
    print("6. Salir")
    print("="*50)

def mostrar_registros(registros, archivo):
    """Muestra los registros de forma legible"""
    if not registros:
        print(f"No hay registros en '{archivo}'")
        return
    
    print(f"\n--- REGISTROS EN '{archivo}' ({len(registros)}): ---")
    for i, registro in enumerate(registros, 1):
        print(f"Registro {i}:")
        for campo, valor in registro.items():
            print(f"  {campo}: {valor}")
        print("-" * 40)

def pedir_datos_registro(campos):
    """Pide los datos para un nuevo registro basado en los campos del archivo"""
    print(f"\nIngrese los datos del nuevo registro:")
    registro = {}
    
    for campo in campos:
        valor = input(f"{campo}: ").strip()
        registro[campo] = valor
    
    return registro

def obtener_campos_desde_archivo(archivo, formato):
    """Obtiene los campos (encabezados) de un archivo existente"""
    try:
        if formato == 'csv':
            with open(archivo, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return reader.fieldnames
        else:  # json
            datos = json_a_diccionarios(archivo)
            if datos and len(datos) > 0:
                return list(datos[0].keys())
            return None
    except:
        return None

def cargar_archivo():
    """Permite al usuario cargar un archivo CSV o JSON"""
    print("\n📁 CARGAR ARCHIVO CSV/JSON")
    archivo = input("Ingrese el nombre del archivo (ej: datos.csv o datos.json): ").strip()
    
    if not archivo:
        print("No se ingresó ningún nombre de archivo")
        return None, None
    
    formato = determinar_formato(archivo)
    if formato is None:
        print("Formato no soportado. Use .csv o .json")
        return None, None
    
    if not os.path.exists(archivo):
        crear = input(f"El archivo '{archivo}' no existe. ¿Crearlo? (s/n): ").strip().lower()
        if crear == 's':
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    if formato == 'json':
                        json.dump([], f)
                    # Para CSV se crea vacío
                print(f"Archivo '{archivo}' creado exitosamente")
                return archivo, formato
            except Exception as e:
                print(f"Error al crear archivo: {e}")
                return None, None
        else:
            print("Operación cancelada")
            return None, None
    else:
        print(f"Archivo '{archivo}' cargado exitosamente")
        return archivo, formato

def verificar_archivo_cargado(archivo_actual):
    """Verifica si hay un archivo cargado"""
    if not archivo_actual:
        print("\n❌ Error: Primero debe cargar un archivo (Opción 1)")
        return False
    return True

def main():
    """Función principal actualizada"""
    archivo_actual = None
    formato_actual = None
    
    while True:
        mostrar_menu(archivo_actual, formato_actual)
        
        try:
            opcion = input("\nSeleccione una opción (1-6): ").strip()
            
            match opcion:
                case "1":
                    nuevo_archivo, nuevo_formato = cargar_archivo()
                    if nuevo_archivo:
                        archivo_actual = nuevo_archivo
                        formato_actual = nuevo_formato
                
                case "2":
                    if not verificar_archivo_cargado(archivo_actual):
                        continue
                    
                    print(f"\n Leyendo archivo '{archivo_actual}'...")
                    try:
                        if formato_actual == 'csv':
                            registros = csv_a_diccionarios(archivo_actual)
                        else:  # json
                            registros = json_a_diccionarios(archivo_actual)
                        mostrar_registros(registros, archivo_actual)
                    except Exception as e:
                        print(f" Error al leer el archivo: {e}")
                
                case "3":
                    if not verificar_archivo_cargado(archivo_actual):
                        continue
                    
                    print(f"\n AGREGAR NUEVO REGISTRO A '{archivo_actual}'")
                    try:
                        campos = obtener_campos_desde_archivo(archivo_actual, formato_actual)
                        if campos is None:
                            campos_input = input("Ingrese los nombres de los campos separados por coma: ").strip()
                            campos = [campo.strip() for campo in campos_input.split(',')]
                        
                        datos_registro = pedir_datos_registro(campos)
                        
                        if formato_actual == 'csv':
                            if all(datos_registro.values()):
                                agregar_registro(archivo_actual, datos_registro)
                            else:
                                print(" Todos los campos son obligatorios")
                        else:  # json
                            agregar_registro_json(archivo_actual, datos_registro)
                    except Exception as e:
                        print(f" Error al agregar registro: {e}")
                
                case "4":
                    if not verificar_archivo_cargado(archivo_actual):
                        continue
                    
                    print(f"\n BORRAR REGISTRO DE '{archivo_actual}'")
                    try:
                        if formato_actual == 'csv':
                            registros = csv_a_diccionarios(archivo_actual)
                        else:
                            registros = json_a_diccionarios(archivo_actual)
                        
                        if not registros:
                            print(" No hay registros para borrar")
                            continue
                        
                        mostrar_registros(registros, archivo_actual)
                        
                        try:
                            indice = int(input("\nIngrese el número del registro a borrar (1, 2, 3...): ")) - 1
                            
                            if 0 <= indice < len(registros):
                                registro_a_borrar = registros[indice]
                                print(f"\nRegistro seleccionado para borrar:")
                                for campo, valor in registro_a_borrar.items():
                                    print(f"  {campo}: {valor}")
                                
                                confirmacion = input("¿Está seguro de borrar este registro? (s/n): ").strip().lower()
                                
                                if confirmacion == 's':
                                    if formato_actual == 'csv':
                                        borrados = borrar_por_indice(archivo_actual, indice)
                                    else:
                                        borrados = borrar_por_indice_json(archivo_actual, indice)
                                    print(f" Se borró {borrados} registro(s)")
                                else:
                                    print(" Operación cancelada")
                            else:
                                print(" Número de registro inválido")
                        except ValueError:
                            print(" Por favor ingrese un número válido")
                    except Exception as e:
                        print(f" Error al borrar registro: {e}")
                
                case "5":
                    if not verificar_archivo_cargado(archivo_actual):
                        continue
                    
                    print(f"\n MODIFICAR REGISTRO EN '{archivo_actual}'")
                    try:
                        if formato_actual == 'csv':
                            modificar_interactivo(archivo_actual)
                        else:
                            modificar_interactivo_json(archivo_actual)
                    except Exception as e:
                        print(f" Error al modificar registro: {e}")
                
                case "6":
                    print("\n ¡Gracias por usar el sistema! ¡Hasta pronto!")
                    break
                
                case _:
                    print(" Opción no válida. Por favor, seleccione 1-6.")
        
        except KeyboardInterrupt:
            print("\n\n Programa interrumpido por el usuario")
            break
        except Exception as e:
            print(f" Error inesperado: {e}")

if __name__ == "__main__":
    main()