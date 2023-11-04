# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:29:22 2023

@author: leyu3109
"""
import random

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def inserting(ls, ls_res, interval):
    i = 0
    
    rand_range = [[1,0],[3,2]]
    
    while len(ls) < 48:
        insert_number = random.randint(rand_range[0][interval - 1],rand_range[1][interval - 1])
        j = 0
        while j < insert_number:
            current_choice = random.choice(letters)
            if i < len(ls):
                while current_choice == ls[i-1]:
                    current_choice = random.choice(letters)
            ls.insert(i, random.choice(current_choice))
            ls_res.insert(i, 0)
            i += 1
            if len(ls) == 48:
                return ls, ls_res
            j += 1
        i += interval
    return ls, ls_res

def check_repeat(ls):
    current_choice = random.choice(letters)
    if len(ls) < 2:
        return current_choice
    while current_choice == ls[-2]:
        current_choice = random.choice(letters)
    return current_choice

def N_back_task_generator(back_num):
    
    if back_num == 0:
        ls = 16 * ["X"]
        ls_res = 16 * [1]
        inserting(ls, ls_res, 1)
    elif back_num == 1:
        ls = []
        ls_res = []
        #ls, ls_res = inserting(ls, ls_res, back_num + 1)
        for i in range(0,16):
            target = random.choice(letters)
            ls.append(target)
            ls_res.append(0)
            ls.append(target)
            ls_res.append(1)
        ls, ls_res = inserting(ls, ls_res, back_num + 1)
    elif back_num == 2:
        patern_1 = random.randint(0,4) # AXAXA
        patern_2 = random.randint(0,4) # ABAB
        patern_3 = 16 - (patern_1 + patern_2)*2 #AXA
        
        gap_number = 48 - patern_1 * 5 - patern_2 * 4 - patern_3 * 3
        
        patern_ls = [0] * gap_number + [1] * patern_1 + [2] * patern_2 + [3] * patern_3
        random.shuffle(patern_ls)
        
        ls = []
        ls_res = []
        
        for i in patern_ls:
            if i == 0:
                current_choice = check_repeat(ls)
                ls.append(current_choice)
                ls_res.append(0)
            elif i == 1:
                target_letter = check_repeat(ls)
                ls.append(target_letter)
                ls_res.append(0)
                gap = check_repeat(ls)
                ls.append(gap)
                ls_res.append(0)
                ls.append(target_letter)
                ls_res.append(1)
                gap = check_repeat(ls)
                ls.append(gap)
                ls_res.append(0)
                ls.append(target_letter)
                ls_res.append(1)
            elif i == 2:
                target_letter_1 = check_repeat(ls)
                ls.append(target_letter_1)
                ls_res.append(0)
                target_letter_2 = check_repeat(ls)
                ls.append(target_letter_2)
                ls_res.append(0)
                ls.append(target_letter_1)
                ls_res.append(1)
                ls.append(target_letter_2)
                ls_res.append(1)
            elif i == 3:
                target_letter = check_repeat(ls)
                ls.append(target_letter)
                ls_res.append(0)
                gap = check_repeat(ls)
                ls.append(gap)
                ls_res.append(0)
                ls.append(target_letter)
                ls_res.append(1)
    else:
        raise ValueError("back_num should be 1, 2, or 3")
    
    return ls, ls_res

if __name__ == "__main__":
    alpha_list, beta_list = N_back_task_generator(2)
    print(alpha_list)
    print(beta_list)
    print(len(alpha_list))