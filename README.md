# Aback - a FORTH-like programming language
Aback is a FORTH-like programming language - it uses words as an instruction sequence and its data is stack-based.
Here is an example of Aback:
```aback
main: /* define function main */
    " Hello, world! " print /* push Hello, world! to the stack, print it and drop it. */
;; /* end def */
main

0 $x
x dup /* push the value of x to the stack twice */
print /* print the first occurence */
1 + $x /* , and increase the other by one and push it back into x */
x print /* and finally show it to the screen */
```
## Supported features
* Function definition
* Basic math operations (+, -, *, /)
* Comments
* Booleans
* Null
* Variables
* exit word
* Module import
## Planned features
* Arrays
* If, while, for
* Python modules?