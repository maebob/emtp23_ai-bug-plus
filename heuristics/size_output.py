import csv

# rules of bugsplus:
# if (up is None and down is None):
#             return 0, 0
# elif (up is None and down is not None):
#             return -1, 1
# elif (up is not None and down is None):
#             return 1, 1
# elif (up is not None and down is not None):
#             if up + down == 0:
#                         return 0, 0
#         else:
#                     return up + down, 1




def produce_output(input)-> list:
    output = []
    for outer in input:
        for inner in input:
            if outer == None:
                if inner == None:
                    result = '+0'
                else:
                    result = '-1'
            else:
                if inner == None:
                    result = '+1'
                else:
                    result = outer + inner
            output.append(result) if result not in output else None
    return output


def output_after_n_bugs(n) -> list:
    input = [None, 'x', 'y']
    for i in range(n):
        output = produce_output(input)
        for element in output: # add all (new) elements from output to input
            if element not in input:
                input.append(element)
    #nice_output = mathematical_output(output)
    #write_to_file(nice_output, f'output{i+1}.csv')
    #return mathematical_output(output)
    return output

def size_of_output(list)-> int:
    return len(list)

def mathematical_output(last_output)-> list:
    mathematical = [None]
    for string in last_output:
        if string == None:
            continue
        else:
            variable_part = []
            number_part = 0
            #loop through string:
            for i in range(len(string)):
                if string[i] == '+' or string[i] == '-':
                    #number_part.append(int(string[i:i+2])) # add number to number_part and change type to int
                    number_part += int(string[i:i+2])
                elif string[i].isnumeric(): # ignore numbers, they have been taken care of by +/-
                    continue
                else:
                    variable_part.append(string[i])
            number_part = numbers_to_strings(number_part) # rewrite numerical part to string:
            variable_part = count_variable(variable_part) # rewrite variables into multiplications
            string = variable_part+number_part # join variable and number part
        mathematical.append(string) if string not in mathematical else None # add string to sorted_output if it is not already in there
    return mathematical

    return None

def write_to_file(output, filename)-> None:
    with open(filename,'w') as out:

        csv_out=csv.writer(out, delimiter='\n')
        csv_out.writerow(output)


def sort_string(variables)-> str: # sort string alphabetically
    return ''.join(sorted(variables))


def numbers_to_strings(number)-> str:
    if number == 0:
        return ''
    if number > 0:
        return '+' + str(number)
    else:
        return str(number)

def count_variable(string)-> str: #takes in a string and counts the number of variables
    count_x = string.count('x')
    count_y = string.count('y')
    return str(str(count_x) +'x+' + str(count_y) + 'y')




def mathemize(output)-> list:
    """
    takes in string from output and puts it in mathematically correct format
    ignores None
    everything else:
    1. split string into variable part and number part by looking for +/-
    2. sort variable part alphabetically
    3. calculate value of numerical part
    4. joins the two parts as string
    """
    # takes in string from output and puts it in mathematically correct format
    # first:
    sorted_output = [None]
    # loop through all strings in list
    for string in output:
        if string == None:
            continue
        else:
            variable_part = []
            number_part = 0
            #loop through string:
            for i in range(len(string)):
                if string[i] == '+' or string[i] == '-':
                    #number_part.append(int(string[i:i+2])) # add number to number_part and change type to int
                    number_part += int(string[i:i+2])
                elif string[i].isnumeric(): # ignore numbers, they have been taken care of by +/-
                    continue
                else:
                    variable_part.append(string[i])
            number_part = numbers_to_strings(number_part) # rewrite numerical part to string:
            variable_part = sort_string(variable_part) # sort variables alphabetically
            string = variable_part+number_part # join variable and number part
        sorted_output.append(string) if string not in sorted_output else None # add string to sorted_output if it is not already in there
    return sorted_output




def main():
    output_after_n_bugs(4)



if __name__ == "__main__":
    main()

