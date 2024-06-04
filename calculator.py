#Imports
import re
import operator


# Operators and their functions
operator_dict = {
            "+" : operator.add,
            "add" : operator.add,

            "-" : operator.sub, 
            "sub" : operator.sub,

            "*" : operator.mul, 
            "mul" : operator.mul,

            "/" : operator.truediv, 
            "div" : operator.truediv,

            "^" : operator.pow, 
            "pow" : operator.pow,

            "%" : operator.mod, 
            "mod" : operator.mod
    }   
operator_keys = [key for key in operator_dict.keys()]


# Calculator History
ans_history = 0
calc_history = {} 
answer = None
ans_key = None
def print_calc_history():

    print("History: ")
    for i in range(len(calc_history)):

        print (f"   Calc No.{i+1}| {calc_history[i][0]} = {calc_history[i][1]}")

    print("\n To redo a calculation in history enter h and the calc number (example: h1)")

def redo_calc(history_input):

    def extract_number(input_string):
        number = re.search(r'\d+', input_string)
        if number:
            return int(number.group())
        else:
            return None
        
    numb = extract_number(history_input) - 1

    return numb



#Calculating function
def calc(op, n1, n2=None):
    # Checking
    def checking():

        valid_op = False
        valid_number = True
        valid_function = False

        # Checking if operator is valid
        if op in operator_dict.keys():

            valid_op = True

            # Checking if numbers is int
            n1_check = isinstance(n1, (int, float))
            if n1_check == False:
                valid_number = False
                raise Exception(f'Invalid number "{n1}"')

            if n2 is not None:
                n2_check = isinstance(n2, (int, float))
                if n2_check == False:
                    valid_number = False
                    raise Exception(f'Invalid number "{n2}"')

                # Checking if division by zero
                if (op in ["/", "div", "%", "mod"]) and n2 == 0:
                    raise Exception(f'Division by zero')

        elif op not in operator_dict.keys():
            valid_op = False
            raise Exception(f'Invalid operator "{op}"')

        if valid_op == True and valid_number == True:

            valid_function = True

        return valid_function

    check_valid = checking()

    # Calculations
    if check_valid == True:

        # Calculate the 2 given numbers
        if n2 != None:

            result = operator_dict[op](n1, n2)

            return result

        elif n2 == None:

            if op in ["+", "add"]:

                return n1

            elif op in ["-", "sub"]:

                return n1*(-1)

#Eval Function
def eval(op_num_lst):

    #Check if input is valid
    if not isinstance(op_num_lst, list):
        raise Exception(f'Failed to evaluate "{op_num_lst}"')

    elif len(op_num_lst) not in [2, 3]:
        raise Exception(f'Failed to evaluate "{op_num_lst}"')


    #Solve input
    if len(op_num_lst) == 2:
        if isinstance(op_num_lst[1], list):
            op_num_lst[1] = eval(op_num_lst[1])
        return calc(op_num_lst[0], op_num_lst[1])

    elif len(op_num_lst) == 3:
        if isinstance(op_num_lst[1], list):
            op_num_lst[1] = eval(op_num_lst[1])
        if isinstance(op_num_lst[2], list):
            op_num_lst[2] = eval(op_num_lst[2])
        return calc(op_num_lst[0], op_num_lst[1], op_num_lst[2])

#Convert [n1, op, n2] -> [op, n1, n2] Function
def struct(input_list):
    
    if isinstance(input_list, (list)) and (len(input_list) == 1) and (input_list[0] in operator_dict.keys()):
        raise Exception(f'Failed to structure "{input_list}"')

    # Check if input_list is a list
    elif not isinstance(input_list, (list)):
        raise Exception(f'Failed to structure "{input_list}"')

    # If input_list just like ["+", 2]
    elif len(input_list) <= 2 and input_list[0] in ["add", "+", "-", "sub"]:
        return input_list
    elif len(input_list) <= 2 and input_list[1] in ["add", "+", "-", "sub"]:
        new_list = [input_list[1], input_list[0]]
        return new_list
    
    # If input_list just like ["test+", 2]
    elif len(input_list) <= 2 and isinstance(input_list[1], str):
        new_list = [input_list[1], input_list[0]]
        return new_list
    elif len(input_list) <= 2 and isinstance(input_list[0], str):
        return input_list

    # If input_list is something like [1, "+", 3, "-"]
    elif not isinstance(input_list[-1], list) and input_list[-1] not in operator_dict.keys() and all(item in operator_dict.keys() or isinstance(item, (int, float, complex)) for item in input_list[1::2]) and not isinstance(input_list[-1], (int, float, complex)):
        raise Exception(f'Failed to structure "{input_list}"')

    else:
        # Power
        for i in range(len(input_list)):
            if input_list[i] in ["pow", "^"]:
                sublist = [input_list[i], input_list[i-1], input_list[i+1]]
                input_list[i] = sublist
                new_list = [value for index, value in enumerate(input_list) if index not in [i-1, i+1]]
                if len(new_list) > 3:
                    return struct(new_list)
                if len(new_list) == 3:
                    new_list[0], new_list[1] = new_list[1], new_list[0]
                    return new_list
            if len(input_list) == 3:
                input_list[0], input_list[1] = input_list[1], input_list[0]
                return input_list

        # Mul, Div, and Mod
        for i in range(len(input_list)):
            if input_list[i] in ["*", "mul", "/", "div", "%", "mod"]:
                sublist = [input_list[i], input_list[i-1], input_list[i+1]]
                input_list[i] = sublist
                new_list = [value for index, value in enumerate(input_list) if index not in [i-1, i+1]]
                if len(new_list) > 3:
                    return struct(new_list)
                if len(new_list) == 3:
                    new_list[0], new_list[1] = new_list[1], new_list[0]
                    return new_list
            if len(input_list) == 3:
                input_list[0], input_list[1] = input_list[1], input_list[0]
                return input_list

        # Add and Sub
        for i in range(len(input_list)):
            if input_list[i] in ["add", "+", "-", "sub"]:
                sublist = [input_list[i], input_list[i-1], input_list[i+1]]
                input_list[i] = sublist
                new_list = [value for index, value in enumerate(input_list) if index not in [i-1, i+1]]
                if len(new_list) > 3:
                    return struct(new_list)
                if len(new_list) == 3:
                    new_list[0], new_list[1] = new_list[1], new_list[0]
                    return new_list
            if len(input_list) == 3:
                input_list[0], input_list[1] = input_list[1], input_list[0]
                return input_list

        # Random Operators ("??", "t", "?", "test", "mol", etc.)
        for i in range(len(input_list)):
            if input_list[i] not in operator_dict.keys() and not isinstance(input_list[i], (float, int)):
                sublist = [input_list[i], input_list[i-1], input_list[i+1]]
                input_list[i] = sublist
                new_list = [value for index, value in enumerate(input_list) if index not in [i-1, i+1]]
                if len(new_list) > 3:
                    return struct(new_list)
                if len(new_list) == 3:
                    new_list[0], new_list[1] = new_list[1], new_list[0]
                    return new_list
            if len(input_list) == 3:
                input_list[0], input_list[1] = input_list[1], input_list[0]
                return input_list
            

