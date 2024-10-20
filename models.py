class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # "operator" or "operand"
        self.value = value      # Operator or operand value
        self.left = left        # Left child node
        self.right = right      # Right child node

    def __repr__(self):
        return f"Node({self.type}, {self.value})"
