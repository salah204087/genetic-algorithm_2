import random
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt


def fitness1_standard(Chromosome,len_chromosome):
    fit1=[]
    summation=0.0
    for i in range (len(Chromosome)):
        for j in range (len_chromosome-2):
            summation+=(Chromosome[i][j]*((2)**(len_chromosome-j-1)))/2**len_chromosome
        fit1.append(-2+summation*(2-(-2)))
        summation=0.0
    return fit1

def fitness2_standard(Chromosome,len_chromosome):
    fit2=[]
    summation=0.0
    m=2
    for i in range (len(Chromosome)):
        for j in range (2,4):
            summation+=(Chromosome[i][j]*((2)**(len_chromosome-m-1)))/2**len_chromosome
            m+=1
        fit2.append(-2+summation*(2-(-2)))
        summation=0.0
        m=2
    return fit2
def fitness1_gray(Chromosome,len_chromosome):
    fit1=[]
    summation=0.0
    summ=0.0
    for i in range (len(Chromosome)):
        for j in range (len_chromosome-2):
            for k in range (j+1):
                summ+=Chromosome[i][j]%2
                if (j==1):
                    break
            summation+=(summ*((2)**(len_chromosome-j-1)))/2**len_chromosome
            summ=0.0
        fit1.append(-2+summation*(2-(-2)))
        summation=0.0
    return fit1
#print(fitness1_gray(Chromosome,Chromosome_length))

def fitness2_gray(Chromosome,len_chromosome):
    fit2=[]
    summation=0.0
    summ=0.0
    m=2
    for i in range (len(Chromosome)):
        for j in range (2,4):
            for k in range (j-1):
                summ+=Chromosome[i][j]%2
                if (j==3):
                    break
            summation+=(summ*((2)**(len_chromosome-j-1)))/2**len_chromosome
            m+=1
            summ=0.0
        fit2.append(-2+summation*(2-(-2)))
        summation=0.0
        m=2
    return fit2
#print(fitness2_gray(Chromosome,Chromosome_length))
def fitness_function(x1,x2):
    x=[]
    for i in range(len(Chromosome)):
        x.append(8-((x1[i]+0.0317)**2)+(x2[i]**2))
    return x
#print(fitness_function(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length)))
def fitness_function_constrain(x1,x2):
    x=[]
    for i in range(len(Chromosome)):
        x.append((8-((x1[i]+0.0317)**2)+(x2[i]**2))-abs(x1[i]+x2[i]-1))
    return x
#print(fitness_function_constrain(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length)))
def rank(fitness_func):
    array = np.array(fitness_func)
    order = array.argsort()
    ranks = order.argsort()
    for i in range (len(fitness_func)):
        ranks[i]=ranks[i]+1
    return ranks
#print(rank(fitness_function(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))

def rank_fit(fitness_rank):
    rankfit=[]
    np.sort(fitness_rank)
    for i in range (len(fitness_rank)):
        SP=random.uniform(1, 2)
        rankfit.append((2-SP)+(2*(SP-1))*((fitness_rank[i]-1)/(len(fitness_rank)-1)))
    return rankfit
#print (rank_fit(rank(fitness_function(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length)))))
        
    
def Selection(relative):
    relative_fitness=[]
    for i in range (len(relative)):
        relative_fitness.append(relative[i]/sum(relative))
    return relative_fitness

def cumulative(prob,relative):
    total_sum=0.0
    cumulative_probabilities=[]
    for i in range (len(prob)):
        total_sum+=prob[i]
        cumulative_probabilities.append(total_sum)
    return cumulative_probabilities

#print(cumulative(Selection(rank_fit(rank(fitness_function(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))), rank_fit(rank(fitness_function(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))))

def one_point_crossover(cum,Chromosome,pcross,len_chromosome):
    gene=[]
    for i in range(int(.5*len(Chromosome))):
        parent1_cum=0.0
        parent2_cum=0.0
        index_parent1=0
        index_parent2=0
        child1=[]
        child2=[]     
        cut=0.0
        for i in range (len(cum)):
            if random.random()<cum[i]:
                parent1_cum=cum[i-1]
                index_parent1=cum.index(parent1_cum)
                break
            else:
                continue
        for i in range (len(cum)):
            if random.random()<cum[i]:
                parent2_cum=cum[i-1]
                index_parent2=cum.index(parent2_cum)
                break
            else:
                continue
        cut=random.randint(0, len_chromosome)
        parent1=Chromosome[index_parent1]
        parent2=Chromosome[index_parent2]
        if random.random() < pcross:
            for i in range (int(cut)):
                child1.append(parent1[i])
            for i in range (int(cut),len_chromosome):
                child1.append(parent2[i])
            for i in range (int(cut)):
                child2.append(parent2[i])
            for i in range (int(cut),len_chromosome):
                child2.append(parent1[i])
            gene.append(child1)
            gene.append(child2)
        else:
            gene.append(parent1)
            gene.append(parent2)
    return gene

def mutation(gen,pmut,len_chromosome):
    nextgene=[]
    for i in range(len(gen)):
        genen=[]
        for j in range(len_chromosome):
            if random.random() < pmut:
                genen.append(int(not gen[i][j]))
            else:
                genen.append(gen[i][j])
        nextgene.append(genen)
    return nextgene


