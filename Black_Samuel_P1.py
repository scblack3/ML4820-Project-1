#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#For final turn in only turn in portion that you run for not the machine learning portion,
#read in file and use that k that we found to be best to find our nearest neighbor
import random
import math
#import matplotlib.pyplot as plt
#from matplotlib.ticker import MultipleLocator
#from matplotlib.ticker import AutoMinorLocator

my_data = []
def find_closest(page, compared_value1, compared_value2, k):
    nearest_neighbor = []
    nearest_species = []
    
    for line in page:
        fields = line.strip().split()
        distance = math.sqrt((float(compared_value1) - float(fields[0]))**2 + (float(compared_value2) - float(fields[1]))**2)
        
        if len(nearest_neighbor) < k:
            nearest_neighbor.append(distance)
            nearest_species.append(fields[2])
                    
        elif len(nearest_neighbor) == k:
            if max(nearest_neighbor) > distance:
                index_replace = nearest_neighbor.index(max(nearest_neighbor))
                nearest_neighbor[index_replace] = distance
                nearest_species[index_replace] = fields[2]
    
    return nearest_species

def read_file(input_file):
    #Opens file and and strips total data points from it
    input_file = open(input_file, "r")
    i = 0
    for line in input_file:
        if i == 0:
            i += 1
        elif i > 0:
            my_line = line.strip()    
            my_data.append(my_line)
    
    random.shuffle(my_data)

#Read in data, take out the 300, and randomly shuffle the data for the files
def parse_file(input_file):
    
    #Opens file and and strips total data points from it
    input_file = open(input_file, "r")
    total_number = 0
    folds = 5
    i = 0
    for line in input_file:
        if i == 0:
            total_number = line
            i += 1
        elif i > 0:
            my_line = line.strip()    
            my_data.append(my_line)
    
    random.shuffle(my_data)

    #Total number of training data
    total_training = (int(total_number) / int(folds)) * (folds - 1)

    TrainingSet = open("TrainingSet.txt", "w+")
    TestSet = open("TestSet.txt", "w+")

    #Corrects strings to remove tabs and writes them to Training and Test files
    j = 0
    for item in my_data:
        item.replace('\t', ' ')
    
        if 0 <= j <= total_training - 1:
            TrainingSet.write(str(item) + '\n')
        elif j > total_training - 1:
            TestSet.write(str(item) + '\n')
        j+=1    
    TrainingSet.seek(0)

    #Fold intervals for training data
    training_interval = total_training / folds

    #Write Validation and Training Files
    for i in range(folds):
        start = (i * training_interval) + 1
        end = start + training_interval
        j = 1
    
        Val = open("Val%s.txt" %(i+1), "w+")
        Train = open("Train%s.txt" % (i + 1), "w+")
        
        for line in TrainingSet:
            if 0 <= j < start:
                Train.write(line)
            if start <= j < end:
                Val.write(line)
            if end <= j <= total_training:
                Train.write(line)
            j = j + 1
        Val.close()
        Train.close()
        TrainingSet.seek(0)

    #Closes training, test, and input files
    TrainingSet.close()
    TestSet.close()
    input_file.close

#Compares for nearest neighbor and calculates accuracy based on k-values
def get_accuracy(folds, k_min, k_max, train_file, test_file):
    k_accuracy = {}
    #For each k value between and including k_min and k_max
    for k in range(k_min, k_max + 1,2):
        accuracy = 0
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        #For the number of folds defined
        for i in range(folds):
            #If its a training file
            if train_file == 'Train':
                Train = open(train_file + "%s.txt" %(i+1), 'r')
                Val = open(test_file + '%s.txt' %(i+1), 'r')
                
            #Else its the actual file being run
            else:
                Train = open(train_file + ".txt" ,'r')
                Val = open(test_file + '.txt', 'r')
                
            #For each line in the validation file
            for line in Val:
                
                #Set all initial values
                fields = line.strip().split()
                Actual_Val = fields[2]
                Zero_Count = 0
                One_Count = 0
                
                nearest_classification = find_closest(Train, fields[0], fields[1], k)
                Train.seek(0)
                
                #Count number of 0's and 1's
                Zero_Count = nearest_classification.count('0')
                One_Count = nearest_classification.count('1')
                d = {'0' : Zero_Count, '1' : One_Count}
                Guess = max(d, key=d.get)
            
                #TP
                if (int(Guess) == 1) & (int(Actual_Val) == 1):
                    TP +=1
                #TN
                elif (int(Guess) == 0) & (int(Actual_Val) == 0):
                    TN +=1
                #FP
                elif (int(Guess) == 1) & (int(Actual_Val) == 0):
                    FP +=1
                #FN
                elif (int(Guess) == 0) & (int(Actual_Val) == 1):
                    FN +=1 
        #Calculate accuracy       
        accuracy = (TP + TN) / (TP + TN + FP + FN)
        k_accuracy[k] = accuracy
        
    #Find the optimal k value
    optimal_k = max(k_accuracy, key=k_accuracy.get)
    
    #Return the best k value and the accuracy with it
    return optimal_k, k_accuracy[optimal_k]

#Finding the type of the point given 
def find_type(body_length, dorsal_fin, k):
    #Finds the nearest classification and returns a guess     
    nearest_classification = find_closest(my_data, body_length, dorsal_fin, k)
    Zero_Count = nearest_classification.count('0')
    One_Count = nearest_classification.count('1')
    d = {'0' : Zero_Count, '1' : One_Count}
    Guess = max(d, key=d.get)           
    return Guess


def main():
    input_file = input("Please enter the name of the training data file: ")
    parse_file(input_file)
    best_k, accuracy = get_accuracy(5, 1, 21, 'Train', 'Val')
    final_accuracy, accuracy1 = get_accuracy(1, best_k, best_k, 'TrainingSet', 'TestSet')
    #best_k = 7
    #read_file(input_file)
    print('At k = ' + str(best_k) + ' our accuracy on our test set is ' + str(accuracy1) + '%.' )
    
    body_length = 1.0
    dorsal_fin = 1.0
    while (float(body_length) != 0) | (float(dorsal_fin) != 0):
        body_length, dorsal_fin = input('Enter a body length followed by a dorsal fin length: ').split()
        if (float(body_length) == 0) & (float(dorsal_fin) == 0):
            break
        answer = find_type(body_length, dorsal_fin, best_k)
        print('Based on the data entered your fish spieces is TigerFish' + str(answer))
        

if __name__ == "__main__":
    main()