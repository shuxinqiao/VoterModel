from matplotlib.pyplot import axis
import numpy as np
from string import ascii_uppercase
from itertools import product


def create_node_name_vector(n, rep_type):

    """
    create a numpy array of names of nodes

    :param n: size of array, integer from 0 to 5000 \n
    :param rep_type: type of representation \n
                    "number" for 1,2,...,n \n
                    "char" for A,B,...,AA,AB,...

    :return: numpy.array() object
    """

    # size parameter check
    if n not in range(0,5000) or not (isinstance(n, int)):
        raise ValueError("argument n is either not in range(0,5000) or not integer")
    
    # number type node representation
    if rep_type == "number":
        
        # generate numpy array by size n
        node_name_vector = np.arange(n)

        return node_name_vector
    
    # letter type node representation
    if rep_type == "char":

        # generate numpy array by combination of 26 letters (e.g. AA,AB,AC)
        # get number of bits used for given n size
        bit_size = int( (n / 26) // 26) + 2
            
        node_name_list = []
        
        # combination of all possible bit size
        for i in range(bit_size):
            for letter in product(ascii_uppercase, repeat=i+1):
                node_name_list.append("".join(letter))

        # choose the n size
        node_name_vector = np.array(node_name_list[0:n])

        return node_name_vector
    
    # type argument check
    raise ValueError("argument rep_type is neither number nor char")


def create_node_value_vector(n, gen_type="uniform"):
    """
    create a numpy array of binary values of nodes \n
    0 for not believe, 1 for believe

    :param n: size of array, positive integer \n
    :param rep_type: (default = "uniform") the way assigning binary values

    :return: numpy.array() object
    """

    # size parameter check
    if (n < 0) or not (isinstance(n, int)):
        raise ValueError("argument n is neither positive nor integer")

    # generate n size numpy array with all 0
    node_value_vector = np.random.randint(2,size=n)
        
    return node_value_vector


def create_binary_matrix(n, gen_type="uniform", bin_p=False):
    """
    create a numpy symmetric matrix of binary value of nodes' relationship \n
    by reshaping the node_value array (depends on function: create_node_value_vector())

    :param n: n**2 is the size of matrix, positive integer \n
    :param gen_type: (default = "uniform") the way of assigning binary values

    :return: numpy.matrix() object
    """
    
    # size parameter check
    if (n < 0) or not (isinstance(n, int)):
        raise ValueError("argument n is neither positive nor integer")

    # unifrom generation method
    if gen_type == "uniform":
        node_array = create_node_value_vector(n**2, gen_type)
        reshaped_node_matrix = node_array.reshape(n, n)

        # node_matrix may have 1 in its diagonals so fill them with ones
        np.fill_diagonal(reshaped_node_matrix, 1)

        # complete the graph with right relationships
        node_matrix = np.bitwise_or(reshaped_node_matrix,reshaped_node_matrix.transpose())

        return node_matrix


    # binomial generation method given each row with binomial
    elif gen_type == "binomial":

        if not bin_p:
            raise ValueError("binomial probility not given")
        
        else:
            for i in range(n):
                # create row of node matrix, E[1(all j in row)] = n * bin_p
                node_matrix = np.random.binomial(1,bin_p,(n,n))
            
            np.fill_diagonal(node_matrix, 1)

            return node_matrix
    
    else:
        raise ValueError("gen_type wrong")



def transition_rate(node_matrix, node_vector):
    """
    calculate mean influence each node received from its relationships.

    :param node_matrix: n by n shape numpy matrix \n
    :param node_vector: n by 1 shape numpy array

    :return: n by 1 numpy array
    """

    vector_n = node_vector.shape[0]

    # giving directed weighted graph by transpose matrix
    mean_influence_vector = node_matrix.T.dot(node_vector)
    node_divide = node_matrix.sum(axis=0)

    # convert the vector into float type to calculate probability
    mean_influence_vector = mean_influence_vector.astype(np.float)

    for i in range(vector_n):
        mean_influence_vector[i] = mean_influence_vector[i] / node_divide[i]

    return mean_influence_vector


def change_node_value(node_vector, forward_transition_vector, backward_transition_vector):
    """
    random choose to flip 1 to 0 or 0 to 1, depends on transition rate

    :param node_vector: n by 1 numpay array \n
    :param transition_vector: n by 1 numpy array \n

    :return: n by 1 numpy array
    """
        
    for i in range(node_vector.shape[0]):
        if node_vector[i] == 0:
            node_vector[i] = np.random.binomial(1,forward_transition_vector[i])

        elif node_vector[i] == 1:
            node_vector[i] = 1 - np.random.binomial(1,backward_transition_vector[i])

    return node_vector

