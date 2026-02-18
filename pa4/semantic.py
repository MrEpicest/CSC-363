from acdcast import *

class SemanticError(Exception):
    pass


def semanticanalysis(program: list[ASTNode]) -> None:

    declared = []
    initialized = []

    for linenumber, statement in enumerate(program, start=1):
        _semantic_check_stmt(statement, declared, initialized, linenumber)
    
    return 


def _semantic_check_stmt(statement: ASTNode, declared: list[str], initialized: list[str], linenumber: int) -> None:

    if isinstance(statement, IntDclNode):
        if statement.varname in declared:
            raise SemanticError(f"Variable {statement.varname!r} redeclared at line {linenumber}")
        else:
            declared.append(statement.varname)
            return
        
    
    if isinstance(statement, PrintNode):
        if statement.varname not in declared:
            raise SemanticError(f"Trying to print undeclared variable {statement.varname!r} at line {linenumber}")
        elif statement.varname not in initialized:
            raise SemanticError(f"Trying to print uninitialized variable {statement.varname!r} at line {linenumber}")
        return
    
    if isinstance(statement, AssignNode):
        if statement.varname not in declared:
            raise SemanticError(f"Assignment to undeclared variable {statement.varname!r} at line {linenumber}")
        else:
            _semantic_check_expr(statement.expr, declared, initialized, linenumber)
            initialized.append(statement.varname)
            return


    raise SemanticError(f"Unknown statement type at line {linenumber}")
    # Catches any weird statement types; this should never happen for a validly parsed program
    # Keeping it here though will help if your parser has an undiscovered or unfixed bug


def _semantic_check_expr(expr: ASTNode, declared: list[str], initialized: list[str], linenumber: int):
    if isinstance(expr, IntLitNode):
        return
    
    if isinstance(expr, VarRefNode):
        if expr.varname not in declared:
            raise SemanticError(f"Use of undeclared variable {expr.varname!r} at line {linenumber}")
        elif expr.varname not in initialized:
            raise SemanticError(f"Use of uninitialized variable {expr.varname!r} at line {linenumber}")
        return
        # SemanticError(f"Use of undeclared variable {varname!r} at line {linenumber}")
        # SemanticError(f"Use of unitialized variable {varname!r} at line {linenumber}")
        
    if isinstance(expr, BinOpNode):
        # Two recursive calls go here...
        _semantic_check_expr(expr.left, declared, initialized, linenumber)
        _semantic_check_expr(expr.right, declared, initialized, linenumber)
        return
    
    raise SemanticError(f"Unknown expression type at line {linenumber}")
    # Catches any weird statement types; this should never happen for a validly parsed program
    # Keeping it here though will help if your parser has an undiscovered or unfixed bug