import numpy as np
from string import ascii_uppercase
from itertools import combinations, product

# create a numpy array of name of nodes
def create_node_name_vector(n, rep_type):

    # size argument check
    if n not in range(0,5000):
        raise ValueError("argument n is not in range(0,5000)")
    
    # number type node representation
    if rep_type == "number":
        
        # generate numpy array by size n
        node_name_vector = np.arange(n)

        return node_name_vector
    
    # letter type node representation
    if rep_type == "char":

        # generate numpy array by combination of 26 letters (e.g. AA,AB,AC)
        bit_size = int( (n / 26) // 26) + 2
            
        node_name_list = []
        
        for i in range(bit_size):
            for letter in product(ascii_uppercase, repeat=i+1):
                node_name_list.append("".join(letter))

        node_name_vector = np.array(node_name_list[0:n])

        return node_name_vector
    
    # type argument check
    raise ValueError("argument rep_type is neither number nor char")


# create a numpy array of binary value of nodes
def create_node_value_vector(n, gen_type="uniform"):

    # generate n size numpy array with all 0
    node_value_list = np.zeros(n, dtype=int)

    # uniform distributed 0/1 to all n nodes
    if gen_type == "uniform":

        # random.randint uses discrete uniform distribution
        selection_list = np.random.randint(0,n,n//2)
        
        # change the selected nodes' value
        for i in selection_list:
            node_value_list[i] = 1
        
        return node_value_list
