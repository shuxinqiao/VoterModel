import sys, os

# add path to parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils import *


def main():

    node_vector_num = create_node_name_vector(15, "number")
    #print(node_vector_num)

    node_vector_char = create_node_name_vector(79, "char")
    #print(node_vector_char)

    node_value_vector = create_node_value_vector(5)
    print(node_value_vector)

    node_binary_matrix = create_binary_matrix(5)
    print(node_binary_matrix)

    mean_influence_vector = mean_influence(node_binary_matrix, node_value_vector)
    print(mean_influence_vector)



    return 0



if __name__ == '__main__':
    main()