def get_next(string, input_number):
    if input_number < 0 or input_number >= len(string):
        return "End of string"
    
    char = string[input_number]
    if char.isdigit() or char == '.':
        match = re.search(r'[\d.]+', string[input_number:])
        num_str = match.group()
        if '.' in num_str:
            return float(num_str)
        else:
            return int(num_str)
    elif char.isalpha():
        match = re.search(r'[a-zA-Z]+', string[input_number:])
        return match.group()
    elif char in operator_dict.keys():
        return char
    else:
        return char

# Parsing
def parse(string_to_parse):

    global calc_history
    global ans_history
    global answer
    global ans_key

    string_to_parse = string_to_parse.replace(" ", '')
    if len(calc_history) >= 1 and (answer is not None):
        string_to_parse = string_to_parse.replace("ans", str(answer))
    parsed_list = []
    input_number = 0

    while input_number < len(string_to_parse):
        if string_to_parse[input_number] == '(':
            # Find the matching closing parenthesis
            open_count = 1
            close_count = 0
            index = input_number + 1
            while open_count != close_count:
                if string_to_parse[index] == '(':
                    open_count += 1
                elif string_to_parse[index] == ')':
                    close_count += 1
                index += 1
            # Recursively parse the contents of the parentheses and append to the parsed_list
            parsed_list.append(parse(string_to_parse[input_number + 1:index - 1]))
            input_number = index
        else:
            token = get_next(string_to_parse, input_number)
            parsed_list.append(token)
            input_number += len(str(token))

    def combine_strings_in_list(input_list):
        index = 0
        while index < len(input_list) - 1:
            if isinstance(input_list[index], str) and isinstance(input_list[index + 1], str):
                input_list[index] = input_list[index] + input_list[index + 1]
                del input_list[index + 1]
                return combine_strings_in_list(input_list)
            else:
                index += 1
        return input_list

    parse_res = combine_strings_in_list(parsed_list)
    return struct(parse_res)

def pre_parse(string_to_parse):

    open_parenthesis_count = string_to_parse.count("(")
    closed_parenthesis_count = string_to_parse.count(")")

    if open_parenthesis_count == closed_parenthesis_count: return string_to_parse
    elif open_parenthesis_count != closed_parenthesis_count: raise Exception(f'Not matching parenthesis')


#Coordinate the functions to get result!!!
def coordinate(the_input):
    try:
        res = eval(parse(pre_parse(str(the_input))))
        return res
    except Exception as e: return (f'Error: {e}')


# Print functions in Aki's CoddyCalculator
def print_functions():

    print("These are the functions in Aki's CoddyCalculator: \n")
    print(" - calc(op, n1, n2)\n - eval(op_num_lst) \n - struct(input_list) \n - get_next(string, input_number) \n - parse(string_to_parse) \n - pre_parse(string_to_parse) \n - coordinate(the_input) \n - print_functions() \n - run_calc()")


# Run Function
def run_calc():

    global calc_history
    global ans_history
    global answer
    global ans_key

    print(f'Hello, please enter with operators.')
    print(f'The operators are  \n{operator_keys} \nEnter "op" or "operators" to show up valid operators\n')
    print('examples:\n 2 * (25 + 2) \n 3 ^ 24 \n 3-2+10 \n ans mul2 \n\n')

    while True:
        user_input = input("Enter your input (enter 'q' or 'quit' to exit, 'h' or 'history' to open history): ")
        if user_input.lower() in ['q', 'quit']:
            print("Exiting...")
            break

        elif user_input.lower() in ['op', 'operators']:
            print(f"Operators: {operator_keys}")

        elif user_input.lower() in ['h', 'history']:
            print_calc_history()
            
        else:

            if "h" in user_input:

                result = calc_history[redo_calc(user_input)][1]

                calc_history[ans_history] = [user_input, result]

                ans_key = list(calc_history.keys())[-1]
                answer = calc_history[ans_key][1]

                print(f"Result: {calc_history[redo_calc(user_input)][0]} = {calc_history[redo_calc(user_input)][1]}")

                ans_history += 1
            else:

                result = coordinate(user_input)

                calc_history[ans_history] = [user_input, result]

                ans_key = list(calc_history.keys())[-1]
                answer = calc_history[ans_key][1]

                print("Result:", result)

                ans_history += 1

        

if __name__ == "__main__":
    run_calc()