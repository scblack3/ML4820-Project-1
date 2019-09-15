#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Samuel Connor Black
# September 15, 2019
# ML4820 Project 1
# This program takes in an input file given by the user, the program will then
# prompt the user for a dorsal fin length and body length value and find its 
# probable species based on its k nearest neighbors.
# =============================================================================
import random
import math

#Creates a list to hold all data read in from the file
my_data = []

#This function finds the k nearest neighbors for a given value 
def find_closest(data, compared_value1, compared_value2, k):
    #Creates list for nearest_neighbor and its species
    nearest_neighbor = []
    nearest_species = []
    
    #Iterates through our data
    for line in data:
        fields = line.strip().split()
        #Finds the euclidean distance
        distance = math.sqrt((float(compared_value1) - float(fields[0]))**2 + 
                             (float(compared_value2) - float(fields[1]))**2)
        #If we havent reached 7 values yet, just add it to the nearest list
        if len(nearest_neighbor) < k:
            nearest_neighbor.append(distance)
            nearest_species.append(fields[2])
        #Else if we already have seven values, find the largest distance and
        #replace if if our new distance is smaller
        elif len(nearest_neighbor) == k:
            if max(nearest_neighbor) > distance:
                index_replace = nearest_neighbor.index(max(nearest_neighbor))
                nearest_neighbor[index_replace] = distance
                nearest_species[index_replace] = fields[2]
    
    #Return the list of our species that are the closest
    return nearest_species

#This function just reads in our input file and puts it into a list for
#manipulation
def read_file(input_file):
    #Opens file and and strips total data points from it
    input_file = open(input_file, "r")
    i = 0
    #Ignore the first line (just the number of points), then keep reading
    for line in input_file:
        if i == 0:
            i += 1
        elif i > 0:
            my_line = line.strip()    
            my_data.append(my_line)
    
    random.shuffle(my_data)

#Finding the type of the point given 
def find_type(body_length, dorsal_fin, k):
    #Finds the nearest classification and returns a guess     
    nearest_classification = find_closest(my_data, body_length, dorsal_fin, k)
    #Sees if there are more 1's or 0's in our list
    Zero_Count = nearest_classification.count('0')
    One_Count = nearest_classification.count('1')
    d = {'0' : Zero_Count, '1' : One_Count}
    #Returns a 1 or 0 to denote species
    Guess = max(d, key=d.get)           
    return Guess


def main():
    #Request an input file from user
    input_file = input("Please enter the name of the training data file: ")
    #Best_k set to 7 based on our machine learning algorithms output
    best_k = 7
    read_file(input_file)
    
    body_length = 1.0
    dorsal_fin = 1.0
    #While the user does not enter two 0's for values, keep prompting for more
    while (float(body_length) != 0) | (float(dorsal_fin) != 0):
        #Try to get two values, if not catch the exception
        try:
            body_length, dorsal_fin = input('Enter a body length followed by a dorsal fin length: ').split()
            answer = find_type(body_length, dorsal_fin, best_k)
            print('Based on the data entered your fish spieces is TigerFish' + str(answer))
        except:
            print('Please enter two values')
        #If two zeros are entered break from the program and quit
        if (float(body_length) == 0) & (float(dorsal_fin) == 0):
            break
        

if __name__ == "__main__":
    main()