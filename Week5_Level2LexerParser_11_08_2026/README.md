# Week 5 — Level 2 Lexer + Parser (Stages 2a → 2c)

## What's already provided (do not modify)

- `ast_nodes.py` — **changed this week** (flagged in the file): `RelOp`, `Cast`, `Ternary`
  added, fully implemented. `Var`/`Assign`/`Print`/`BinOp` unchanged — note `Num` is discontinued, `Const` used as a generic constant holder for every constant kind (int/double/char/string).
- `SymbolTable.py` — **changed this week**: `DataType` now includes `DOUBLE`, `CHAR`, `STRING`.
  `getSizeOfType()` to handle size of all types.
- `Function.py`, `Program.py`, `three_address_code.py`, `tac_to_mips.py` — unchanged from Week 4.
- `tac_generator.py` — logic unchanged , but **fixes the ast node use `Const` instead of `Num`
- `main.py` — **changed this week**: `-3ac`/`-compile` now catch any exception from
  unimplemented Level 2 codegen . `-tokens`/`-ast`/`-parse` are untouched and fully work on Level 2 programs.

## What you need to do

- `tinycstr_lexer.py` — Level 1 rules are complete and marked "do not modify." Your work is the
  three staged Level 2 sections: `DOUBLE`/`REAL_CONST` (2a), `CHAR`/`STRING`/`CHAR_CONST`/`STRING_CONST`/
  six relational operators (2b), `QUESTION`/`COLON` (2c).
- `tinycstr_parser.py` — same structure: Level 1 grammar complete and marked "do not modify."
  Your TODOs are staged 2a → 2b → 2c, ending with the trickiest part of the week — casts and
  ternary need real precedence work, not just new grammar rules.

## What's provided to help you

- `docs/level2_token_reference.md` — the exact Level 2 token/grammar additions per stage, why
  `Num` is discontinued and `Const` for every literal kind
- `docs/sly_help2.md` — the two genuinely tricky mechanics this week: relational/
  ternary precedence ordering, and the `%prec` idiom casts need (a plain precedence entry isn't
  enough on its own). 
- `tests/` — three `.tc` programs (one per stage) with exact golden tokens/AST — plus one golden
  3AC file for the Stage 2a program specifically, since it's the only stage whose output doesn't
  hit a still-unimplemented codegen path.

## Step by step

1. Read `docs/level2_token_reference.md` fully before writing any code.
2. Implement Stage 2a's lexer + parser TODOs. Test:
   ```bash
   python main.py -tokens -ast tests/test4.tc
   diff tests/test4.tc.toks tests/test4.toks.expected.txt
   diff tests/test4.tc.ast tests/test4.ast.expected.txt
   ```
   If your Week 4 `tac_generator.py` TODOs are already done, also check:
   ```bash
   python main.py -3ac tests/test4.tc
   diff tests/test4.tc.3ac tests/test4.3ac.expected.txt
   ```
3. Implement Stage 2b. Test against `tests/test5.tc` the same way (tokens/AST only)

4. Read `docs/sly_help2.md` 5 carefully before starting Stage 2c — casts are the
   trickiest grammar work in the whole course so far.
5. Implement Stage 2c. Test against `tests/test6.tc` (the corrected Example 3). Specifically
   verify the AST shows `Cast` wrapping only the immediately-following operand, not a whole
   division — that's the one mistake that doesn't show up as a syntax error.
6. Take-home: write 5 TinyCStr(L2) programs — one per sub-stage, plus one combining all of them
   with at least one nested ternary and one chained cast — and produce their ASTs.

## Getting unstuck

If you're still stuck, post in the Week 5 GitHub Issues.
