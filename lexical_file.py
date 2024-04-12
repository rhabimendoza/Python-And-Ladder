# import recognizer file
import recognizer

# define lexical function
def lexical_function(inp):

    # reset the tokenization variable in recognizer file
    recognizer.reset()

    # set error checker to 0
    error = 0

    # set comment checker to 0
    comment = 0

    # set comment collector to empty
    com = ""

    # split input line by line
    lines = inp.split("\n")

    # iterate through lines
    for y, line in enumerate(lines):

        # output line count
        count = "Line count: " + str(y + 1)
        recognizer.line_counter(count)

        # set index checker to 0
        ind = 0

        # iterate through characters
        for i, ch in enumerate(line):

            # start of comment
            if ch == '[':
                comment = 1
                com += ch
                continue
            
            # end of comment
            if comment == 1 and ch == ']':
                comment = 0
                com += ch
                recognizer.lex_comment(com)
                com = ""
                continue

            # comment contents
            if comment == 1:
                com += ch
                continue
            
            # skip tokenized characters
            if ind > 0:
                ind = ind - 1
                continue

            # skip spaces
            if ch == ' ':
                continue

            # text
            if ch == '"':

                recognizer.lex_delimoper(ch)

                ind = i + 1

                if ind >= len(line):
                    recognizer.lex_error_text(" ")
                else:
                    err = 0

                    word = " "

                    while ind < len(line):
                        try:
                            if line[ind] == '"':
                                break
                            word = word + line[ind]
                            ind = ind + 1
                            if line[ind] == '"':
                                break
                        except IndexError:
                            recognizer.lex_error_text(" ")
                            err = 1

                    if(err != 1):
                        ind = ind - i

                        recognizer.lex_text(word)

                        recognizer.lex_delimoper(ch)

            # words
            elif ch.isalpha():
                err = 0

                word = ""
                word = word + ch

                ind = i + 1

                if(ind < len(line) and line[ind].isnumeric()):
                    err = 1

                while (ind < len(line)) and (line[ind].isalpha() or line[ind].isnumeric()):
                    word = word + line[ind]
                    if(ind < len(line) and line[ind].isnumeric()):
                        err = 1
                    ind = ind + 1 

                ind = ind - i - 1

                if(err == 1):
                    recognizer.lex_error_identifier(word)
                else:
                    recognizer.lex_reserve(word)

            # numbers
            elif ch.isnumeric():
                err = 0

                word = ""
                word = word + ch

                ind = i + 1

                if(ind < len(line) and line[ind].isalpha()):
                    err = 1

                while (ind < len(line)) and (line[ind].isnumeric() or line[ind] == '.' or line[ind].isalpha()):
                    word = word + line[ind]
                    if(ind < len(line) and line[ind].isalpha()):
                        err = 1
                    ind = ind + 1

                ind = ind - i - 1

                if(err == 1):
                    recognizer.lex_error_identifier(word)
                else:
                    recognizer.lex_number(word)

            # others
            else:

                word = ""
                word = word + ch

                ind = i + 1

                all = ['+', '-', '*', '/', '%', '=', '!', '>', '<']

                if(ind < len(line)):
                    if ch in all and line[ind] == '=':
                        recognizer.lex_delimoper(ch + line[ind])
                        ind = ind - i
                    elif ch == '/' and line[ind] == '/':
                        if((len(line) > ind + 1) and line[ind + 1] == '='):
                            recognizer.lex_delimoper(ch + line[ind] + line[ind + 1]) 
                            ind = ind - i + 1
                        else:
                            recognizer.lex_delimoper(ch + line[ind])
                            ind = ind - i
                    elif ch == '+' and line[ind] == '+':
                        recognizer.lex_delimoper(ch + line[ind])
                        ind = ind - i
                    elif ch == '-' and line[ind] == '-':
                        recognizer.lex_delimoper(ch + line[ind])
                        ind = ind - i
                    elif ch == '|' and line[ind] == '|':
                        recognizer.lex_delimoper(ch + line[ind])
                        ind = ind - i
                    elif ch == '&' and line[ind] == '&':
                        recognizer.lex_delimoper(ch + line[ind])
                        ind = ind - i
                    else:
                        recognizer.lex_delimoper(ch)
                        ind = ind - i - 1
                else:
                    recognizer.lex_delimoper(ch)
                    ind = ind - i - 1
        
        # unterminated comment
        if y == len(lines) - 1 and comment == 1:
            error = 2
    
    # output error or result
    if error == 2:
        return recognizer.comm_err()
    else:
        return recognizer.result()