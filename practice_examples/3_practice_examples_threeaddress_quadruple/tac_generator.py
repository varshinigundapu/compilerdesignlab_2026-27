"""
AST to Three-Address Code generator.

  - Var(name)  -> return the name directly. No instruction emitted --
                  reading a variable doesn't require computing anything.
  - Num(value) -> return str(value) directly. No instruction emitted --
                  a literal is already a value, it doesn't need a
                  temporary just to exist.
  - BinOp(op, left, right) -> recursively get the left and right
                  operands (each may or may not have emitted
                  instructions as a side effect), allocate ONE new
                  temporary, emit ONE BinOpTAC combining the two
                  operands into it, and return the new temporary's name.
  - Assign(var, expr) -> get the expr's result operand, emit ONE CopyTAC
                  assigning it into var.name.
"""
from ast_nodes import Num, Var, Assign, BinOp
from three_address_code import BinOpTAC, CopyTAC


class TACGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0

    def new_temp(self):
        """
        return a fresh temporary name, "t1", "t2", ... --
        one counter per TACGenerator instance 
        """
        self.temp_counter = self.temp_counter + 1
        return "t" + str(self.temp_counter)


    def addInstruction(self, instruction):
        """just appends to the flat instruction list."""
        self.instructions.append(instruction)


    def gen_stmt(self, stmt):
        operand = self.gen_expr(stmt.expr)
        self.addInstruction(CopyTAC(stmt.var.name, operand))
        return self.instructions

    def gen_expr(self, node):
        """
        Note the order: fully resolve both operands (which may themselves
        recursively emit instructions for nested BinOps) BEFORE emitting
        this node's own instruction -- otherwise instructions come out in
        the wrong order.
        """
        if isinstance(node, Num):
            return str(node.value)    # no instruction emitted
        if isinstance(node, Var):
            return node.name          # no instruction emitted
        if isinstance(node, BinOp):
            left_operand  = self.gen_expr(node.left)
            right_operand = self.gen_expr(node.right)
            dest = self.new_temp()
            self.addInstruction(BinOpTAC(dest, node.op, left_operand, right_operand))
            return dest


def generate_for_statement(stmt):
    """wrapper: generate() a fresh TACGenerator for every statement"""
    return TACGenerator().gen_stmt(stmt)
