#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:50:50 2019

@author: connorblack
"""
import random
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import AutoMinorLocator

#this is my python code
input_file = open("FF14.txt", "r")
my_data = []
total_number = 0

#Read in data, take out the 300, and randomly shuffle the data for the files
i = 0
for line in input_file:
    if i == 0:
        total_number = line
        i += 1
    elif i > 0:
        my_line = line.strip()    
        my_data.append(my_line)
    
random.shuffle(my_data)


TrainingSet = open("TrainingSet.txt", "w+")
TestSet = open("TestSet.txt", "w+")

j = 0
for item in my_data:
    item.replace('\t', ' ')
    
    if 0 <= j <= 239:
        TrainingSet.write(str(item) + '\n')
    elif j > 239:
        TestSet.write(str(item) + '\n')
    j+=1
    
#Writes all Train and Test Files
TrainingSet.seek(0)

#Write Validation and Training Files
for i in range(5):
    start = (i * 48) + 1
    end = start + 48
    j = 1
    
    Val = open("Val%s.txt" %(i+1), "w+")
    Train = open("Train%s.txt" % (i + 1), "w+")
        
    for line in TrainingSet:
        if 0 <= j < start:
            Train.write(line)
        if start <= j < end:
            Val.write(line)
        if end <= j <= 240:
            Train.write(line)
        j = j + 1
    Val.close()
    Train.close()
    TrainingSet.seek(0)

#Finding numbers for K
#for k in range(1,22,2):
#Mapping the figures for the test
# =============================================================================
# for i in range(5):
#     fig = plt.figure()
#     ax = fig.add_subplot(1,1,1)
# 
#     #Sets stuff for axis
#     ax.xaxis.set_major_locator(MultipleLocator(5))
#     ax.yaxis.set_major_locator(MultipleLocator(5))
#     ax.xaxis.set_minor_locator(AutoMinorLocator())
#     ax.yaxis.set_minor_locator(AutoMinorLocator())
# 
#     Train1 = open("Train%s.txt" %(i+1), "r")
#     for line in Train1:
#         fields = line.strip().split()
#         if int(fields[2]) == 0:
#             ax.scatter(float(fields[0]), float(fields[1]), color = 'blue', marker = '^')
#         elif int(fields[2]) == 1:
#             ax.scatter(float(fields[0]), float(fields[1]), color = 'orange' , marker = '^')
#     Val1 = open("Val%s.txt" %( i + 1 ), "r")
#     for line in Val1:
#         fields = line.strip().split()
#         ax.scatter(float(fields[0]), float(fields[1]), color = 'green', marker = '*')
# 
# 
#     plt.show()   
# 
#     Train1.close
#     Val1.close
# =============================================================================

#Attempt 1 At comparing fo rnearest
k_accuracy = {}
for k in range(1,22,2):
    accuracy = 0
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(5):
        Train = open("Train%s.txt" %(i+1), 'r')
        Val = open('Val%s.txt' %(i+1), 'r')

        for line in Val:
            
            nearest_neighbor = []
            nearest_classification = []
            fields = line.strip().split()
            Actual_Val = fields[2]
            Zero_Count = 0
            One_Count = 0
            for each_line in Train:
                
                fields2 = each_line.strip().split()
                distance = math.sqrt((float(fields[0]) - float(fields2[0]))**2 + (float(fields[1]) - float(fields2[1]))**2)
                
                if len(nearest_neighbor) < k:
                    nearest_neighbor.append(distance)
                    nearest_classification.append(fields2[2])
                    
                elif len(nearest_neighbor) == k:
                    if max(nearest_neighbor) > distance:
                        index_replace = nearest_neighbor.index(max(nearest_neighbor))
                        nearest_neighbor[index_replace] = distance
                        nearest_classification[index_replace] = fields2[2]
            Train.seek(0)
            
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
    #print('TP: ' + str(TP) + ' TN: ' + str(TN) + ' FP: ' + str(FP) + ' FN: ' + str(FN))
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    #print('Accuracy: ' + str(accuracy))
    k_accuracy[k] = accuracy

print(k_accuracy)
TrainingSet.close()
TestSet.close()

input_file.close