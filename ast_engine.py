import re
from typing import Dict, Any, Optional, List  # Import List here

class Node:
    def __init__(self, node_type: str, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value      # Optional value for operand nodes
        self.left = left        # Left child node
        self.right = right      # Right child node

def create_rule(rule_string):
    tokens = tokenize(rule_string)
    return parse_expression(tokens)

def tokenize(rule_string):
    # Tokenize the input string, considering operators, operands, and parentheses
    token_pattern = r'(\(|\)|AND|OR|\w+\s*[\=<>!]+\s*[\w\']+)'
    tokens = re.findall(token_pattern, rule_string)
    return [token.strip() for token in tokens if token.strip()]

def parse_expression(tokens):
    stack = []
    operators = []
    
    for token in tokens:
        if token == '(':
            # Start a new subexpression
            operators.append(token)
        elif token == ')':
            # Resolve the subexpression
            while operators and operators[-1] != '(':
                operator = operators.pop()
                right = stack.pop()
                left = stack.pop()
                stack.append(Node(node_type='operator', value=operator, left=left, right=right))
            operators.pop()  # Remove the '('
        elif token in ('AND', 'OR'):
            while (operators and operators[-1] in ('AND', 'OR')):
                operator = operators.pop()
                right = stack.pop()
                left = stack.pop()
                stack.append(Node(node_type='operator', value=operator, left=left, right=right))
            operators.append(token)
        else:
            # Match conditions e.g., "age > 30"
            match = re.match(r'(\w+)\s*([\=<>!]+)\s*(.*)', token)
            if match:
                field, operator, value = match.groups()
                stack.append(Node(node_type='operand', value=(field, operator, value)))
            else:
                raise ValueError(f"Invalid token: {token}")

    # Resolve remaining operators in the stack
    while operators:
        operator = operators.pop()
        right = stack.pop()
        left = stack.pop()
        stack.append(Node(node_type='operator', value=operator, left=left, right=right))

    # Ensure there is one root node in the stack
    if len(stack) != 1:
        raise ValueError("Invalid rule string; remaining operands in stack")

    return stack.pop()  # Return the root of the AST



def combine_rules(rules: List[str]) -> Optional[Node]:
    """Combine multiple rules into one AST."""
    asts = [create_rule(rule) for rule in rules]
    
    if len(asts) == 0:
        return None
    if len(asts) == 1:
        return asts[0]

    combined_node = Node(node_type='operator', value='AND', left=asts[0], right=asts[1])
    
    for ast in asts[2:]:
        combined_node = Node(node_type='operator', value='AND', left=combined_node, right=ast)

    return combined_node

def evaluate_rule(ast: Dict[str, Any], data: Dict[str, Any]) -> bool:
    """
    Evaluate the given AST against the provided data.

    - **ast**: The AST representation of the rule to evaluate.
    - **data**: A dictionary of attributes to evaluate against the rule.
    """
    if ast['type'] == 'operator':
        # Recursively evaluate left and right operands
        left_result = evaluate_rule(ast['left'], data) if ast['left'] else None
        right_result = evaluate_rule(ast['right'], data) if ast['right'] else None
        
        # Perform logical operations based on the operator type
        if ast['value'] == 'AND':
            return left_result and right_result
        elif ast['value'] == 'OR':
            return left_result or right_result
    elif ast['type'] == 'operand':
        # Handle the operand correctly
        field, operator, value = ast['value']  # Extract the values

        # Convert value to appropriate type if necessary
        if value.isdigit():  # If the value is a number
            value = int(value)
        elif value.replace('.', '', 1).isdigit():  # Check for float
            value = float(value)
        else:
            value = value.strip("'")  # Remove quotes if any

        # Perform the comparison
        if operator == '>':
            return data.get(field, None) > value
        elif operator == '<':
            return data.get(field, None) < value
        elif operator == '>=':
            return data.get(field, None) >= value
        elif operator == '<=':
            return data.get(field, None) <= value
        elif operator == '==':
            return data.get(field, None) == value
        elif operator == '!=':
            return data.get(field, None) != value

    # Default case if no condition is met
    return False
