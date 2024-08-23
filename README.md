# MacroScript Wrapper (MSW)

This is a LISP-like language that compiles to [Robot is Chill's](https://github.com/balt-dev/robot-is-chill) macro language called MacroScript.

## Example

```clj
[(*define +    (add *1 *2))
 (*define ^    (pow *1 *2))
 (*define $    (load *1))
 (*define =    (store *1 *2))
 (*define loop (unescape (repeat *1 '[*2])))
 (= i 0)
 (loop 10
   [(= i (+ ($ i) 1))
    (int (^ ($ i) 2))
    " "])]
```
Compiles to:
```
[store/i/0][unescape/[repeat/10/\[store\/i\/\[add\/\[load\/i\]\/1\]\]\[int\/\[pow\/\[load\/i\]\/2\]\] ]]
```
Outputs:
```
1 4 9 16 25 36 49 64 81 100 
```

(For some more scripts, see the [examples/](examples/) directory.)

## Language

Even though it's not quite LISP, it's similar in syntax as it uses [S-expressions](https://en.wikipedia.org/wiki/S-expression).

* Symbols, strings, integers and floats are equivalent and converted to strings.
* Parentheses run macros: `(f "x" y)` returns `[f/x/y]`.
* Brackets concatenate everything inside: `[(f x) a b " "]` returns `[f/x]ab `.
* Putting quotes before expressions escape `[`, `/` and `]` with backslashes. This can be nested further: `'[a b '[c d] e f]` returns `\[a\/b\]\\\[c\\\/d\\\]\[e\/f\]`.

### Metamacros with `*define`

TODO