#!/bin/python3
import csv
from itertools import product
from matplotlib.font_manager import json
import matplotlib.pyplot as plt
import math
import os
import time

dmg = 6   # Glommus has +6 on dmg roll
atks = 8  # Glommus has 8 attacks


def calculate_probability():
    # Probability for one die
    p_uniq = 1 / 6

    # Initialize probabilities for each possible sum
    sum_probabilities = {i: float(0) for i in range(2, 13)}

    # Calculate all possibilities and their probabilities for two dice
    for i in range(1, 7):
        for j in range(1, 7):
            die1 = i
            die2 = j
            if die1 > 2 and die2 > 2:   # No Re-rolls
                sum_probabilities[die1 + die2] += p_uniq ** 2
            elif die1 > 2 or die2 > 2:  # Re-roll one
                for j2 in range(1, 7):
                    sum_probabilities[die1 + j2] += p_uniq ** 3
            else:                       # Re-roll both
                for j3 in range(1, 7):
                    for i3 in range(1, 7):
                        sum_probabilities[j3 + i3] += p_uniq ** 4

    return sum_probabilities


result = calculate_probability()
with open('p.csv', 'w', newline='\n') as f:
    writer = csv.writer(f)
    writer.writerows(result.items())

for total_sum, probability in result.items():
    print(
        f"The probability of getting a sum of {total_sum} is: {probability:.4f}")

all_rolls = [int(roll) for roll in result.keys()]
probabilities = list(result.values())

dmg_dist_file = "damage_distribution.json"
dmg_distribution = {}


def process_combination(combination, i=0):
    combination_dmg = sum(combination) + len(combination)*dmg
    curr_prob = math.prod(result[roll] for roll in combination)

    if combination_dmg not in dmg_distribution:
        dmg_distribution[combination_dmg] = curr_prob
    else:
        dmg_distribution[combination_dmg] += curr_prob
    if not i % 1e6:
        print(combination, curr_prob, f"{100*(i/11**8):.2f}%")


if os.path.isfile(dmg_dist_file):
    with open(dmg_dist_file, 'r') as f:
        dmg_distribution = json.load(f)
else:
    start_time = time.time()
    for i, combination in enumerate(product(all_rolls, repeat=8)):
        process_combination(combination, i)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Execution time:", elapsed_time, "seconds")

exampleAC = 17
exampleHP = 69
atk_mod = 10
p_miss = (exampleAC - atk_mod - 1) / 20
p_hit = 1 - p_miss
p_kill = sum([prob for dmg, prob in dmg_distribution.items() if int(dmg) >= exampleHP])
print(f"Example opponent AC: {exampleAC} HP: {exampleHP}")
print(f"If all Attacks hit, it would kill with the probability ~{p_kill*100:.2f}%")
print(f"With +{atk_mod} on Attack Rolls hits with p={p_hit*100:.2f}%")
print(f"Giving the final probability of killing the opponent: {p_kill*p_hit*100:.2f}%")

with open(dmg_dist_file, 'w') as f:
    json.dump(dmg_distribution, f)

dmg_outputs = [int(d) for d in dmg_distribution.keys()]
dmg_probs = list(dmg_distribution.values())

plt.plot(dmg_outputs, dmg_probs,
         label="Glommus' Damage Output")
plt.scatter(dmg_outputs, dmg_probs,
            color='red', label='Data Points')

plt.xlabel('Total Dmg')
plt.ylabel('Probability')
plt.title("Glommus' Damage Output distribution")

plt.legend()
plt.savefig('glommus.png')
