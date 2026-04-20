import sys
import os
from typing import List

from .CodeObject import CodeObject
from .InstructionList import InstructionList
from .instructions import *
from ..compiler import *
from ..ast import *
from ..ast.visitor.AbstractASTVisitor import AbstractASTVisitor

class CodeGenerator(AbstractASTVisitor):

  def __init__(self):
    self.intRegCount = 1
    self.numCtrlStructs = 0
    self.floatRegCount = 1
    self.intTempPrefix = 't'
    self.floatTempPrefix = 'f'
    self.loopLabel = 0
    self.elseLabel = 0
    self.outLabel = 0
    self.currFunc = None

  def getIntRegCount(self):
    return self.intRegCount

  def getFloatRegCount(self):
    return self.floatRegCount



  def postprocessVarNode(self, node: VarNode) -> CodeObject:
    sym = node.getSymbol()

    co = CodeObject(sym)
    co.lval = True
    co.type = node.getType()

    return co



  
  def postprocessIntLitNode(self, node: IntLitNode) -> CodeObject:
    ''' 
    Copy from PA8
    '''

    co = CodeObject()

    temp = self.generateTemp(Scope.Type.INT)
    val = node.getVal()
    # LI t2, 5
    co.code.append(Li(temp, val))
    co.temp = temp
    co.lval = False
    co.type = node.getType()

    return co


  def postprocessFloatLitNode(self, node: FloatLitNode) -> CodeObject:
    ''' 
    Copy from PA8
    '''
    co = CodeObject()

    temp = self.generateTemp(Scope.Type.FLOAT)
    val = node.getVal()

    co.code.append(FImm(temp, val))
    co.temp = temp
    co.lval = False
    co.type = node.getType()
  
    return co
  

  def postprocessBinaryOpNode(self, node: BinaryOpNode, left: CodeObject, right: CodeObject) -> CodeObject:
    ''' 
    Copy from PA8
    '''
    co = CodeObject()
    newcode = CodeObject()

    if left.lval:
      left = self.rvalify(left)

    co.code.extend(left.code)

    if right.lval:
        right = self.rvalify(right)

    co.code.extend(right.code)

    operator = node.getOp()

    if left.type is Scope.Type.INT and right.type is Scope.Type.INT:
    
      temp = self.generateTemp(Scope.Type.INT)

      if operator == BinaryOpNode.OpType.ADD:
        co.code.append(Add(dest=temp, src1=left.temp, src2=right.temp))
      elif operator == BinaryOpNode.OpType.SUB:
        co.code.append(Sub(dest=temp, src1=left.temp, src2=right.temp))
      elif operator == BinaryOpNode.OpType.MUL:
        co.code.append(Mul(dest=temp, src1=left.temp, src2=right.temp))
      elif operator == BinaryOpNode.OpType.DIV:
        co.code.append(Div(dest=temp, src1=left.temp, src2=right.temp))

      co.type = left.type # update CodeObject type; left and right are the same type at this point

    elif left.type is Scope.Type.FLOAT and right.type is Scope.Type.FLOAT:

      temp = self.generateTemp(Scope.Type.FLOAT)

      if operator == BinaryOpNode.OpType.ADD:
        co.code.append(FAdd(dest=temp, src1=left.temp, src2=right.temp))
      elif operator == BinaryOpNode.OpType.SUB:
        co.code.append(FSub(dest=temp, src1=left.temp, src2=right.temp))
      elif operator == BinaryOpNode.OpType.MUL:
        co.code.append(FMul(dest=temp, src1=left.temp, src2=right.temp))
      elif operator == BinaryOpNode.OpType.DIV:
        co.code.append(FDiv(dest=temp, src1=left.temp, src2=right.temp))

      co.type = left.type # update CodeObject type; left and right are the same type at this point

    else:
      raise CodeGenerator(f"can't add {right.type} with {left.type}")
    

    co.temp = temp
    co.lval = False
    co.type = left.type

    return co
	 



  def postprocessUnaryOpNode(self, node: UnaryOpNode, expr: CodeObject) -> CodeObject:
    ''' 
    Copy from PA8
    '''
    co = CodeObject()  # Step 0

    if expr.lval:
      expr = self.rvalify(expr)

    co.code.extend(expr.code) # Add in all the code required to get expr after rvalifying


    if expr.type == Scope.Type.INT:
      temp = self.generateTemp(Scope.Type.INT)
      co.code.append(Neg(src=expr.temp, dest=temp))
      

    elif expr.type == Scope.Type.FLOAT:
      temp = self.generateTemp(Scope.Type.FLOAT)
      co.code.append(FNeg(src=expr.temp, dest=temp))

    else:
      raise Exception("Non int/float type in unary op!")

    co.type = expr.type
    co.temp = temp
    co.lval = False 

    return co

  def postprocessAssignNode(self, node: AssignNode, left: CodeObject, right: CodeObject) -> CodeObject:
    ''' 
    Copy from PA8
    '''
    co = CodeObject()
  
    assert(left.isVar())
    assert(left.lval)

    if right.lval:
      right = self.rvalify(right)

    co.code.extend(right.code)

    if left.ste.isLocal() == True:

      offset = self.generateAddrFromVariable(left)
      
      if right.type is Scope.Type.INT:
        co.code.append(Sw(right.temp, "fp", offset))
      elif right.type is Scope.Type.FLOAT:
        co.code.append(Fsw(right.temp, "fp", offset))

    else:

      address = self.generateAddrFromVariable(left)
      addr_temp = self.generateTemp(Scope.Type.INT)
      co.code.append(La(addr_temp, address)) # La t0, address

      if right.type is Scope.Type.INT:
        co.code.append(Sw(right.temp, addr_temp, '0')) # Sw t1, 0(t0)   (assuming t1 has a value that we can store)
      elif right.type is Scope.Type.FLOAT:
        co.code.append(Fsw(right.temp, addr_temp, '0')) # Fsw f1, 0(t0)   (assuming t1 has a value that we can store)
   
    return co

  def postprocessStatementListNode(self, node: StatementListNode, statements: list) -> CodeObject:
    co = CodeObject()

    for subcode in statements:
      co.code.extend(subcode.code)

    co.type = None
    return co

	 # Generate code for read
	 # 
	 # Step 0: create new code object
	 # Step 1: add code from VarNode (make sure it's an lval)
	 # Step 2: generate GetI instruction, storing into temp
	 # Step 3: generate store, to store temp in variable
	
  def postprocessReadNode(self, node: ReadNode, var: CodeObject) -> CodeObject:
    ''' 
    Copy from PA8
    '''
    co = CodeObject()

    assert(var.isVar())

    if var.ste.isLocal():

      if var.type is Scope.Type.INT:
        temp = self.generateTemp(Scope.Type.INT)
        co.code.append(GetI(temp))
        offset = self.generateAddrFromVariable(var)
        co.code.append(Sw(temp, "fp", offset))

      elif var.type is Scope.Type.FLOAT:
        temp = self.generateTemp(Scope.Type.FLOAT)
        co.code.append(GetF(temp))
        offset = self.generateAddrFromVariable(var)
        co.code.append(Fsw(temp, "fp", offset))

    else:

      if var.type is Scope.Type.INT:
        temp = self.generateTemp(Scope.Type.INT)
        co.code.append(GetI(temp))
        address = self.generateAddrFromVariable(var)
        temp2 = self.generateTemp(Scope.Type.INT)
        co.code.append(La(temp2, address))
        co.code.append(Sw(temp, temp2, '0'))

      elif var.type is Scope.Type.FLOAT:
        temp = self.generateTemp(Scope.Type.FLOAT)
        co.code.append(GetF(temp))
        address = self.generateAddrFromVariable(var)
        temp2 = self.generateTemp(Scope.Type.INT)
        co.code.append(La(temp2, address))
        co.code.append(Fsw(temp, temp2, '0'))
        pass

      else:
        raise Exception("Bad type in read node")
    
    return co
	 

  def postprocessWriteNode(self, node: WriteNode, expr: CodeObject) -> CodeObject:
    ''' 
    Copy from PA8
    '''
    co = CodeObject()

    mytype = expr.getType()

    """if expr.isVar():

      # first get the address to load from and store it in a register (addr_temp)

      address = self.generateAddrFromVariable(expr)
      addr_temp = self.generateTemp(Scope.Type.INT)

     # LA t0, address

      if mytype is Scope.Type.INT:

        temp = self.generateTemp(Scope.Type.INT)

        #co.code.append(Lw(temp, addr_temp, '0'))        

        co.code.append(PutI(expr.temp))

      elif mytype is Scope.Type.FLOAT:

        
        temp = self.generateTemp(Scope.Type.FLOAT)

        #co.code.append(Flw(temp, addr_temp, '0'))

        co.code.append(PutF(expr.temp))

      elif mytype is Scope.Type.STRING:

        co.code.append(PutS(addr_temp))"""

    #else:

    if expr.lval == True:
        expr = self.rvalify(expr)

    co.code.extend(expr.code)

    if mytype is Scope.Type.INT:

      co.code.append(PutI(expr.temp))

    elif mytype is Scope.Type.FLOAT:

      co.code.append(PutF(expr.temp))

    elif mytype is Scope.Type.STRING:

      co.code.append(PutS(expr.temp))

    return co




  def postprocessCondNode(self, node: CondNode, left: CodeObject, right: CodeObject) -> CodeObject:
    '''
    NEW:
    '''
    node.setOp(node.getReversedOp(node.getOpFromString(node.getOp()))) # Reverse comparison type
    
    co = CodeObject()

    if left.lval == True: # can't simply do "if left.lval" because left.lval could equal None (which is not a boolean)
      left = self.rvalify(left)

    if right.lval == True:
      right = self.rvalify(right)

    co.code.extend(left.code)
    co.code.extend(right.code)

    #co.code.append(f"; Left type: {left.type}")
    #co.code.append(f"; Right type: {right.type}")

    #elseLabel = self._generateElseLabel(self._getnumCtrlStruct())

    if left.type is Scope.Type.INT and right.type is Scope.Type.INT:
      co.type = Scope.Type.INT
    elif left.type is Scope.Type.FLOAT and right.type is Scope.Type.FLOAT:
      co.type = Scope.Type.FLOAT
    else:
      raise CodeGenerator(f"can't compare {left.type} to {right.type}")

    

    co.temp = left.temp
    co.temp2 = right.temp
    co.cmptype = node.oc
  

    return co




  def postprocessIfStatementNode(self, node: IfStatementNode, cond: CodeObject, tlist: CodeObject, elist: CodeObject) -> CodeObject:
    '''
    NEW
    '''

    self._incrnumCtrlStruct()
    
    labelnum = self._getnumCtrlStruct()
    
    co = CodeObject()

    co.code.extend(cond.code)

    elseLabel = self._generateElseLabel(self._getnumCtrlStruct())

    #co.code.append(str(cond.cmptype == CondNode.OpType.LE))
    #co.code.append(str(cond.type == Scope.Type.INT))

    if cond.type == Scope.Type.INT:
      if cond.cmptype == CondNode.OpType.EQ:
        co.code.append(Beq(cond.temp, cond.temp2, elseLabel))
      elif cond.cmptype == CondNode.OpType.NE:
        co.code.append(Bne(cond.temp, cond.temp2, elseLabel))
      elif cond.cmptype == CondNode.OpType.LT:
        co.code.append(Blt(cond.temp, cond.temp2, elseLabel))
      elif cond.cmptype == CondNode.OpType.LE:
        co.code.append(Ble(cond.temp, cond.temp2, elseLabel))
      elif cond.cmptype == CondNode.OpType.GT:
        co.code.append(Bgt(cond.temp, cond.temp2, elseLabel))
      elif cond.cmptype == CondNode.OpType.GE:
        co.code.append(Bge(cond.temp, cond.temp2, elseLabel))

    elif cond.type == Scope.Type.FLOAT:
      temp = self.generateTemp(Scope.Type.INT)
      if cond.cmptype == CondNode.OpType.EQ:
        co.code.append(Feq(cond.temp, cond.temp2, temp)) # FEQ t0, t1, t2
        co.code.append(Bne(temp, 'x0',elseLabel))       # BNE t2, x0, else
      elif cond.cmptype == CondNode.OpType.NE:
        co.code.append(Feq(cond.temp, cond.temp2, temp))
        co.code.append(Beq(temp, 'x0', elseLabel))
      elif cond.cmptype == CondNode.OpType.LT:
        co.code.append(Flt(cond.temp, cond.temp2, temp))
        co.code.append(Bne(temp, 'x0', elseLabel))
      elif cond.cmptype == CondNode.OpType.LE:
        co.code.append(Fle(cond.temp, cond.temp2, temp))
        co.code.append(Bne(temp, 'x0', elseLabel))
      elif cond.cmptype == CondNode.OpType.GT:
        co.code.append(Fle(cond.temp, cond.temp2, temp))
        co.code.append(Beq(temp, 'x0', elseLabel))
      elif cond.cmptype == CondNode.OpType.GE:
        co.code.append(Flt(cond.temp, cond.temp2, temp))
        co.code.append(Beq(temp, 'x0', elseLabel))

    co.code.append(self._generateThenLabel(labelnum)+":")
    co.code.extend(tlist.code)
    co.code.append(J(self._generateDoneLabel(labelnum)))
    co.code.append(self._generateElseLabel(labelnum)+":")
    if elist is not None:
      co.code.extend(elist.code)
    co.code.append(self._generateDoneLabel(labelnum)+":")

    return co



  def postprocessWhileNode(self, node: WhileNode, cond: CodeObject, wlist:
  CodeObject) -> CodeObject:
    ''' 
    NEW
    '''

    self._incrnumCtrlStruct()
    
    labelnum = self._getnumCtrlStruct()
    co = CodeObject()

    co.code.append(self._generateLoopLabel(labelnum)+":")
    co.code.extend(cond.code)
    
    doneLabel = self._generateDoneLabel(self._getnumCtrlStruct())

    #co.code.append(str(cond.cmptype == CondNode.OpType.LE))
    #co.code.append(str(cond.type == Scope.Type.INT))

    if cond.type == Scope.Type.INT:
      if cond.cmptype == CondNode.OpType.EQ:
        co.code.append(Beq(cond.temp, cond.temp2, doneLabel))
      elif cond.cmptype == CondNode.OpType.NE:
        co.code.append(Bne(cond.temp, cond.temp2, doneLabel))
      elif cond.cmptype == CondNode.OpType.LT:
        co.code.append(Blt(cond.temp, cond.temp2, doneLabel))
      elif cond.cmptype == CondNode.OpType.LE:
        co.code.append(Ble(cond.temp, cond.temp2, doneLabel))
      elif cond.cmptype == CondNode.OpType.GT:
        co.code.append(Bgt(cond.temp, cond.temp2, doneLabel))
      elif cond.cmptype == CondNode.OpType.GE:
        co.code.append(Bge(cond.temp, cond.temp2, doneLabel))

    elif cond.type == Scope.Type.FLOAT:
      temp = self.generateTemp(Scope.Type.INT)
      if cond.cmptype == CondNode.OpType.EQ:
        co.code.append(Feq(cond.temp, cond.temp2, temp)) # FEQ t0, t1, t2
        co.code.append(Bne(temp, 'x0',doneLabel))       # BNE t2, x0, else
      elif cond.cmptype == CondNode.OpType.NE:
        co.code.append(Feq(cond.temp, cond.temp2, temp))
        co.code.append(Beq(temp, 'x0', doneLabel))
      elif cond.cmptype == CondNode.OpType.LT:
        co.code.append(Flt(cond.temp, cond.temp2, temp))
        co.code.append(Bne(temp, 'x0', doneLabel))
      elif cond.cmptype == CondNode.OpType.LE:
        co.code.append(Fle(cond.temp, cond.temp2, temp))
        co.code.append(Bne(temp, 'x0', doneLabel))
      elif cond.cmptype == CondNode.OpType.GT:
        co.code.append(Fle(cond.temp, cond.temp2, temp))
        co.code.append(Beq(temp, 'x0', doneLabel))
      elif cond.cmptype == CondNode.OpType.GE:
        co.code.append(Flt(cond.temp, cond.temp2, temp))
        co.code.append(Beq(temp, 'x0', doneLabel))

    co.code.extend(wlist.code)
    co.code.append(J(self._generateLoopLabel(labelnum)))
    co.code.append(self._generateElseLabel(labelnum)+":")
    co.code.append(self._generateDoneLabel(labelnum)+":")
    
    return co


  def postprocessReturnNode(self, node: ReturnNode, retExpr: CodeObject) -> CodeObject:
    '''
    This is responsible for handing things like "return b" or "return".  
    Notably, this part will NOT generate a RET instruction.
    Step 1: rvalify (if necessary) code for the retExpr
    Step 2: add in retExpr code
    Step 3: store return value from retExpr's temporary to the return value spot in the stack (8 up from FP)
    '''
    co = CodeObject()

    if retExpr.lval == True:
      retExpr = self.rvalify(retExpr)

    co.code.extend(retExpr.code)

    if retExpr.type == Scope.Type.INT:
      co.code.append(Sw(retExpr.temp, "fp", "8"))
    elif retExpr.type == Scope.Type.FLOAT:
      co.code.append(Fsw(retExpr.temp, "fp", "8"))


    return co


  def preprocessFunctionNode(self, node: FunctionNode):

    self.currFunc = node.getFuncName()

    self.intRegCount = 0
    self.floatRegCount = 0


  def postprocessFunctionNode(self, node: FunctionNode, body: CodeObject) -> CodeObject:
    '''
    Responsible for actually putting together a function's code
    Step 1: Set up stack frame
    Step 2: Save temporaries
    Step 3: Add in body code (this will include a return node)
    Step 4: Load temporaries
    Step 5: Undo stack frame
    Step 6: Append the RET instruction
    '''

    co = CodeObject()

    numLocals = node.scope.getNumLocals()
    allocation = numLocals*(4) # amount of stack space needed to allocate for local variables

    # entry label
    co.code.append(self._generateFunctionEntryLabel(node.funcName)+":")

    # set up stack frame
    co.code.append(Sw("fp", "sp", "0")) # push the address of fp onto the stack
    co.code.append(Mv(dest="fp", src="sp")) # move the address of sp into fp
    co.code.append(Addi(dest="sp", src1="sp", imm=str(-4 - allocation))) # -4 for initial decrement and then -allocation for local variables
   
    # save registers
    for i in range(self.intRegCount):
      co.code.append(Sw(f"t{i}", "sp", "0"))
      co.code.append(Addi(dest="sp", src1="sp", imm="-4"))
    for i in range(self.floatRegCount):
      co.code.append(Fsw(f"f{i}", "sp", "0"))
      co.code.append(Addi(dest="sp", src1="sp", imm="-4"))

    # body
    co.code.append(self._generateFunctionCodeLabel(node.funcName)+":")
    co.code.extend(body.code)

    # ret label
    co.code.append(self._generateFunctionRetLabel()+":")

    # increment to registers
    co.code.append(Addi(dest="sp", src1="sp", imm="4"))

    # restore registers
    for i in range(self.floatRegCount-1, -1, -1):
      co.code.append(Flw(f"f{i}", "sp", "0"))
      co.code.append(Addi(dest="sp", src1="sp", imm="4"))
    for i in range(self.intRegCount-1, -1, -1):
      co.code.append(Lw(f"t{i}", "sp", "0"))
      co.code.append(Addi(dest="sp", src1="sp", imm="4"))

    # undo stack frame
    co.code.append(Mv(dest="sp", src="fp"))
    co.code.append(Lw("fp", "fp", "0"))

    # return
    co.code.append(Ret())

    return co


	

  def postprocessFunctionListNode(self, node: FunctionListNode, functions: List[CodeObject]) -> CodeObject:
    '''
    Generate code for the list of functions. This is the "top level" code generation function
    Step 1: Set fp to point to sp
    Step 2: Insert a JR to main
    Step 3: Insert a HALT
    Step 4: Include all the code of the functions
    '''

    co = CodeObject()

    co.code.append(Mv("sp", "fp"))
    co.code.append(Jr(self._generateFunctionEntryLabel("main")))
    co.code.append(Halt())
    co.code.append(Blank())

    # Add code for each of the functions
    for c in functions:
      co.code.extend(c.code)
      co.code.append(Blank())
    
    return co


  def postprocessCallNode(self, node: CallNode, args: List[CodeObject]) -> CodeObject:
    '''
    Responsible for handling when we actually make a function call, for example, something like a = foo(b)
    The call node would be the foo(b) call.
    Step 1: For each argument, insert rvalified code object and push result to stack
    Step 2: Allocate space for return value (what if there isn't one?)
    Step 3: Push ra to stack
    Step 4: JR to function
    Step 5: Pop ra back from stack
    Step 6: Pop return value into fresh temporary
    Step 7: Remove arguments from stack (move sp up, no need to keep these values)
    '''

    co = CodeObject()

    # push args to stack
    for arg in args:
      if arg.lval:
        arg = self.rvalify(arg)
      co.code.extend(arg.code)
      if arg.type is Scope.Type.INT:
        co.code.append(Sw(arg.temp, "sp", "0"))
      elif arg.type is Scope.Type.FLOAT:
        co.code.append(Fsw(arg.temp, "sp", "0"))
      co.code.append(Addi(dest="sp", src1="sp", imm="-4"))

    # allocate space for rv
    co.code.append(Addi(dest="sp", src1="sp", imm="-4"))

    # store ra
    co.code.append(Sw("ra", "sp", "0"))
    co.code.append(Addi(dest="sp", src1="sp", imm="-4"))

    # call function
    co.code.append(Jr(self._generateFunctionEntryLabel(node.funcName)))

    # increment sp to ra
    co.code.append(Addi(dest="sp", src1="sp", imm="4"))

    # restore ra
    co.code.append(Lw("ra", "sp", "0"))

    # increment sp to rv
    co.code.append(Addi(dest="sp", src1="sp", imm="4"))

    # get rv
    if node.type == Scope.Type.INT:
      co.type = Scope.Type.INT # set the type so that assign nodes can handle the function call
      co.temp = self.generateTemp(Scope.Type.INT)
      co.code.append(Lw(co.temp, "sp", "0"))
    elif node.type == Scope.Type.FLOAT:
      co.type = Scope.Type.FLOAT # set the type so that assign nodes can handle the function call
      co.temp = self.generateTemp(Scope.Type.FLOAT)
      co.code.append(Flw(co.temp, "sp", "0"))

    # increment sp to top of args
    co.code.append(Addi(dest="sp", src1="sp", imm=str(len(args)*4)))
   
    return co


  
  def generateTemp(self, t: Scope.Type) -> str:
    if t == Scope.Type.INT:
      s = self.intTempPrefix + str(self.intRegCount)
      self.intRegCount += 1
      return s
    elif t == Scope.Type.FLOAT:
      s = self.floatTempPrefix + str(self.floatRegCount)
      self.floatRegCount += 1
      return s
    else:
      raise Exception("Generating temp for bad type")



  def rvalify(self, lco : CodeObject) -> CodeObject:
 
    #assert(lco.lval is True)
    #assert(lco.isVar() is True)
    
    co = CodeObject()

    if lco.ste.isLocal() == True:

      offset = self.generateAddrFromVariable(lco)

      if lco.type is Scope.Type.INT:
        temp1 = self.generateTemp(Scope.Type.INT)
        co.code.append(Lw(temp1, "fp", offset))

      elif lco.type is Scope.Type.FLOAT:
        temp1 = self.generateTemp(Scope.Type.FLOAT)
        co.code.append(Flw(temp1, "fp", offset))

      else:
        raise Exception(f"Bad type {lco.type} in rvalify!")

      co.temp = temp1

    else:

      address = self.generateAddrFromVariable(lco)
      temp1 = self.generateTemp(Scope.Type.INT) # Addresses are always ints
      co.code.append(La(temp1, address)) # Load address (global only)

      if lco.type is Scope.Type.INT:
        temp2 = self.generateTemp(Scope.Type.INT)
        co.code.append(Lw(temp2, temp1, '0'))
        co.temp = temp2

      elif lco.type is Scope.Type.FLOAT:
        temp2 = self.generateTemp(Scope.Type.FLOAT)
        co.code.append(Flw(temp2, temp1, '0'))
        co.temp = temp2

      elif lco.type is Scope.Type.STRING:
        co.temp = temp1

      else:
        raise Exception(f"Bad type {lco.type} in rvalify!")

    co.type = lco.type
    co.lval = False

    return co
  

  def generateAddrFromVariable(self, lco: CodeObject) -> str:
    ''' 
    Copy from PA8/9
    Don't use the exact same thing as in PA8...use this to get addresses
    symbol = lco.getSTE()
    address = symbol.addressToString()
    Otherwise the hex addresses for globals will get mangled
    '''
    assert(lco.isVar() is True)

    symbol = lco.getSTE()   # Get symbol from symbol table
    address = symbol.addressToString()
    #address = str(symbol.getAddress()) # Get address of variable

    return address


  def _incrnumCtrlStruct(self):
    self.numCtrlStructs += 1

  def _getnumCtrlStruct(self) -> int:
    return self.numCtrlStructs
  
  def _generateThenLabel(self, num: int) -> str:
    return "then"+str(num)

  def _generateElseLabel(self, num: int) -> str:
    return "else"+str(num)

  def _generateLoopLabel(self, num: int) -> str:
    return "loop"+str(num)

  def _generateDoneLabel(self, num: int) -> str:
    return "done"+str(num)
  


  
  def _generateFunctionEntryLabel(self, func = None) -> str:
    if func is None:
      return "func_entry_" + self.currFunc
    else:
      return "func_entry_" + func
    
  def _generateFunctionCodeLabel(self, func = None) -> str:
    if func is None:
      return "func_code_" + self.currFunc
    else:
      return "func_code_" + func  


  def _generateFunctionRetLabel(self) -> str:
    return "func_ret_" + self.currFunc