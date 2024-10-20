from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from ast_engine import create_rule, combine_rules, evaluate_rule  # Import functions from ast_engine

app = FastAPI()

# Define the request models
class RuleRequest(BaseModel):
    rule_string: str

class CombineRulesRequest(BaseModel):
    rules: List[str]

class EvaluateRuleRequest(BaseModel):
    ast: Dict[str, Any]
    data: Dict[str, Any]

# Route to create a rule
@app.post("/create_rule/")
async def create_rule_endpoint(request: RuleRequest):
    try:
        rule_ast = create_rule(request.rule_string)
        return {
            "message": "Rule created successfully",
            "ast": serialize_ast(rule_ast)
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Route to combine multiple rules
@app.post("/combine_rules/")
async def combine_rules_endpoint(request: CombineRulesRequest):
    try:
        combined_ast = combine_rules(request.rules)
        return {
            "message": "Rules combined successfully",
            "ast": serialize_ast(combined_ast)
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Route to evaluate a rule
@app.post("/evaluate_rule/")
async def evaluate_rule_endpoint(request: EvaluateRuleRequest):
    try:
        result = evaluate_rule(request.ast, request.data)
        return {
            "message": "Evaluation completed",
            "result": result
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Helper function to serialize the AST for response
def serialize_ast(node):
    if not node:
        return None
    return {
        "type": node.type,
        "value": node.value,
        "left": serialize_ast(node.left),
        "right": serialize_ast(node.right)
    }
