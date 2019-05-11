from lark import Lark          # pip install lark-parser
from lark import Transformer


class MarteConfigParser:
    """Class created for parsing MARTe configs. Use parse_config method."""
    def __init__(self):
        self.marte_parser = Lark(r"""
            ?value: number
                  | string
                  | pair
                  | dict
                  | list

            pair : literal "=" value

            // list cannot contain sub-terminals
            list : "{" literal " " literal "}"
            dict : "{" [pair ("\n"? pair)*] "}"

            LETTER_DEF: "a".."z" | "A".."Z"
            NUMBER_DEF: "0".."9"
            // string cannot start with number
            WORD: LETTER_DEF (LETTER_DEF|NUMBER_DEF)+
            string : WORD

            number: SIGNED_NUMBER

            ?literal: number | string

            %import common.SIGNED_NUMBER
            %import common.WS_INLINE
            %import common.WS
            %ignore WS

            COMMENT: "//" /[^\n]/*           // single-line comment
                   | "/*" /(.|\n|\r)+/ "*/"  // multi-line comment
            %ignore COMMENT

            """, start='value')
        
    class TreeToPython(Transformer):
        def string(self, s):
            return str(s[0])
        def number(self, n):
            value = None
            try:
                value = int(n[0])
            except ValueError:
                value = float(n[0])
            return value

        list = list
        pair = tuple
        dict = dict

    def parse_config(self, config_text):
        config_text = "{" + config_text + "}"
        
        tree = self.marte_parser.parse(config_text)
        out = self.TreeToPython().transform(tree)
        
        return out