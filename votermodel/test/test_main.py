import sys, os

# add path to parent directory
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from utils import *
import matplotlib.pyplot as plt


def main():

    # parameters
    # main operation
    n = False
    loop_time = False

    # relation and node value
    relation_size_mean = False # n * p
    value_size_mean = False

    # self confidence
    self_choice = False
    diagonal_mean = False

    # relation strength
    model_choice = False
    upper_range = False

    # general
    upper_limit = 10000
    
    pop_rate = []
    run_times = []

    # prompt
    (n,loop_time,relation_size_mean,value_size_mean,self_choice,diagonal_mean,model_choice,upper_range) = user_prompt(n,loop_time,relation_size_mean,value_size_mean,self_choice,diagonal_mean,model_choice,upper_range,upper_limit)
    

    # binomial param - p calculation
    bin_pro_matrix = relation_size_mean / (n - 1)    # p = mean / n
    bin_pro_vector = value_size_mean / (n)



    # initiation
    # model check
    if model_choice == "b":
        node_matrix = create_matrix(n,"binomial",bin_pro_matrix)

    elif model_choice == "f":
        node_matrix_binomial = create_matrix(n,"binomial",bin_pro_matrix)
        node_matrix_float = create_matrix(n,"uniform",upper_range)
        node_matrix = np.where(node_matrix_binomial==1,node_matrix_float,node_matrix_binomial)

    else:
        raise ValueError("\n\n\nProgram wrong. Model choice is out of expectation.\n\n\n")


    node_value_vector = create_node_value_vector(n,"binomial",bin_pro_vector)


    # self confidence check
    if self_choice == "e":
        np.fill_diagonal(node_matrix, diagonal_mean)

    elif self_choice == "u":
        np.fill_diagonal(node_matrix, np.random.uniform(high=diagonal_mean*2,size=n))

    else:
        raise ValueError("\n\n\nProgram wrong. Self choice is out of expectation.\n\n\n")


    print(node_matrix[0])

    pop_rate.append(np.mean(node_value_vector))
    run_times.append(0)


    # plot preparation
    fig, ((ax1, ax2)) = plt.subplots(2)
  
    # main loop
    for i in range(loop_time):

        print("----------  run ",i+1," ----------")

        transition_rate_vector = transition_rate(node_matrix, node_value_vector)
        #print(transition_rate_vector)

        reverse_node_value_vector = 1 - node_value_vector
        #print(reverse_node_value_vector)

        reverse_transition_rate_vector = transition_rate(node_matrix, reverse_node_value_vector)
        #print(reverse_transition_rate_vector)

        node_value_vector = change_node_value(node_value_vector,transition_rate_vector,reverse_transition_rate_vector)
        #print(node_value_vector)


        pop_rate.append(np.mean(node_value_vector))
        run_times.append(i+1)
        

        ax1.cla()
        ax1.set_title("Believer Rate in Whole Population")
        ax1.set(xlabel="Run time (t)",ylabel="Proportion of Believers (%)")
        #plot_line = plt.figure(1)
        #plt.stem(run_times,pop_rate,"blue")
        ax1.plot(run_times,pop_rate,"cornflowerblue")

        ax2.cla()
        ax2.set_title("Believer Rate States Account")
        ax2.set(xlabel="Proportion of Believers (%)",ylabel="Occur time")
        #plot_hist = plt.figure(2)
        ax2.hist(pop_rate, color="springgreen")
        
        plt.tight_layout()

        plt.pause(0.02)
    
    
    plt.show()


    return 0

def test():
    n = 500
    pop_rate = []
    run_times = []


    node_value_vector = create_node_value_vector(n)
    print(node_value_vector)
    print(np.random.binomial(1,0.1,(n,n)))
    

    #node_matrix = create_binary_matrix(n)
    #node_matrix = create_binary_matrix(n,"binomial",0.1)
    #print(node_matrix)


if __name__ == '__main__':
    main()
    #test()