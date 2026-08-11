"""
Three-address code (3AC) -- TRIPLE representation. 

A "quadruple" representation of three address code IR 
(where every binary operation invents an explicit named temporary, e.g. `t1 = a + b`): 
a TRIPLE never names its own result. Instead, each triple is numbered by its position
in the program (0, 1, 2, ...), and any LATER triple that needs an earlier one's result refers 
to it by that index -- written as "(i)" in text form. For example, `d = a + b*c;` becomes:

    (0) * b, c
    (1) + a, (0)
    (2) c = (1)

A temporary's identity is just its position in the instruction
list, so it never needs a name and therefore never needs a
SymbolTable entry -- only genuinely declared source variables (a, b, c)
do.

Three triple class each a small class with a render() method 

    BinOpTriple(op, arg1, arg2)   -- op in {'+','-','*','/'}. Its OWN
                                   result is referred to by later triples
                                   as TripleRef(this triple's index).
    AssignTriple(dest, arg1)   -- dest is always a real declared
                                   variable NAME (a plain string) -- the
                                   only triple shape that writes to a
                                   named variable rather than producing
                                   an anonymous, index-addressed result.

`arg1`/`arg2` are always one of:
    - a plain variable name (string, e.g. "a")
    - a literal integer written as a digit string (e.g. "5")
    - a TripleRef(i), pointing at an earlier triple's result

Use TripleProgram to build a program -- its append() sets each
triple's `.index` automatically and hands back a ready-to-use TripleRef,
which is exactly what tac_generator.py's gen_expr() needs for a BinOp.
"""


class TripleRef:
    """A reference to an earlier triple's result, by its index."""

    def __init__(self, index):
        self.index = index

    def render(self):
        return f"({self.index})"

    def __eq__(self, other):
        return isinstance(other, TripleRef) and self.index == other.index

    def __repr__(self):
        return f"TripleRef({self.index})"


def render_operand(operand):
    """Renders a plain name/literal string, or a TripleRef, to text."""
    if isinstance(operand, TripleRef):
        return operand.render()
    return str(operand)


def is_literal(operand):
    """
    True if `operand` is a literal integer (as a string) rather than a
    variable name or a TripleRef. 
    """
    return isinstance(operand, str) and operand.isdigit()


class BinOpTriple:
    def __init__(self, op, arg1, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.index = None  # set by TripleProgram.append()

    def render(self):
        return f"({self.index}) {self.op} {render_operand(self.arg1)}, {render_operand(self.arg2)}"


class AssignTriple:
    def __init__(self, dest, arg1):
        self.dest = dest
        self.arg1 = arg1
        self.index = None

    def render(self):
        return f"({self.index}) {self.dest} = {render_operand(self.arg1)}"




class TripleProgram:
    """
    A flat, ordered list of triples, with automatic
    index assignment.
    """

    def __init__(self):
        self.triples = []

    def append(self, triple):
        """
        Sets `triple.index` with its position in the program and
        returns a TripleRef pointing at it -- the gen_expr()
        usually wants that ref immediately after appending.
        """
        triple.index = len(self.triples)
        self.triples.append(triple)
        return TripleRef(triple.index)

    def render(self):
        return "\n".join(t.render() for t in self.triples)

    def __len__(self):
        return len(self.triples)

    def __iter__(self):
        return iter(self.triples)

def render_threeAddressCode(tripleprogram):
    """
    Text form of a flat list of TAC instructions, one per line 
    """
    return tripleprogram.render()
