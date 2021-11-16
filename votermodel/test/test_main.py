import sys, os

# add path to parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils import *
import matplotlib.pyplot as plt



def main():

    # parameters
    n = False
    loop_time = False
    relation_size_mean = False # n * p
    value_size_mean = False
    self_deter_range = False
    upper_range = False
    upper_limit = 10000

    (n,loop_time,relation_size_mean,value_size_mean,upper_range,upper_limit) = user_prompt(n,loop_time,relation_size_mean,value_size_mean,upper_range,upper_limit)
    
    # binomial param - p calculation
    bin_pro_matrix = relation_size_mean / (n - 1)    # p = mean / n
    bin_pro_vector = value_size_mean / (n)


    pop_rate = []
    run_times = []


    node_value_vector = create_node_value_vector(n,"binomial",bin_pro_vector)
    #print(np.mean(node_value_vector))

    #node_binary_matrix = create_binary_matrix(n)
    node_binary_matrix = create_binary_matrix(n,"binomial",bin_pro_matrix)

    print(node_binary_matrix)
    #print(node_binary_matrix[1])

    pop_rate.append(np.mean(node_value_vector))
    run_times.append(0)


    for i in range(loop_time):

        print("----------  run ",i+1," ----------")

        transition_rate_vector = transition_rate(node_binary_matrix, node_value_vector)
        #print(transition_rate_vector)

        reverse_node_value_vector = 1 - node_value_vector
        #print(reverse_node_value_vector)

        reverse_transition_rate_vector = transition_rate(node_binary_matrix, reverse_node_value_vector)
        #print(reverse_transition_rate_vector)

        node_value_vector = change_node_value(node_value_vector,transition_rate_vector,reverse_transition_rate_vector)
        #print(node_value_vector)


        pop_rate.append(np.mean(node_value_vector))
        run_times.append(i+1)
        
        
        
        #plt.pause(0.05)
    
    plot_line = plt.figure(1)
    #plt.stem(run_times,pop_rate,"blue")
    plt.plot(run_times,pop_rate,"red")
    plt.title("Believer rate in whole population")

    plot_hist = plt.figure(2)
    plt.hist(pop_rate, color="blue")

    plt.show()


    return 0

def test():
    n = 500
    pop_rate = []
    run_times = []


    node_value_vector = create_node_value_vector(n)
    print(node_value_vector)
    print(np.random.binomial(1,0.1,(n,n)))
    

    #node_binary_matrix = create_binary_matrix(n)
    #node_binary_matrix = create_binary_matrix(n,"binomial",0.1)
    #print(node_binary_matrix)


if __name__ == '__main__':
    main()
    #test()