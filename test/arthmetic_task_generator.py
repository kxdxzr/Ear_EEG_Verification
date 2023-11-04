# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 19:26:31 2023
@author: leyu3109
"""
import random

def generate_30_list():
    result_ls = 10 * ["<"] + 10 * ["="] + 10 * [">"]
    random.shuffle(result_ls)
    return result_ls

def generare_single_cal(format_ls, compare_result):
    int_1 = random.randint(10 ** (format_ls[0]-1),10 ** (format_ls[0]) - 1)
    int_2 = random.randint(10 ** (format_ls[1]-1),10 ** (format_ls[1]) - 1)
    
    result = int_1 + int_2
    if compare_result == "<":
        compare = random.randint(int(result * 0.5) ,result - 1)
    elif compare_result == "=":
        compare = result
    elif compare_result == ">":
        compare = random.randint(result + 1, int(result * 1.5))
    else:
        raise ValueError("Compare_result should be <, = , >")
    return [int_1, int_2, compare]

def transfer_function(level):
    target = level + 1
    if target % 2 == 0:
        return [int(target/2), int(target/2)]
    else:
        return [int((target-1)/2), int((target+1)/2)]

def arthmetic_task_generator(level):
    result_ls = generate_30_list() + generate_30_list() + generate_30_list()
    
    generated_ls = []
    
    for i in range(len(result_ls)):
        format_ls = transfer_function(level)
        generated_ls.append(generare_single_cal(format_ls, result_ls[i]))
        
    return generated_ls, result_ls

if __name__ == "__main__":
    generated_ls, result_ls = arthmetic_task_generator(1)
    print(generated_ls)
    print(result_ls)
    print(len(generated_ls))