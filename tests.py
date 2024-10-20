from ast_engine import create_rule, combine_rules, evaluate_rule

def test_create_rule():
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    rule_ast = create_rule(rule_string)
    assert rule_ast is not None

def test_evaluate_rule():
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
    rule_ast = create_rule(rule_string)
    user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    result = evaluate_rule(rule_ast, user_data)
    assert result == True

def test_combine_rules():
    rule1 = create_rule("age > 30 AND salary > 50000")
    rule2 = create_rule("experience > 5")
    combined_ast = combine_rules([rule1, rule2])
    assert combined_ast is not None
