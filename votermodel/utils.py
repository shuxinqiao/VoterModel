from matplotlib.pyplot import axis
import numpy as np
from string import ascii_uppercase
from itertools import product
from math import ceil

from numpy.core.numeric import normalize_axis_tuple


# asking user setting parameters (termial, no external GUI)
def user_prompt(n,loop_time,relation_size_mean,value_size_mean,self_choice,diagonal_mean,model_choice,upper_range,upper_limit):
    """
    Ask user to set parameters, all parameters have default value.

    :param n: size of population, integer from 0 to upper_limit \n
    :param loop_time: loop time for simulation \n
    :param relation_size_mean: relation expected links for one \n
    :param value_size_mean: number of believers for initial condition \n
    :param diagonal_mean: expected value for diagonal_ \n 
    :param upper_range: upper limit for uniform RV range \n
    :param upper_limit: general numerical limit for possible runs \n

    :return: all parameters in input order
    """
    setting_progress = False

    while not setting_progress:
       
        print("-----setting parameters-----\n")
        print("Please enter correct format. Press enter key to submit.\n")

        try:
            
            # population size prompt
            n = int(input("1.Population size (integer only from (0,{}] (default:500)): ".format(upper_limit)) or "500")
            if n not in range(0,upper_limit+1):
                raise ValueError 
            

            # loop time prompt
            loop_time = int(input("2.Loop time (integer only from (0,{}] (default:100)): ".format(upper_limit)) or "100")
            if loop_time not in range(0,upper_limit+1):
                raise ValueError 
            

            # expected relation size prompt
            relation_size_mean = int(input("3.Expected relation size (integer only from (0,{}] (default:n/2)): ".format(n)) or n//2)
            if relation_size_mean not in range(0,n+1):
                raise ValueError 
            

            # expected believer size prompt
            value_size_mean = int(input("4.Expected believers size (integer only from (0,{}] (default:n/2)): ".format(n)) or n//2)
            if value_size_mean not in range(0,n+1):
                raise ValueError 


            # self confidence method prompt
            self_choice = input("5.Exact value for self confidence or Expected value (uniformly)? type (e/u) (default:e): ")

            # expected self confidence prompt
            if self_choice == "e" or self_choice == "u":
                diagonal_mean = float(input("  -> 5.1.Expected self-confidence value (float from (0,{}] (default:1)): ".format(upper_limit)) or "1")
                if ceil(diagonal_mean) not in range(0,upper_limit+1):
                    raise ValueError

            elif self_choice == "":
                self_choice = "e"
                diagonal_mean = 1
            
            else:
                raise ValueError
            

            # model prompt 
            model_choice = input("6.Binary relation (1/0) or Float value relation (uniformly)? type (b/f) (default:b): ")
            if model_choice == "b":
                pass

            # float model requires expected value for uniform distribution
            elif model_choice == "f":
            
                upper_range = float(input("  -> 6.1.Expected relation strength value (float from (0,{}] (default:self-confidence({}))): ".format(upper_limit,diagonal_mean)) or "1")
                if ceil(upper_range) not in range(0,upper_limit+1):
                    raise ValueError 

                upper_range = upper_range*2

            elif model_choice == "":
                model_choice = "b"
            
            else:
                raise ValueError

                
            # Final running prompt
            quit_sign = input("Run the simulation now? type (y/n) (default:y): ")
            if quit_sign == "y":
                setting_progress = True
            
            elif quit_sign == "n":
                exit()
            
            elif quit_sign:
                raise ValueError

            else:
                setting_progress = True


        except ValueError:
            print("\n!!! input wrong, please try again. !!!\n")
            input("press enter to try again\n")


    return (n,loop_time,relation_size_mean,value_size_mean,self_choice,diagonal_mean,model_choice,upper_range)


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


def create_node_value_vector(n, gen_type="binomial", bin_p=False):
    """
    create a numpy array of binary values of nodes \n
    0 for not believe, 1 for believe

    :param n: size of array, positive integer \n
    :param rep_type: (default = "binomial") the way assigning binary values

    :return: numpy.array() object
    """

    # size parameter check
    if (n < 0) or not (isinstance(n, int)):
        raise ValueError("argument n is neither positive nor integer")

    
    if gen_type == "binomial":
        
        if not bin_p:
            raise ValueError("binomial probility not given")
        
        else:
            # create node vector, E[1(all j in row)] = n * bin_p
            node_value_vector = np.random.binomial(1,bin_p,(n,1))

            return node_value_vector
    
    else:
        raise ValueError("Wrong generation type")


def create_matrix(n, gen_type="binomial", gen_param=False):
    """
    create a numpy symmetric matrix of binary value of nodes' relationship \n
    by reshaping the node_value array (depends on function: create_node_value_vector())

    :param n: n**2 is the size of matrix, positive integer \n
    :param gen_type: (default = "binomial") the way of assigning values
    :param gen_param: value for binomial;  range for uniform

    :return: numpy.matrix() object
    """
    
    # size parameter check
    if (n < 0) or not (isinstance(n, int)):
        raise ValueError("argument n is neither positive nor integer")


    # binomial generation method given each row with binomial
    if gen_type == "binomial":

        if not gen_param:
            raise ValueError("binomial probility not given")
        
        else:
            # create row of node matrix, E[1(all j in row)] = n * bin_p
            node_matrix = np.random.binomial(1,gen_param,(n,n))

            return node_matrix

    # uniform continuous generation method given each row with RV from range
    elif gen_type == "uniform":

        if not gen_param:
            raise ValueError("uniform range not given")
        
        else:

            node_matrix = np.random.uniform(high=float(gen_param),size=n**2)
            node_matrix = np.reshape(node_matrix,(n,n))

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

