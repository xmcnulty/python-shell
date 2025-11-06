from typing import List

def process_args(input: str) -> List[str]:
    """
    Processes arguments similar to Bash word splitting.
    Handles quotes, escapes, and line continuations.
    """
    args = []
    in_single_quote = False
    in_double_quote = False
    current = ""
    i = 0
    n = len(input)

    while i < n:
        c = input[i]

        if c == "\\":
            # handle line continuation
            if i + 1 < n and input[i + 1] == "\n":
                i += 2
                continue  # skip both
            if in_single_quote:
                current += "\\"
            elif in_double_quote:
                # only certain escapes allowed
                if i + 1 < n and input[i + 1] in ['\\', '"', '$', '`']:
                    current += input[i + 1]
                    i += 1
                else:
                    current += "\\"
            else:
                # outside quotes: always escapes next char
                if i + 1 < n:
                    current += input[i + 1]
                    i += 1
        elif c == "'":
            if in_double_quote:
                current += "'"
            else:
                in_single_quote = not in_single_quote
        elif c == '"':
            if in_single_quote:
                current += '"'
            else:
                in_double_quote = not in_double_quote
        elif c.isspace():
            if in_single_quote or in_double_quote:
                current += c
            elif current:
                args.append(current)
                current = ""
        else:
            current += c

        i += 1

    if current:
        args.append(current)

    return args