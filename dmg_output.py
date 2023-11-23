#!/bin/python3
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline


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

dmg = 6   # Glommus has +6 on dmg roll
atks = 8  # Glommus has 8 attacks

damage_outputs = [(amount + dmg) * atks for amount in result.keys()]
probabilities = list(result.values())

x_smooth = np.linspace(min(damage_outputs), max(damage_outputs), 300)
y_smooth = make_interp_spline(damage_outputs, probabilities)(x_smooth)

plt.plot(x_smooth, y_smooth, label="Glommus' Damage Output")
plt.scatter(damage_outputs, probabilities, color='red', label='Data Points')

plt.xlabel('Total Dmg')
plt.ylabel('Probability')
plt.title("Glommus' Damage Output distribution")

plt.legend()
plt.savefig('glommus.png')
