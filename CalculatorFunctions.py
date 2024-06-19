from HonkaiBotData import *
from char_weights import *
# Function to calculate the scores of flat values
def flat_stat_calculate_score(stat, value, base_stat):
    flat_normalization = (1 / (2 * Argenti_base_stats[base_stat] * 0.01)) * (64.8 / main_flat_values[base_stat])
    weight = Argenti_weights[stat]
    score = weight * flat_normalization * value
    return score

def calculate_score(stat, value):
    print(f"Checking stat: {stat}")
    if stat in normalizations and stat in Argenti_weights:
        normalization = normalizations[stat]
        weight = Argenti_weights[stat]
        score = weight * normalization * value
        print(f"Score calculated: {score}")
        return score
    elif stat.startswith('FLAT_'):
        base_stat = stat.split('_')[1]
        return flat_stat_calculate_score(stat, value, base_stat)
    else:
        print("Stat not found in normalizations or Argenti_weights")
        return 0
    
# Function to calculate the total score for four stats
def calculate_total_score(stats):
    total_score = 0
    for stat, value in stats.items():
        score = calculate_score(stat, value)
        total_score += score
    return total_score
