# Week 4 — Level 1: Three-Address Code and MIPS Code Generation

## What is "Level 1" of TinyCStr?

**Level 1** of TinyCStr contains a basic set of language features. Each subsequent level builds on the previous level by adding new language features.

At Level 1, TinyCStr supports:

- A single `int main(){ ... }` function
- `int` variable declarations
- Integer constants
- Assignment statements
- `print` statements
- Arithmetic operators: `+`, `-`, `*`, `/`, `%`

The compiler will gradually support these features through different stages:

```text
Level 1
  ├── Week 2 → Lexer
  ├── Week 3 → Parser + AST
  └── Week 4 → Three-Address Code + MIPS
```

By the end of Week 4, the complete Level 1 compiler will be able to process a TinyCStr program from source code to executable MIPS code.

This week completes the Level 1 compiler pipeline:

```text
Source Program
      ↓
    Lexer
      ↓
    Parser
      ↓
     AST
      ↓
Three-Address Code
      ↓
    MIPS
      ↓
   Execution
```

---

## What are we building?

In Week 3, the parser produced an Abstract Syntax Tree (AST).  
This week we use that AST to generate:

1. **Three-Address Code (TAC)** as an intermediate representation.
2. **MIPS assembly code** from the TAC.

The complete flow is:

```text
AST
 ↓
TAC / Triples
 ↓
MIPS Assembly
 ↓
SPIM Execution
```

This introduces two important compiler concepts:
- **Intermediate Code Generation**
- **Target Code Generation**

---

### Why do we need Three-Address Code?

Consider:

```c
x = a + b * c;
```

The AST represents the structure of the expression, but it is not yet convenient for generating machine instructions.  
We can first convert it into simpler intermediate instructions:

```text
t1 = b * c
t2 = a + t1
x = t2
```

Each instruction performs a simple operation.  
This is called **Three-Address Code (TAC)**.  
TAC provides an intermediate step between the AST and the target machine code.

```text
AST → Three-Address Code → MIPS
```

---

### Why are we using Triples?

There are different ways to represent Three-Address Code.  
One common representation is **quadruples**:

```text
(operator, argument1, argument2, result)
```

For `x = a + b * c`, we could write:

```text
0: ( *, b,  c,  t1 )
1: ( +, a,  t1, t2 )
2: ( =, t2, -,  x  )
```

**Triples** remove the explicit result field.  
Instead, the result of a triple is identified by its position:

```text
0: ( *, b,    c   )
1: ( +, a,    (0) )
2: ( =, (1),  x   )
```

Here:
- `(0)` means the result produced by triple 0.
- `(1)` means the result produced by triple 1.

Therefore, explicit temporary names such as `t1` and `t2` are not required.

---

## What are we trying to do this week?

The goal is to complete the Level 1 compiler by implementing:

### Part 1 — AST → Three-Address Code
Traverse the AST and generate triples for:
- Arithmetic expressions
- Assignment statements
- `print` statements

For example, `x = a + b * c;` should produce triples similar to:

```text
0: ( *, b,    c   )
1: ( +, a,    (0) )
2: ( =, (1),  x   )
```

### Part 2 — Three-Address Code → MIPS
Translate each triple into one or more MIPS instructions.

For example, `(0) * b, c` can be translated conceptually into:

```assembly
lw  $t0, <address-of-b>
lw  $t1, <address-of-c>
mul $t2, $t0, $t1
```

The result of triple 0 is now available in `$t2`.  
A later triple referring to `(0)` can therefore use `$t2`.

---

### Register Allocation

MIPS operations use registers. For example:

```assembly
add $t2, $t0, $t1
```

means `$t2 = $t0 + $t1`.

The code generator therefore needs to keep track of where values are stored:
- Triple 0 → `$t2`
- Triple 1 → `$t3`
- Triple 2 → `$t4`

If a later triple contains `(0)`, the code generator can resolve it to `$t2`.  
This week uses a simple register allocation strategy suitable for understanding the basic idea.

---

### Memory and Stack Frames

Variables need memory locations.  
The compiler uses the symbol table to assign offsets to variables in the function's stack frame.

Conceptually:

| Variable | Offset |
|---|---|
| `a` | `4($fp)` |
| `b` | `8($fp)` |
| `c` | `12($fp)` |
| `x` | `16($fp)` |

A variable can then be loaded using:

```assembly
lw $t0, 4($fp)
```

and stored using:

```assembly
sw $t1, 16($fp)
```

The stack frame provides a structured way to organize the memory used by the function.  
This is an important step toward understanding activation records and run-time memory organization.

---


## What do you need to do?

There are three main implementation tasks:

### 1. Generate Three-Address Code
Complete `tac_generator.py` by implementing the TODOs in:
- `gen_stmt()`
- `gen_expr()`

The generator should traverse the AST and produce triples.

