import math

# Shunting Yard algorithm implementation. Could also use recursion.
# Shunting Yard converts infix expressions into Reverse Polish Notation.

# Why did I choose Shunting Yard, over recursion? The main reason is complexity - Recursion can be challenging to implement and debug.
# Considering the time constraints, I didn't feel confident in implementing recursion to solve this problem.
# Some added benefits over recursion include memory efficency through the use of two stacks avoiding any potential stack overflow issues associated
# With recursion (Python has around 1000 level of recursion before stackoverflow occurs so it's unlikely to be hit, but is worth considering).
# Python also being an interpreted language, can result in overheads for function calls, particularly when recursively called. Shunting Yard doesn't require that overhead.

# Assigning each operator a precendence value and an association. This'll be handy later.
# Particularly, dictionary usage is handy as you can look up and retrieve in constant time. When compared to conditional checking,
# which would grow in linear time. 
# It's also much easier to update and extend, as you can add and edit easily.
# It has the added benefit of being easily readable and organised, by keeping operator related information outside of functions.
operators = {
    '+': (1, 'L'), '-': (1, 'L'),
    '*': (2, 'L'), '/': (2, 'L'),
    '^': (3, 'R')
}

def tokenize_string(expression):
    expression = expression.replace(' ', '') #Important to remove white space now else you run into issues later.
    tokens = []
    current_number = []  # Used to build numbers with multiple digits or decimals
    i = 0 
    
    while i < len(expression):
        char = expression[i]
        
        # Handle digits and decimal points for numbers
        if char.isdigit() or char == '.':
            current_number.append(char)  # Build up the number with digits and decimal points
            
        else:
            # Finalize and append any current number we've been building
            if current_number:
                tokens.append(''.join(current_number))
                current_number = []
            
            # Handle negative numbers at the start or after an operator/parenthesis
            if char == '-' and (i == 0 or expression[i - 1] in '(-+*/^)'):
                current_number.append(char)  # Start a negative number
            
            # If it's a recognized operator or parenthesis, add directly to tokens
            elif char in operators or char in '()':
                tokens.append(char)
                
            else:
                # Raise error for any unrecognized characters
                raise ValueError(f"Unexpected character: {char}")
        
        i += 1
    
    # Add the last number if there's one left over
    if current_number:
        tokens.append(''.join(current_number))
    
    return tokens

#Helper function to check if our tokens are numeric or not.
def check_is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def infix_to_rpn(expression):
    output = [] # Output list for RPN
    stack = [] # Working stack for our operators and brackets
    tokens = tokenize_string(expression) #Tokenize our string now, and store for use.

    for token in tokens:
        if check_is_number(token):
            output.append(token) #If token is a number, add to output list.

        elif token in operators:
            #Attempting to solve when we should remove operators from our stack into our output list. Start by...
            # Checkign the stack isn't empty
            # Checking that the whatever is on top is actually an operator.
            # If not, then loop doesn't execute.

            while (stack and stack[-1] in operators and
                   ((operators[token][1] == 'L' and operators[token][0] <= operators[stack[-1]][0]) or
                    (operators[token][1] == 'R' and operators[token][0] < operators[stack[-1]][0]))):
                # This bit is particularly confusing. I'm handling left and right associative operators to determine pop precedence.
                # Checking if the operator is L or R associative first.
                # Then, I check the precedence of the operator.
                # Left associative... Pop if the current operator has lower or equal precedence to the operator on the stack.

                # Right associative... Higher precendence means that we pop if the operator on top of the stack is lower in precendence.
                # In other words, right associative operators should be pushed before other operators.
                # Left associative operators. Higher precedence is popped first, (* or /) and then lower precedence (+ or -)
                output.append(stack.pop()) # Highest precendence operators added to output
            stack.append(token) # Put current operator onto the stack.
        
        elif token == '(':
            stack.append(token)

        elif token == ')':
            while stack and stack [-1] != '(':
                output.append(stack.pop()) #Pop until left bracket is found
            stack.pop() #Discard the bracket

    while stack:
        output.append(stack.pop()) #Pop all remaining operators to the output list.

    return output

def evaluate_rpn(rpn_expression):
    stack = []

    for token in rpn_expression:
        if check_is_number(token):
            stack.append(float(token)) #Converting everything to a float to support decimals
        else:
            b = stack.pop() #Grab number
            a = stack.pop() if stack else 0 #Grab another unless the stack is empty

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                stack.append(a / b)
            elif token == '^':
                stack.append(math.pow(a, b)) #I'm not sure if I should use math, but it seemed like a bad idea to implement my own exponent function

    return stack[0] #Returns the final item in the stack

def evaluate_expression(expression):
    rpn = infix_to_rpn(expression)
    result = evaluate_rpn(rpn)
    return result

expression = "-53 + -24"
result = evaluate_expression(expression)
print("Expression is: ", expression)
print ("Result: ", result)