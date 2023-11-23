#!/bin/python3
import csv


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
