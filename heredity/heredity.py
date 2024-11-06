import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    '''
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    '''
    people=load_data("data/family0.csv")
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
    
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")

    
def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    lista=[]
    join_prob=1
    #===================TWO GENES=============================
    for name in people:
        prob_m=1
        prob_f=1
        mother=people[name]['mother']
        father=people[name]['father']
        
        # GETS FROM MAMA 
        if mother is None:
            prob_m=PROBS['gene'][2]   
        if mother is not None:
            if mother in two_genes:
                prob_m=1-PROBS['mutation']
            elif mother in one_gene:
                prob_m=0.5
            else:
                prob_m=PROBS['mutation']
                
        #GETS FROM PAPA
        if father is None:
            prob_f=PROBS['gene'][2]
        if father is not None:
            if father in two_genes:
                prob_f=1-PROBS['mutation']
            elif father in one_gene:
                prob_f=0.5
            else:
                prob_f=PROBS['mutation']

                
        if name in one_gene:
            trait_prob=PROBS['trait'][1]
            if mother is None and father is None:
                join_prob=PROBS['gene'][1]
                #print(f"1 gen {join_prob}")
            else:
                join_prob=prob_m*(1-prob_f)+(1-prob_m)*prob_f
                #print(f"1 gen {join_prob}")
        if name in two_genes:
            trait_prob=PROBS['trait'][2]
            if mother is None and father is None:
                join_prob=PROBS['gene'][2]
                #print(f"2 gen {join_prob}")
            else:
                join_prob=prob_m*prob_f
                #print(f"2 gen {join_prob}")
        if name not in one_gene and name not in two_genes:
            trait_prob=PROBS['trait'][0]
            if mother is None and father is None:
                join_prob=PROBS['gene'][0]
                #print(f"0 gen {join_prob}")
            else:
                join_prob=(1-prob_m)*(1-prob_f)
                #print(f"0 gen {join_prob}")
                
        if name in have_trait:
            join_prob=join_prob*trait_prob[True]
        else:
            join_prob=join_prob*trait_prob[False]
        lista.append(join_prob)
        
    result=1
    for prob in lista:
        result*=prob
    return result

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        gen=(1 if person in one_gene else 2 if person in two_genes else 0)
        trait=(person in have_trait)
        probabilities[person]["gene"][gen]+=p
        probabilities[person]["trait"][trait]+=p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        suma=sum(list(probabilities[person]["gene"].values()))
        for key,prob in probabilities[person]["gene"].items():
            probabilities[person]["gene"][key]=prob/suma
        suma=sum(list(probabilities[person]["trait"].values()))
        for key,prob in probabilities[person]["trait"].items():
            probabilities[person]["trait"][key]=prob/suma
        
    #raise NotImplementedError






if __name__ == "__main__":
    
    main()
