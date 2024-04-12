# reserves dictionary
control = {
    'is': "cont_is",
    'else': "cont_else",
    'iselse': "cont_iselse",
    'for': "cont_for",
    'while': "cont_while",
    'countup': "cont_up",
    'countdown': "cont_down",
    'to': "cont_to"
}
io = {
    'show': "io_out",
    'ask': "io_inp"
}
value = {
    'true': "val_true",
    'false': "val_false",
}
datatype = {
    'wholenum': "dt_wn",
    'decimalnum': "dt_dn",
    'text': "dt_text",
    'bool': "dt_bool",
    'wholenumber': "dt_wn",
    'decimalnumber': "dt_dn",
    'boolean': "dt_bool"
}
show = {
    'showsquare': "show_sq",
    'showrectangle': "show_re",
    'showtriangle': "show_tr"
}
perimeter = {
    'perisquare': "per_sq",
    'perirectangle': "per_re",
    'peritriangle': "per_tr"
}
area = {
    'arsquare': "ar_sq",
    'arrectangle': "ar_re",
    'artriangle': "ar_tr"
}
function = {
    'add': "func_add",
    'sub': "func_sub",
    'multi': "func_multi",
    'cond': "func_cond"
}

# combining reserves dictionary
reserves = {}
reserves.update(control)
reserves.update(function)
reserves.update(show)
reserves.update(perimeter)
reserves.update(area)
reserves.update(io)
reserves.update(value)
reserves.update(datatype)

# reserves key list
reserves_key = reserves.keys()