### 2. Connect Function Compilation
Complete `Function.py`. The `compile()` method should:
1. Assign offsets to symbols.
2. Construct the MIPS generator.
3. Generate MIPS code.
4. Store the generated code for later output.

```text
Function → assignOffsetsToSymbols() → MIPSGenerator → generate() → MIPS code
```

### 3. Generate MIPS Code
Complete `tac_to_mips.py` by implementing:
- `resolve_address()`
- `load()`
- `store()`
- `gen_instr()`

These functions connect the intermediate representation to MIPS instructions.

---

Builds directly on practice examples 4 and 5.
## What's already provided (do not modify)

- `tinycstr_lexer.py`, `tinycstr_parser.py`, `ast_nodes.py` — unchanged.
- `SymbolTable.py` — `assignOffsetsToSymbols()`, `getSizeOfType()`, and
  `size()` fully implemented.
- `Program.py` — `Program.compile()` already just loops calling
  `function.compile()` for every function.
- `three_address_code.py` — the triple IR (`BinOpTriple`, `AssignTriple`, `PrintTriple`,
  `TripleRef`, `TripleTAC`).
- `main.py` — compile option flow `parse` →
  `program.generateTripleTAC()` → `program.compile()` → `func.getMipsCode()`.

## What you need to do

- `tac_generator.py` —  TODOs — `gen_stmt()`,`gen_expr()` 
- `Function.py` —  `compile()` : call `assignOffsetsToSymbols()`, construct a `MIPSGenerator`, call `generate()`, store the result.
- `tac_to_mips.py` — TODOs: `resolve_address()`, `load()`, `store()`,
  `gen_instr()`. 

## What's provided to help you

- `docs/register_allocation_reference.md` — exactly how this week's `tac_to_mips.py` differs
  from the practice example (real offsets, `PrintTriple`, prologue/epilogue), a full worked
  register-allocation trace for the precedence take-home program
- `docs/mips_spim_reference.md` — the Frame-based Linkage Convention mapped to actual MIPS,
  including why no explicit exit syscall is needed (verified on real SPIM).
- `tests/` — three `.tc` programs with exact golden triple-form `.3ac`, register-allocated
  frame-based `.s`, and expected SPIM console output — **every one of these was actually run on
  real SPIM** to generate.

## Step by step

1. Read `docs/register_allocation_reference.md` and the practice example it builds on.
2. Implement TODOs in `Function.py`, `tac_generate.py`,`tac_to_mips.py`
4. Test the full pipeline:
   ```bash
   python main.py -3ac -compile tests/test1.tc
   diff tests/test1.tc.3ac tests/test1.3ac.expected.txt
   diff tests/test1.tc.spim tests/test1.s.expected.txt
   ```
5. **Actually run it on SPIM** — a diff-matching `.s` is not the finish line:
   ```bash
   spim -file tests/test1.tc.spim
   ```
6. Take-home: 5 additional TinyCStr(L1) programs exercising all four operators, run through the
   full pipeline, actual SPIM console output included in your report.


---

## Step by step

### Step 1 — Understand the AST → TAC transformation
Start with `practice_examples/4_practice_examples_threeaddress_triple/`.

For example, for `x = a + b * c;`, the AST:

```text
        =
       /       x   +
         /         a   *
           /           b   c
```

is traversed bottom-up:
1. First: `(0) * b, c`
2. Then: `(1) + a, (0)`
3. Finally: `(2) = (1), x`

> **Key Concept:** The index of a triple identifies the result produced by that triple.

### Step 2 — Implement `gen_expr()`
Complete `tac_generator.py`. Start with expression nodes such as `Num`, `Var`, and `BinOp`.

For a binary operation:
1. Generate code for the left child.
2. Generate code for the right child.
3. Create a new `BinOpTriple`.
4. Return a reference to the newly created triple.

```text
           BinOp(+)
          /               left       right
        ↓           ↓
     triple       triple
        \           /
         \         /
          new triple
```

### Step 3 — Implement `gen_stmt()`
Handle statements such as Assignment and Print.

For example, `x = a + b;` should generate the expression first:

```text
(0) + a, b
```

and then generate an assignment:

```text
(1) = (0), x
```

### Step 4 — Test the TAC
Run:

```bash
python3 main.py -3ac tests/test1.tc
```

Check the generated `.3ac` file against the expected output. The triple output should have the correct operator, operands, triple references, and ordering.

### Step 5 — Understand Triple → MIPS
Study `practice_examples/5_practice_examples_MIPS/`.

Suppose the triples are:

```text
0: ( *, b,    c   )
1: ( +, a,    (0) )
2: ( =, (1),  x   )
```

The code generator might maintain `Triple 0 → $t2`. After generating `0: ( *, b, c )`, when it sees `(0)` in triple 1, it knows that the value is currently in `$t2`.

