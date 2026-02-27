from acdcast import *

class InstructionList:

    def __init__(self):

        self.instructions = []

    def append(self, instruction: str):

        self.instructions.append(instruction)

    def extend(self, newinstructions: "InstructionList"):
        
        self.instructions.extend(newinstructions.instructions)

    def __iter__(self):
        return iter(self.instructions)




def codegenerator(program: list[ASTNode]) -> InstructionList:

    code = InstructionList()

    for statement in program:

        newcode = stmtcodegen(statement)
        code.extend(newcode)

    return code
    

optypes = {TokenType.EXPONENT:'^',
           TokenType.TIMES:'*',
           TokenType.DIVIDE:'/',
           TokenType.PLUS:'+',
           TokenType.MINUS:'-'}

def stmtcodegen(statement: ASTNode) -> InstructionList:

    code = InstructionList()

    if isinstance(statement, IntDclNode):

        return code


    if isinstance(statement, IntLitNode):

        code.append(statement.value)

        return code


    if isinstance(statement, VarRefNode):

        code.append(f"l{statement.varname}")

        return code
    
    if isinstance(statement, PrintNode):

        code.append(f"l{statement.varname}")

        code.append("p")

        return code

    
    if isinstance(statement, AssignNode):

        code.extend(stmtcodegen(statement.expr))

        code.append(f"s{statement.varname}")
    
        return code

    if isinstance(statement, BinOpNode):

        left = stmtcodegen(statement.left)
        right = stmtcodegen(statement.right)

        code.instructions.extend(left)

        if statement.optype == TokenType.EXPONENT and isinstance(statement.right, IntLitNode):
            code.instructions.extend(['d' for i in range(int(statement.right.value)-1)])
            code.instructions.extend(['*' for i in range(int(statement.right.value)-1)])
        else:

            code.instructions.extend(right)

            code.append(optypes[statement.optype])

        return code
    

    # Should never get here
    return code
