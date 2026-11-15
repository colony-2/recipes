# Native document presentation byte references

`presentation-bytes.json` records compact Go `encoding/json` lengths from c2j
commit `d031eb49c6777555cca1f58449b8451b1fc77c37`, using the exact
`DocumentMetadata` and `reviewDocumentPresentation` definitions from
`pkg/input/document_metadata.go`. Go 1.26.8 produced these references.

The escaped case includes quotes, a backslash, `<>&`, U+2028/U+2029, an emoji,
a multibyte attachment ID and explicit zero order. The empty case marshals to
`{}`. Boundary cases use 180 IDs `review/d000.txt` through `review/d179.txt`,
title `Decision`, explicit zero order, the first role primary and the remaining
roles supporting. Each description repeats `x` according to the stored lengths.
The overview is `review/d000.txt`. Native typed marshaling yields exactly 65536
and 65537 bytes, while each descriptor stays within its own bounds.

The direct test executes the authored checker and compares its measured bytes
with these native references. It does not compute expected lengths with the
recipe's encoder. Empty native maps omit the field, and zero order remains
present because the native type uses an integer pointer.
