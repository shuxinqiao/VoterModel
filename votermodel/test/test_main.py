import sys, os

# add path to parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils import *
import matplotlib.pyplot as plt


def main():

    n = 50
    pop_rate = []
    run_times = []

    #node_vector_num = create_node_name_vector(n, "number")
    #print(node_vector_num)

    #node_vector_char = create_node_name_vector(n, "char")
    #print(node_vector_char)

    node_value_vector = create_node_value_vector(n)
    print(node_value_vector)

    node_binary_matrix = create_binary_matrix(n)
    print(node_binary_matrix)   
    #print(node_binary_matrix[1])

    pop_rate.append(np.mean(node_value_vector))
    run_times.append(0)

    for i in range(500):
        print("----------run ",i," ------------------")
        transition_rate_vector = transition_rate(node_binary_matrix, node_value_vector)
        #print(transition_rate_vector)

        reverse_node_value_vector = 1 - node_value_vector
        #print(reverse_node_value_vector)

        reverse_transition_rate_vector = transition_rate(node_binary_matrix, reverse_node_value_vector)
        #print(reverse_transition_rate_vector)

        node_value_vector = change_node_value(node_value_vector,transition_rate_vector,reverse_transition_rate_vector)
        print(node_value_vector)


        pop_rate.append(np.mean(node_value_vector))
        run_times.append(i+1)
        

        plt.plot(run_times,pop_rate,"red")

        plt.pause(0.05)

    plt.show()


    return 0



if __name__ == '__main__':
    main()