if exists("b:current_syntax")
  finish
endif

syntax match folder "+.*/"
" syntax keyword folder ems2
highlight link folder Keyword

let b:current_syntax = "vim_tc_explorer"
