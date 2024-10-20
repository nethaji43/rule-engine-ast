# Rule Engine with AST

## Overview
This project is a Rule Engine application that uses an Abstract Syntax Tree (AST) to determine user eligibility based on attributes like age, department, income, and experience. The system allows for dynamic creation, combination, and modification of rules, providing an API for interacting with the rule engine.

## Table of Contents
- [Features](#features)
- [Data Structure](#data-structure)
- [API Design](#api-design)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features
- Create rules using a simple rule string syntax.
- Combine multiple rules into a single AST.
- Evaluate rules against user attributes.
- Error handling for invalid rule strings and unsupported operations.

## Data Structure
The rule engine uses a Node data structure to represent the AST:
- **type**: String indicating the node type ("operator" for AND/OR, "operand" for conditions).
- **left**: Reference to another Node (left child).
- **right**: Reference to another Node (right child for operators).
- **value**: Optional value for operand nodes (e.g., conditions).

## API Design
The following API endpoints are available:
1. **Create Rule**
   - **Endpoint**: `/create_rule/`
   - **Method**: POST
   - **Body**: `{"rule_string": "your_rule_string"}`
   - **Response**: Returns the AST representation of the created rule.

2. **Combine Rules**
   - **Endpoint**: `/combine_rules/`
   - **Method**: POST
   - **Body**: `{"rules": ["rule1_string", "rule2_string"]}`
   - **Response**: Returns the combined AST of the rules.

3. **Evaluate Rule**
   - **Endpoint**: `/evaluate_rule/`
   - **Method**: POST
   - **Body**: 
   ```json
   {
       "ast": {
           "type": "operator",
           "value": "AND",
           "left": {"type": "operand", "value": ["age", ">", "30"]},
           "right": {"type": "operand", "value": ["salary", "<", "50000"]}
       },
       "data": {"age": 35, "salary": 40000}
   }