### Step 6 — Implement loading and storing
Complete `load()` and `store()` in `tac_to_mips.py`.

A constant such as `10` can be loaded using:

```assembly
li $t0, 10
```

A variable must be loaded from its stack-frame location:

```assembly
lw $t0, 4($fp)
```

Similarly, a result must eventually be stored:

```assembly
sw $t0, 16($fp)
```

### Step 7 — Implement `gen_instr()`
Complete `gen_instr()`. It should translate triples into appropriate MIPS instructions.

For example, `(0) + a, b` may result in:

```assembly
lw  $t0, 4($fp)
lw  $t1, 8($fp)
add $t2, $t0, $t1
```

*(The exact registers depend on the allocation strategy.)*

### Step 8 — Implement `Function.compile()`
Complete the function-level compilation process in `Function.py`:

```text
Function → assignOffsetsToSymbols() → create MIPSGenerator → generate MIPS → store generated code
```

### Step 9 — Run the complete pipeline
Run:

```bash
python3 main.py -3ac -compile tests/test1.tc
```

Then compare the generated files with the expected output provided in `tests/`.

### Step 10 — Actually run the generated code
A compiler is not complete just because the generated assembly looks correct. Run the generated MIPS program using SPIM:

```bash
spim -file tests/test1.tc.spim
```

Check the actual output against the expected output.

```text
TinyCStr Source → AST → Triples → MIPS → SPIM → Correct Output
```

---

## A complete example

Consider:

```c
x = (a + b) * (c - d);
```

### AST
```text
             =
           /             x     *
               /               +   -
             / \ /             a  b c  d
```

### Three-Address Code
```text
t1 = a + b
t2 = c - d
t3 = t1 * t2
x = t3
```

### Triple representation
```text
0: ( +, a,    b    )
1: ( -, c,    d    )
2: ( *, (0),  (1)  )
3: ( =, (2),  x    )
```

### MIPS generation (Conceptual)
```assembly
lw  $t0, <address-of-a>
lw  $t1, <address-of-b>
add $t2, $t0, $t1

lw  $t0, <address-of-c>
lw  $t1, <address-of-d>
sub $t3, $t0, $t1

mul $t4, $t2, $t3

sw  $t4, <address-of-x>
```

*(The actual variable addresses are determined by the symbol-table offsets.)*

---

## Testing

The `tests/` directory contains programs with expected results across all compilation stages:

```text
Source → AST → 3AC / Triples → MIPS → SPIM Output
```

For each test:

1. **Generate triples:**
   ```bash
   python3 main.py -3ac tests/test1.tc
   ```
2. **Generate MIPS:**
   ```bash
   python3 main.py -compile tests/test1.tc
   ```
3. **Compare generated files:**  
   Compare the generated `.3ac` and `.s` files with their corresponding expected files in `tests/`.
4. **Run with SPIM:**
   ```bash
   spim -file tests/test1.tc.spim
   ```

Do not consider the test complete until the actual SPIM output is correct.

---

## Take-home work

Write **5 additional Level 1 TinyCStr programs**. Your programs should collectively exercise:
- Integer declarations
- Assignments
- Print statements
- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Division (`/`)
- Remainder (`%`)
- Combinations of operators

For each program:
1. Generate the triples.
2. Generate MIPS code.
3. Run the generated program using SPIM.
4. Record the actual output.
5. Include the source program, triples, MIPS code, and SPIM output in your report.

At least one program should contain a compound expression such as:

```c
x = (a + b) * (c - d) + e;
```

so that you can verify AST structure, triple references, register allocation, generated MIPS, and final output.

---

## What you should understand by the end of Week 4

You should be able to explain:
- Why compilers use an intermediate representation
- What Three-Address Code is
- The difference between quadruples and triples
- How an AST can be traversed to generate TAC
- How triple indices represent intermediate results
- How triple references are resolved during code generation
- How variables and constants are loaded
- How values are stored back into memory
- What a stack frame is and why a compiler assigns offsets to variables
- What register allocation means and how registers can be reused
- How TAC instructions are translated into MIPS instructions
- How to test generated assembly using SPIM
- The complete flow from source code to executable target code

---

## Level 1 compiler — completed

At the end of Week 4, you have built a complete compiler pipeline for Level 1 TinyCStr:

```text
TinyCStr Source
       │
       ▼
    Lexer
       │
       ▼
    Parser
       │
       ▼
      AST
       │
       ▼
Three-Address Code (Triples)
       │
       ▼
MIPS Code Generator
       │
       ▼
 MIPS Assembly
       │
       ▼
     SPIM
       │
       ▼
 Program Output
```

This completes the first end-to-end TinyCStr compiler level. The next level will add new language features while reusing and extending the compiler infrastructure developed here.

---


## Getting unstuck

If you're still stuck, post in the Week 4 GitHub Issues thread  