def generation(population,number_of_generation,len_chromosome,pcross,pmut,type_of_decoding):
    highest_fitness=[]
    average_fitness=[]
    all_population=[]
    gen=Chromosome
    decoding=[]
    if (type_of_decoding==1):
        decoding=rank_fit(rank(fitness_function(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))
    elif(type_of_decoding==2):
        decoding=rank_fit(rank(fitness_function_constrain(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))
    elif(type_of_decoding==3):
        decoding=rank_fit(rank(fitness_function(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))
    elif(type_of_decoding==4):
        decoding=rank_fit(rank(fitness_function_constrain(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))
    for i in range (int(number_of_generation/population)):
       all_population.append(gen)
       highest_fitness.append(max(decoding))
       average_fitness.append(mean(decoding))
       gen=mutation(one_point_crossover(cumulative(Selection(decoding), decoding),gen,pcross,len_chromosome),pmut,len_chromosome)
       if (type_of_decoding==1):
           decoding=rank_fit(rank(fitness_function(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))
       elif(type_of_decoding==2):
           decoding=rank_fit(rank(fitness_function_constrain(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))
       elif(type_of_decoding==3):
           decoding=rank_fit(rank(fitness_function(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))
       elif(type_of_decoding==4):
           decoding=rank_fit(rank(fitness_function_constrain(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))
    print("The final population:")
    print(all_population[int(number_of_generation/population)-1])
    for i in range(int(number_of_generation/population)):
        print("The highest fitness in "+ str(i+1) +" generation:"+str(highest_fitness[i]))
        print("The average fitness in "+ str(i+1) +" generation:"+str(average_fitness[i]))
    print()
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    x=np.array(highest_fitness)
    y=np.array(average_fitness)
    plt.plot(x,color="blue")
    plt.title("fitness acurracy without elitism")
    plt.plot(y, color="red")
    plt.show()

#generation(20,100 ,Chromosome_length, 0.6, 0.05,1)

def elitism(size_of_elitism,population,number_of_generation,len_chromosome,pcross,pmut,type_of_decoding):
    highest_fitness=[]
    average_fitness=[]
    all_population=[]
    gen=Chromosome
    copy_of_gene=[]
    decoding=[]
    if (type_of_decoding==1):
        decoding=rank_fit(rank(fitness_function(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))
    elif(type_of_decoding==2):
        decoding=rank_fit(rank(fitness_function_constrain(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))
    elif(type_of_decoding==3):
        decoding=rank_fit(rank(fitness_function(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))
    elif(type_of_decoding==4):
        decoding=rank_fit(rank(fitness_function_constrain(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))
    for i in range (int(number_of_generation/population)):     
        all_population.append(gen)
        highest_fitness.append(max(decoding))
        average_fitness.append(mean(decoding))
        gen=mutation(one_point_crossover(cumulative(Selection(decoding), decoding),gen,pcross,len_chromosome),pmut,len_chromosome)
        copy_of_gene=decoding.copy()
        x=rank_fit(copy_of_gene)
        if (type_of_decoding==1):
            decoding=rank_fit(rank(fitness_function(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))
        elif(type_of_decoding==2):
            decoding=rank_fit(rank(fitness_function_constrain(fitness1_standard(Chromosome, Chromosome_length),fitness2_standard(Chromosome, Chromosome_length))))
        elif(type_of_decoding==3):
            decoding=rank_fit(rank(fitness_function(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))
        elif(type_of_decoding==4):
            decoding=rank_fit(rank(fitness_function_constrain(fitness1_gray(Chromosome, Chromosome_length),fitness2_gray(Chromosome, Chromosome_length))))
        for i in range(size_of_elitism):
            index=x.index(max(x))
            x[index]=0
            gen[i]=mutation(one_point_crossover(cumulative(Selection(decoding), decoding),gen,pcross,len_chromosome),pmut,len_chromosome)[index]
    print("The final population with elitism:")
    print(all_population[int(number_of_generation/population)-1])
    for i in range(int(number_of_generation/population)):
        print("The highest fitness in "+ str(i+1) +" generation with elitism:"+str(highest_fitness[i]))
        print("The average fitness in "+ str(i+1) +" generation with elitism:"+str(average_fitness[i]))
    print()
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    x=np.array(highest_fitness)
    y=np.array(average_fitness)
    plt.plot(x,color="blue")
    plt.title("fitness acurracy with elitism")
    plt.plot(y, color="red")
    plt.show()
#elitism(2,20,100 ,Chromosome_length, 0.6, 0.05,1)

while (True):
    Chromosome_length=int(input("Enter the number of bits to encode the variables:"))
    if (Chromosome_length<=3):
        print("please enter valid bit (>3)")
        print()
    else:
        break
Chromosome=np.random.randint(2, size = (100,Chromosome_length))

while(True):
    print("1-Standard decoding by  optimization function")
    print("2-Standard decoding by  optimization function and constraint")
    print("3-gray decoding by  optimization function")
    print("4-gray decoding by  optimization function and constraint")
    print("5-Exit")
    choice=int(input("Enter your choice:"))
    if (choice==1):
        generation(20,100 ,Chromosome_length, 0.6, 0.05,choice)
        elitism(2,20,100 ,Chromosome_length, 0.6, 0.05,choice)
    elif(choice==2):
        generation(20,100 ,Chromosome_length, 0.6, 0.05,choice)
        elitism(2,20,100 ,Chromosome_length, 0.6, 0.05,choice)
    elif(choice==3):
        generation(20,100 ,Chromosome_length, 0.6, 0.05,choice)
        elitism(2,20,100 ,Chromosome_length, 0.6, 0.05,choice)
    elif(choice==4):
        generation(20,100 ,Chromosome_length, 0.6, 0.05,choice)
        elitism(2,20,100 ,Chromosome_length, 0.6, 0.05,choice)
    elif(choice==5):
        break
    else:
        print("please enter valid choice:")
        continue
        
