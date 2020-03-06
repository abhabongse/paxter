"""
PEG parser for Paxter language.
"""
from parsimonious.grammar import Grammar

grammar = Grammar(r"""
    start               = fragments ~r"\Z"
    fragments           = ( non_greedy_text paxter_node )* non_greedy_text
    paxter_node         = "@" ( paxter_macro / paxter_func / paxter_phrase / paxter_string )
    paxter_macro        = macro_id wrapped_text
    paxter_func         = normal_id wrapped_fragments
    paxter_phrase       = normal_id / wrapped_text
    paxter_string       = wrapped_string
    wrapped_text        = ( "#" wrapped_text "#" ) / ( "<" wrapped_text ">" ) / ( "{" non_greedy_text "}" )
    wrapped_string      = ( "#" wrapped_string "#" ) / ( "<" wrapped_string ">" ) / ( "\"" non_greedy_text "\"" ) 
    wrapped_fragments   = ( "#" wrapped_fragments "#" ) / ( "<" wrapped_fragments ">" ) / ( "{" fragments "}" ) 
    
    normal_id       = ~r"\w+"
    macro_id        = ~r"\w*!"
    non_greedy_text = ~r".*?"
""")

