# import files with dictonaries
import delimiters
import reserves
import operators

# create collector variable for lexical analyzer
out = ""

# create collector variable for syntax analyzer
tok = []

# reset the tokenization
def reset():
    global out
    global tok
    out = ""
    lex = "Lexemes"
    out += lex.ljust(30) + "Tokens" + "\n"
    tok = []

# count the lines
def line_counter(x):
    global out
    global tok

    out += x + "\n"
    tok.append((x, "line_counter"))

# tokenized comment
def lex_comment(x):
    global out
    global tok

    out += x.ljust(30) + "comment" + "\n"
    tok.append((x, "comment"))

# tokenized unterminated text
def lex_error_text(x):
    global out
    global tok

    x = "[]"
    out += x.ljust(30) + "unterminated_text" + "\n"
    tok.append((x, "unterminated_text"))

# tokenized invalid identifier
def lex_error_identifier(x):
    global out
    global tok

    out += x.ljust(30) + "invalid_identifier" + "\n"
    tok.append((x, "invalid_identifier"))

# tokenized value text
def lex_text(x):
    global out
    global tok

    out += x.ljust(30) + "val_text" + "\n"
    tok.append((x, "val_text"))

# tokenized value number
def lex_number(x):
    global out
    global tok

    try:
        con = float(x)
        if con.is_integer():
            out += x.ljust(30) + "val_whole" + "\n"
            tok.append((x, "val_whole"))
        else:
            out += x.ljust(30) + "val_decimal" + "\n"
            tok.append((x, "val_decimal"))
    except ValueError:
        identifier_check(x)

# tokenized reserved word
def lex_reserve(x):
    global out
    global tok

    if x in reserves.reserves_key:
        out += x.ljust(30) + reserves.reserves[x] + "\n"
        tok.append((x, reserves.reserves[x]))
    else:
        identifier_check(x)

# tokenized delimiter or operator
def lex_delimoper(x):
    global out
    global tok

    if x in delimiters.delimiters_key:
        out += x.ljust(30) + delimiters.delimiters[x] + "\n"
        tok.append((x, delimiters.delimiters[x]))
    elif x in operators.operators_key:
        out += x.ljust(30) + operators.operators[x] + "\n"
        tok.append((x, operators.operators[x]))
    else:
        token_err(x)

# check if identifier is valid or invalid
def identifier_check(x):
    global out
    global tok

    if x.isalpha():
        out += x.ljust(30) + "identifier" + "\n"
        tok.append((x, "identifier"))
    else:
        out += x.ljust(30) + "invalid_identifier" + "\n"
        tok.append((x, "invalid_identifier"))

# tokenized invalid token
def token_err(x):
    global out
    global tok

    out += x.ljust(30) + "invalid_token" + "\n"
    tok.append((x, "invalid_token"))

# tokenized unterminated comment
def comm_err():
    global out
    global tok

    x = ""

    out += x.ljust(30) + "unterminated_comment" + "\n"
    tok.append((x, "unterminated_comment"))

    return result()

# return collected output for lexical
def result():
    return out

# return collected output for syntax
def syntax():
    return tok