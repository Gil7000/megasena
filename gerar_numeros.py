import sqlite3
import random
from itertools import combinations

def get_results_from_db():
    conn = sqlite3.connect('megasena.db')
    cursor = conn.cursor()
    cursor.execute("SELECT bola1, bola2, bola3, bola4, bola5, bola6 FROM resultados")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def generate_megasena_numbers():
    return sorted(random.sample(range(1, 61), 6))

def is_combination_unique(generated_numbers, results):
    generated_combinations = set(combinations(generated_numbers, 4))
    for result in results:
        result_combinations = set(combinations(result, 4))
        if not generated_combinations.isdisjoint(result_combinations):
            return False
    return True

results = get_results_from_db()

unique = False
while not unique:
    new_numbers = generate_megasena_numbers()
    if is_combination_unique(new_numbers, results):
        unique = True

print("Números gerados para a MegaSena:", new_numbers)
