# operators dictionary
arithmetic = {
    '*': "ar_mul",
    '/': "ar_div",
    '%': "ar_mod",
    '//': "ar_indiv"
}
assignment = {
    '=': "assi_eq",
    '+=': "assi_add",
    '-=': "assi_sub",
    '*=': "assi_mul",
    '/=': "assi_div",
    '%=': "assi_mod",
    '//=': "assi_indiv"
}
unary = {
    '++': "unar_inc",
    '--': "unar_dec"
}
logical = {
    '!': "log_not",
    '||': "log_or",
    '&&': "log_and"
}
relational = {
    '==': "rel_eq",
    '!=': "rel_noteq",
    '>': "rel_great",
    '<': "rel_less",
    '>=': "rel_greateq",
    '<=': "rel_lesseq"
}
twoop = {
    '+': "pos_add",
    '-': "neg_sub"
}

# combining operators dictionary
operators = {}
operators.update(arithmetic)
operators.update(assignment)
operators.update(unary)
operators.update(logical)
operators.update(relational)
operators.update(twoop)

# operators key list
operators_key = operators.keys()