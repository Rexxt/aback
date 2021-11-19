# Aback - a FORTH-like programming language
Aback is a FORTH-like programming language - it uses words as an instruction sequence and its data is stack-based.
Here is an example of Aback:
```aback
main: /* define function main */
" Hello, world! " print /* push Hello, world! to the stack, print it and drop it. */
;; /* end def */
main
```