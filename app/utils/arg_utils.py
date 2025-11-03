from typing import List

def process_args(input: str) -> List[str]:
    """
    proccesses arguments to handle quotes and escapes.
    """
    args = []
    in_single_quote = False
    in_double_quote = False

    current = ""

    for c in input:

        if c == '"':
            if in_single_quote:
                current += '"'
            else:
                in_double_quote = not in_double_quote
        elif c == "'":
            if in_double_quote:
                current += "'"
            else:
                in_single_quote = not in_single_quote
        elif c == " ":
            if in_single_quote or in_double_quote:
                current += " "
            elif current:
                args.append(current)
                current = ""
        else:
            current += c

    if current:
        args.append(current)        
    return args