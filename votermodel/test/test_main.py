
import sys, os

# add path to parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils import *


def main():

    node_vector_num = create_node_name_vector(15, "number")
    print(node_vector_num)

    node_vector_char = create_node_name_vector(79, "char")
    print(node_vector_char)

    node_value_list = create_node_value_vector(75)
    print(node_value_list)

    return 0



if __name__ == '__main__':
    main()