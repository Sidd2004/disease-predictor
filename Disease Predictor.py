from itertools import combinations
from collections import defaultdict
def load_medical_data():
    # Sample medical dataset
    medical_dataset = [
        {'Fever', 'Cough', 'Headache',},
        {'Cough', 'SoreThroat', 'Fatigue'},
        {'Fever', 'Nausea', 'Vomiting'},
        {'Headache', 'RunnyNose', 'Sneezing'},
        # Add more patient records as needed
    ]
    return medical_dataset

def create_candidates(medical_dataset, symptom_set_size):
    candidates = set()
    for patient_record in medical_dataset:
        for candidate in combinations(patient_record, symptom_set_size):
            candidates.add(candidate)
    return candidates

def prune_candidates(candidates, frequent_itemsets_prev):
    pruned_candidates = set()
    for candidate in candidates:
        subsets = set(combinations(candidate, len(candidate) - 1))
        if all(subset in frequent_itemsets_prev for subset in subsets):
            pruned_candidates.add(candidate)
    return pruned_candidates

def generate_frequent_itemsets(medical_dataset, min_support):
    symptom_set_size = 1
    frequent_itemsets = defaultdict(int)
    
    while True:
        candidates = create_candidates(medical_dataset, symptom_set_size)
        if not candidates:
            break
        
        if symptom_set_size > 1:
            candidates = prune_candidates(candidates, frequent_itemsets_prev)

        for patient_record in medical_dataset:
            for candidate in candidates:
                if set(candidate).issubset(patient_record):
                    frequent_itemsets[candidate] += 1

        frequent_itemsets_prev = {itemset for itemset, count in frequent_itemsets.items() if count >= min_support}
        if not frequent_itemsets_prev:
            break

        symptom_set_size += 1

    return frequent_itemsets

def find_diseases(user_input, frequent_itemsets):
    user_symptoms = set(user_input.split(','))
    potential_diseases = []

    for symptom_set, support in frequent_itemsets.items():
        if user_symptoms.issubset(symptom_set):
            potential_diseases.append(symptom_set)

    return potential_diseases

def main():
    # Load medical data
    medical_dataset = load_medical_data()

    # Set minimum support threshold
    min_support = 2

    # Generate frequent itemsets
    frequent_itemsets = generate_frequent_itemsets(medical_dataset, min_support)

    # User input
    user_input = input("Enter symptoms separated by commas: ")

    # Find potential diseases
    potential_diseases = find_diseases(user_input, frequent_itemsets)

    # Print results
    if potential_diseases:
        print("Potential Diseases:")
        for disease in potential_diseases:
            if user_input == disease:
                pass
            else:
                    print(f"Disease: {disease}")
    else:
        print("No matching diseases found.")

if __name__ == "__main__":
    main()
