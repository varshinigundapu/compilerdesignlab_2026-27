# Week 4 — Three-Address Code (Triples) and Frame-Based, Register-Allocated MIPS/SPIM

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

## Getting unstuck

If you're still stuck, post in the Week 4 GitHub Issues thread 