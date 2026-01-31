import csv
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    file = filedialog.askopenfilename(
        title="Seleccionar archivo CSV de personas",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    root.destroy()

    return file if file else None


def load_data(file_path):
    people = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                person = {
                    'nombre': row['nombre'],
                    'edad': int(row['edad']),
                    'altura': float(row['altura']),
                    'peso': float(row['peso']),
                    'localidad': row['localidad']
                }
                people.append(person)

        return people
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}'")
        return None
    except Exception as ex:
        print(f"Error al cargar el archivo: {ex}")
        return None


def calculate_average_age(people):
    print("1. ANÁLISIS DE EDAD")

    total_age = sum(p['edad'] for p in people)
    average_age = total_age / len(people)
    print(f"Media de edad: {average_age:.2f} años")
    print("\n")


def younger_and_older(people):
    print("2. PERSONA MÁS JOVEN Y MÁS VIEJA")
    
    youngest_person = min(people, key=lambda p: p['edad'])
    oldest_person = max(people, key=lambda p: p['edad'])
    
    print("Persona más joven:")
    show_person(youngest_person)
    print("\n")

    print("\nPersona más vieja:")
    show_person(oldest_person)
    print("\n")


def calculate_average_height(people):
    print("3. ANÁLISIS DE ALTURA")

    total_height = sum(p['altura'] for p in people)
    average_height = total_height / len(people)
    print(f"Media de altura: {average_height:.2f} metros")
    print("\n")


def tallest_and_smallest(people):
    print("4. PERSONA MÁS ALTA Y MÁS BAJA")
    
    tallest_person = max(people, key=lambda p: p['altura'])
    smallest_person = min(people, key=lambda p: p['altura'])
    
    print("Persona más alta:")
    show_person(tallest_person)
    print("\n")
    
    print("\nPersona más baja:")
    show_person(smallest_person)
    print("\n")


def heavier_and_lighter(people):
    print("5. PERSONA CON MÁS PESO Y MENOS PESO")
    
    heavier_person = max(people, key=lambda p: p['peso'])
    lighter_person = min(people, key=lambda p: p['peso'])
    
    print("Persona con más peso:")
    show_person(heavier_person)
    print("\n")

    print("\nPersona con menos peso:")
    show_person(lighter_person)
    print("\n")


def analyze_cities(people):
    print("6. LOCALIDAD CON MÁS PERSONAS")
    
    total_cities = {}
    for person in people:
        city = person['localidad']
        total_cities[city] = total_cities.get(city, 0) + 1
    
    localidad_max = max(total_cities, key=total_cities.get)
    cantidad_max = total_cities[localidad_max]
    
    print(f"Localidad con más personas: {localidad_max}")
    print(f"Número de personas: {cantidad_max}")
    
    sorted_cities = sorted(total_cities.items(), key=lambda x: x[1], reverse=True)
    
    print("\nTop 5 localidades con más personas:")
    
    for i, (city, quantity) in enumerate(sorted_cities[:5], 1):
        print(f"{i}. {city}: {quantity} personas")
    print("\n")


def show_person(persona):
    print(f"  Nombre: {persona['nombre']}")
    print(f"  Edad: {persona['edad']} años")
    print(f"  Altura: {persona['altura']} m")
    print(f"  Peso: {persona['peso']} kg")
    print(f"  Localidad: {persona['localidad']}")


def make_analysis(people):
    print(f"Total de personas en el dataset: {len(people)}")
    
    calculate_average_age(people)
    younger_and_older(people)
    calculate_average_height(people)
    tallest_and_smallest(people)
    heavier_and_lighter(people)
    analyze_cities(people)


def main():
    print("Bienvenido")
    file_path = select_file()
    
    if not file_path:
        print("No se seleccionó ningún archivo.")
        return
    
    print(f"Archivo seleccionado: {file_path}")
    people = load_data(file_path)
    make_analysis(people)
pass

if __name__ == "__main__":
    main()