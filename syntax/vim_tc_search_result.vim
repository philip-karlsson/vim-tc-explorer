if exists("b:current_syntax")
  finish
endif

syntax match group "-->"
syntax match commands "<Ret>"
syntax match commands "<C-q>"

syntax match group "+.*"
syntax match file "*.*"
syntax match path "$>.*$"

highlight link group Keyword
highlight link path Debug
highlight link file Debug

let b:current_syntax = "vim_tc_explorer"

