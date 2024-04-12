import recognizer
import re

def parseInp():

    # get all lexeme and tokens from lexical analyzer
    lines = recognizer.syntax()

    # remove lexemes
    tokens = separateTokens(lines)

    # check tokens
    errors = parseCheck(tokens)

    # return success or error list
    return errors

def separateTokens(lines):

    # create storage variables
    tokens_line = []
    current_line = []

    # separate by line count and ignore comment
    for _, token in lines:
        if token != "line_counter" and token != "comment":
            current_line.append(token)
        elif token == "line_counter":
            if current_line:
                tokens_line.append(current_line)
                current_line = []
            else:
                tokens_line.append([])
    if current_line:
        tokens_line.append(current_line)
    
    # return the tokens
    return tokens_line

def parseCheck(tokens):

    # create storage and checker variables
    err = []
    line_count = 0
    cb = 0

    # iterate token per line
    for tl in tokens:
        
        # create object of syntax analyzer class
        syntax = SyntaxAnalyzer(tl) 

        # error from lexical analyzer, unterminated text
        if "unterminated_text" in tl:
            try:
                syntax.check_err(line_count, "unterminated text")   
            except SyntaxError: pass

        # error from lexical analyzer, invalid identifier
        elif "invalid_identifier" in tl:
            try:
                syntax.check_err(line_count, "invalid identifier") 
            except SyntaxError: pass
            
        # error from lexical analyzer, invalid token
        elif "invalid_token" in tl:
            try:
                syntax.check_err(line_count, "invalid token")
            except SyntaxError: pass

        # error from lexical analyzer, unterminated comment
        elif "unterminated_comment" in tl:
            try:
                syntax.check_err(line_count, "unterminated comment")
            except SyntaxError: pass
        
        # continue if no error in lexical analyzer
        else:  
            
            # check start token per line
            for t in tl:

                # area square and perimeter square line checking
                if t == "ar_sq" or t == "per_sq":  
                    try:  
                        syntax.check_ap_one(line_count)
                    except SyntaxError: pass
                    break

                # area rectangle, area triangle, and perimeter rectangle line checking
                elif t == "ar_re" or t == "ar_tr" or t == "per_re":
                    try:  
                        syntax.check_ap_two(line_count)
                    except SyntaxError: pass
                    break
                
                # perimeter triangle line checking
                elif t == "per_tr":
                    try:  
                        syntax.check_ap_three(line_count)
                    except SyntaxError: pass
                    break

                # show square and show triangle line checking
                elif t == "show_sq" or t == "show_tr":              
                    try:  
                        syntax.check_ds_one(line_count)
                    except SyntaxError: pass      
                    break

                # show rectangle line checking
                elif t == "show_re":            
                    try:  
                        syntax.check_ds_two(line_count)
                    except SyntaxError: pass
                    break

                # shortened conditional line checking
                elif t == "func_cond":
                    try:
                        syntax.check_sc(line_count)
                    except SyntaxError: pass
                    break

                # direct calculation line checking
                elif t == "func_add" or t == "func_sub" or t == "func_multi":
                    try:
                        syntax.check_dc(line_count)
                    except SyntaxError: pass
                    break

                # counting statement line checking
                elif t == "cont_up" or t == "cont_down":
                    try:
                        syntax.check_count_stmnt(line_count)
                        cb = cb + 1
                    except SyntaxError: pass
                    break

                # while statement line checking
                elif t == "cont_while":
                    try:
                        syntax.check_while_stmnt(line_count)
                        cb = cb + 1
                    except SyntaxError: pass
                    break

                # for statement line checking
                elif t == "cont_for":
                    try:
                        syntax.check_for_stmnt(line_count)
                        cb = cb + 1
                    except SyntaxError: pass
                    break

                # is and iselese line checking
                elif t == "cont_is" or t == "cont_iselse":
                    try:
                        syntax.check_cont_isiselse(line_count)
                        cb = cb + 1
                    except SyntaxError: pass
                    break
                
                # else line checking
                elif t == "cont_else":
                    try:
                        syntax.check_cont_else(line_count)
                        cb = cb + 1
                    except SyntaxError: pass
                    break
            
                # declaration whole number line checking
                elif t == "dt_wn":
                    try:
                        syntax.check_dec_wn(line_count)
                    except SyntaxError: pass
                    break
                
                # declaration decimal number line checking
                elif t == "dt_dn":
                    try:
                        syntax.check_dec_dc(line_count)
                    except SyntaxError: pass
                    break

                # declaration text line checking
                elif t == "dt_text":
                    try:
                        syntax.check_dec_t(line_count)
                    except SyntaxError: pass
                    break

                # declaration boolean line checking
                elif t == "dt_bool":
                    try:
                        syntax.check_dec_b(line_count)
                    except SyntaxError: pass
                    break

                # show line checking
                elif t == "io_out":
                    try:
                        syntax.check_io_out(line_count)
                    except SyntaxError: pass
                    break
                    
                # ask line checking
                if t == "identifier" and "io_inp" in tl:
                    try:
                        syntax.check_io_inp(line_count)
                    except SyntaxError: pass
                    break

                # assignment line checking
                elif t == "identifier" and "io_inp" not in tl:
                    try:
                        syntax.check_assi(line_count)
                    except SyntaxError: pass
                    break

                # delimeter line checking
                elif t == "delim_curl_clo":
                    cb = cb - 1
                    try:
                        syntax.curl_clo(line_count)
                    except SyntaxError: pass
                    break
                
                # not valid statement
                else:
                    try:
                        syntax.check_err(line_count, "invalid statement")
                    except SyntaxError: pass
                    break

        # append error and break
        err.extend(syntax.error_log)
        
        # increment line count
        line_count = line_count + 1

    # check curly brackets count
    if cb < 0:
        err.append("Program error: brackets closed count error")    
    if cb > 0:
        err.append("Program error: brackets opened count error")  
    
    # return success or list of error
    if len(err) == 0:
        err.append("Success")
    return err

# syntax analyzer class
class SyntaxAnalyzer:

    # setup the class
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.current_token = None
        self.error_log = []
        self.consume()

################################################ BASIC FUNCTIONS ################################################
    # consume token function
    def consume(self):
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
        else:
            self.current_token = None    

    # matcher function
    def matchTok(self, correct, lexeme, line, context):
        if self.current_token == correct:
            self.consume()
        else:
            a = ("Line " + str(line) + " error: expecting '" + str(lexeme) + "' at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
################################################ MATCHER FUNCTIONS ################################################

################################################ FORMAT CHECKER FUNCTIONS ################################################
    # area perimeter one parameter syntax
    def check_ap_one(self, line):
        if self.current_token == "ar_sq":
            context = "square area function"
        else:
            context = "square perimeter function"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_ap_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
    
    # area perimeter two parameter syntax
    def check_ap_two(self, line):
        if self.current_token == "ar_re":
             context = "rectangle area function"
        elif self.current_token == "ar_tr":
            context = "triangle area function"
        else:
            context = "rectangle perimeter function"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_ap_param(line, context)
        self.matchTok("delim_comma", ",", line, context)
        self.check_ap_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
    
    # area perimeter three parameter syntax
    def check_ap_three(self, line):
        context = "triangle perimeter function"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_ap_param(line, context)
        self.matchTok("delim_comma", ",", line, context)
        self.check_ap_param(line, context)
        self.matchTok("delim_comma", ",", line, context)
        self.check_ap_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
    # draw shape one parameter syntax
    def check_ds_one(self, line):
        if self.current_token == "show_sq":
            context = "show square function"
        else:
            context = "show triangle function"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_ds_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
    # draw shape two parameter syntax
    def check_ds_two(self, line):
        context = "show rectangle function"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_ds_param(line, context)
        self.matchTok("delim_comma", ",", line, context)
        self.check_ds_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # shortened conditional syntax  
    def check_sc(self, line):
        context = "direct conditional function"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_cond_param(line, context)
        self.matchTok("delim_comma", ",", line, context)
        self.matchTok("delim_quote", '"', line, context)
        self.matchTok("val_text", "text", line, context)
        self.matchTok("delim_quote", '"', line, context)
        self.matchTok("delim_comma", ",", line, context)
        self.matchTok("delim_quote", '"', line, context)
        self.matchTok("val_text", "text", line, context)
        self.matchTok("delim_quote", '"', line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

    # direct calculation syntax  
    def check_dc(self, line):
        if self.current_token == "func_add":
            context = "addition direct calculation function"
        elif self.current_token == "func_sub":
            context = "subtraction direct calculation function"
        else:
            context = "multiplication direct calculation function"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_calculation_param(line, context)
        if self.current_token == "delim_comma":
            while self.current_token == "delim_comma":
                self.consume()
                self.check_calculation_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # counting statement syntax  
    def check_count_stmnt(self, line):
        if self.current_token == "cont_up":
            context = "count up head"
        else:
            context = "count down head"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_count_param(line, context)
        self.matchTok("cont_to", "to", line, context)
        self.check_count_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)
        self.matchTok("delim_curl_op", "{", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # while statement syntax  
    def check_while_stmnt(self, line):
        context = "while repetition head"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_cond_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)
        self.matchTok("delim_curl_op", "{", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # for statement syntax  
    def check_for_stmnt(self, line):
        context = "for repetition head"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.matchTok("dt_wn", "wholenum", line, context)
        self.matchTok("identifier", "identifier", line, context)
        self.matchTok("assi_eq", "=", line, context)
        self.check_for_param(line, context)
        self.matchTok("delim_comma", ",", line, context)
        self.check_cond_param(line, context)
        self.matchTok("delim_comma", ",", line, context)
        self.check_upd_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)
        self.matchTok("delim_curl_op", "{", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # is iselse statement syntax  
    def check_cont_isiselse(self, line):
        if self.current_token == "cont_is":
            context = "is conditional head"
        else:
            context = "iselse conditional head"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_cond_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)
        self.matchTok("delim_curl_op", "{", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # else statement syntax  
    def check_cont_else(self, line):
        context = "else conditional head"

        self.consume()

        self.matchTok("delim_curl_op", "{", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # output statement syntax 
    def check_io_out(self, line):
        context = "output statement"

        self.consume()

        self.matchTok("delim_paren_op", "(", line, context)
        self.check_out_param(line, context)
        if  self.current_token == "delim_comma":
            while self.current_token == "delim_comma":
                self.consume()
                self.check_out_param(line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")        

    # input statement syntax 
    def check_io_inp(self, line):
        context = "input statement"

        self.consume()

        self.matchTok("assi_eq", "=", line, context)
        self.matchTok("io_inp", "show", line, context)
        self.matchTok("delim_paren_op", "(", line, context)
        self.matchTok("delim_paren_clo", ")", line, context)

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")   

    # declaration whole number syntax
    def check_dec_wn(self, line):
        context = "whole number declaration statement"

        self.consume()

        self.check_dec_wn_val(line, context)
        while self.current_token == "delim_comma":
            self.consume()
            self.check_dec_wn_val(line, context)

    # declaration decimal number syntax
    def check_dec_dc(self, line):
        context = "decimal number declaration statement"

        self.consume()

        self.check_dec_dn_val(line, context)
        while self.current_token == "delim_comma":
            self.consume()
            self.check_dec_dn_val(line, context)

    # declaration text syntax
    def check_dec_t(self, line):
        context = "text declaration statement"

        self.consume()

        self.check_dec_t_val(line, context)
        while self.current_token == "delim_comma":
            self.consume()
            self.check_dec_t_val(line, context)

    # declaration boolean syntax
    def check_dec_b(self, line):
        context = "boolean declaration statement"

        self.consume()

        self.check_dec_b_val(line, context)
        while self.current_token == "delim_comma":
            self.consume()
            self.check_dec_b_val(line, context)

    # assignment statement syntax
    def check_assi(self, line):
        context = "assignment statement"

        self.consume()

        self.check_assi_params(line, context)

    # curly brackets line
    def curl_clo(self, line):
        context = "close bracket line"
        
        self.consume()

        if self.current_token is not None:
            a = ("Line " + str(line) + " error: exceed token count at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")     

    # error add
    def check_err(self, line, context):
        a = ("Line " + str(line) + " error: " + str(context))
        self.error_log.append(a) 
        raise SyntaxError ("")  
################################################ FORMAT CHECKER FUNCTIONS ################################################        

################################################ PARAMETER CHECKER FUNCTIONS ################################################
    # area perimeter parameter checker
    def check_ap_param(self, line, context):
        data = ["identifier", "val_whole", "val_decimal"]
        para = 0

        if self.current_token in data:
            self.consume()
        elif self.current_token == "pos_add":
            self.consume()
            if self.current_token in data:
                self.consume()
            elif self.current_token is None:
                para = 1
            else:
                para = 1
        else:
            para = 2
        
        if para == 1:
            a = ("Line " + str(line) + " error: expecting valid value after sign at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # draw shape parameter checker  
    def check_ds_param(self, line, context):
        data = ["identifier", "val_whole"]
        para = 0

        if self.current_token in data:
            self.consume()
        elif self.current_token == "pos_add":
            self.consume()
            if self.current_token in data:
                self.consume()
            elif self.current_token is None:
                para = 1
            else:
                para = 1
        else:
            para = 2
     
        if para == 1:
            a = ("Line " + str(line) + " error: expecting valid value after sign at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
    
    # condition parameter checker
    def check_cond_param(self, line, context):
        data1 = ["identifier", "val_whole", "val_decimal"]
        data2 = ["val_true", "val_false"]
        signs = ["pos_add", "neg_sub"]
        para1 = 0
        para2 = 0

        cur1 = ""

        if self.current_token in data1:
            cur1 = self.current_token
            self.consume()
        elif self.current_token in data2:
            cur1 = "bool"
            self.consume()
        elif self.current_token in signs:
            self.consume()
            if self.current_token in data1:
                cur1 = self.current_token
                self.consume()
            elif self.current_token is None:
                para1 = 1
            else:
                para1 = 1
        elif self.current_token == "log_not":
            self.consume()
            if self.current_token in data2:
                cur1 = "bool"
                self.consume()
            elif self.current_token == "identifier":
                cur1 = self.current_token
                self.consume()
            elif self.current_token is None:
                para1 = 1 
            else:
                para1 = 1
        elif self.current_token == "delim_quote":
            self.consume()
            if self.current_token == "val_text":
                cur1 = self.current_token
                self.consume()
                if self.current_token == "delim_quote":
                    self.consume()
                elif self.current_token is None:
                    para1 = 1 
                else:
                     para1 = 1
            elif self.current_token is None:
                para1 = 1 
            else:
                para1 = 1
        else:
            para1 = 1

        if para1 == 1:
            a = ("Line " + str(line) + " error: invalid first parameter at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        op = ["log_or", "log_and", "rel_eq", "rel_noteq", "rel_great", "rel_less", "rel_greateq", "rel_lesseq", "log_or", "log_and"]

        if self.current_token in op:
            self.consume()
        else:
            a = ("Line " + str(line) + " error: invalid operator at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError("")
        
        cur2 = ""

        if self.current_token in data1:
            cur2 = self.current_token
            self.consume()
        elif self.current_token in data2:
            cur2 = "bool"
            self.consume()
        elif self.current_token in signs:
            self.consume()
            if self.current_token in data1:
                cur2 = self.current_token
                self.consume()
            elif self.current_token is None:
                para2 = 1
            else:
                para2 = 1
        elif self.current_token == "log_not":
            self.consume()
            if self.current_token in data2:
                cur2 = "bool"
                self.consume()
            elif self.current_token == "identifier":
                cur1 = self.current_token
                self.consume()
            elif self.current_token is None:
                para2 = 1 
            else:
                para2 = 1
        elif self.current_token == "delim_quote":
            self.consume()
            if self.current_token == "val_text":
                cur2 = self.current_token
                self.consume()
                if self.current_token == "delim_quote":
                    self.consume()
                elif self.current_token is None:
                    para2 = 1 
                else:
                     para2 = 1
            elif self.current_token is None:
                para2 = 1 
            else:
                para2 = 1
        else:
            para2 = 1

        if para2 == 1:
            a = ("Line " + str(line) + " error: invalid second parameter at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

        if (cur1 == cur2) or (cur1 == "identifier" or cur2 == "identifier"): pass
        else:
            a = ("Line " + str(line) + " error: invalid data type to compare at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # calculation parameter checker
    def check_calculation_param(self, line, context):
        data = ["identifier", "val_whole", "val_decimal"]
        signs = ["pos_add", "neg_sub"]
        para = 0

        if self.current_token in data:
            self.consume()
        elif self.current_token in signs:
            self.consume()
            if self.current_token in data:
                self.consume()
            elif self.current_token is None:
                para = 1
            else:
                para = 1
        else:
            para = 2
        
        if para == 1:
            a = ("Line " + str(line) + " error: expecting valid value after sign at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # counting statement parameter checker
    def check_count_param(self, line, context):
        data = ["identifier", "val_whole"]
        signs = ["pos_add", "neg_sub"]
        para = 0

        if self.current_token in data:
            self.consume()
        elif self.current_token in signs:
            self.consume()
            if self.current_token in data:
                self.consume()
            elif self.current_token is None:
                para = 1
            else:
                para = 1
        else:
            para = 2

        if para == 1:
            a = ("Line " + str(line) + " error: expecting valid value after sign at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # for value statement parameter checker
    def check_for_param(self, line, context):
        data = ["identifier", "val_whole"]
        signs = ["pos_add", "neg_sub"]
        para = 0

        if self.current_token in data:
            self.consume()
        elif self.current_token in signs:
            self.consume()
            if self.current_token in data:
                self.consume()
            elif self.current_token is None:
                para = 1
            else:
                para = 1
        else:
            para = 2

        if para == 1:
            a = ("Line " + str(line) + " error: expecting valid value after sign at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
    # for update statement parameter checker
    def check_upd_param(self, line, context):
        up = ["unar_inc", "unar_dec"]
        para = 0

        if self.current_token in up:
            self.consume()
            if self.current_token ==  "identifier":
                self.consume()
            elif self.current_token is None:
                para = 1
            else:
                para = 1
        elif self.current_token == "identifier":
            self.consume()
            if self.current_token in up:
                self.consume()
            elif self.current_token is None:
                para = 2
            else:
                para = 2

        if para == 1:
            a = ("Line " + str(line) + " error: expecting identifier at update of" + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting increment or decrement sign at update of " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # output statement parameter checker
    def check_out_param(self, line, context):
        data1 = ["identifier", "val_whole", "val_decimal", "val_true", "val_false"]
        data2 = ["identifier", "val_whole", "val_decimal"]
        data3 = ["identifier", "val_true", "val_false"]
        signs = ["pos_add", "neg_sub"]
        para = 0

        if self.current_token in data1:
            self.consume()
        elif self.current_token in signs:
            self.consume()
            if self.current_token in data2:
                self.consume()
            elif self.current_token is None:
                para = 1
            else:
                para = 1
        elif self.current_token == "log_not":
            if self.current_token in data3:
                self.consume()
            elif self.current_token is None:
                para = 1
            else:
                para = 1
        elif self.current_token == "delim_quote":
            self.consume()
            if self.current_token == "val_text":
                self.consume()
                if self.current_token == "delim_quote":
                    self.consume()
                elif self.current_token is None:
                    para = 3
                else:
                    para = 3
            elif self.current_token is None:
                para = 3
            else:
                para = 3
        else:
            para = 2
        
        if para == 1:
            a = ("Line " + str(line) + " error: expecting valid value after sign at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 3:
            a = ("Line " + str(line) + " error: expecting valid text at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # whole number declaration parameter checker
    def check_dec_wn_val(self, line, context):
        signs = ["pos_add", "neg_sub"]
        para = 0

        if self.current_token == "identifier":
            self.consume()
            if self.current_token == "assi_eq":
                self.consume()
                if self.current_token == "identifier" or self.current_token == "val_whole":
                    self.consume()
                elif self.current_token in signs:
                    self.consume()
                    if self.current_token == "val_whole" or self.current_token == "identifier":
                        self.consume()
                    elif self.current_token is None:
                        para = 1
                    else:
                        para = 1
                elif self.current_token is None:
                    para = 2
                else:
                    para = 2
        else:
            para = 2
    
        if self.current_token and self.current_token != "delim_comma":
            para = 2

        if para == 1:
            a = ("Line " + str(line) + " error: expecting valid value after sign at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # decimal number declaration parameter checker
    def check_dec_dn_val(self, line, context):
        signs = ["pos_add", "neg_sub"]
        para = 0

        if self.current_token == "identifier":
            self.consume()
            if self.current_token == "assi_eq":
                self.consume()
                if self.current_token == "identifier" or self.current_token == "val_whole" or self.current_token == "val_decimal":
                    self.consume()
                elif self.current_token in signs:
                    self.consume()
                    if self.current_token == "identifier" or self.current_token == "val_whole" or self.current_token == "val_decimal":
                        self.consume()
                    elif self.current_token is None:
                        para = 1
                    else:
                        para = 1
                elif self.current_token is None:
                    para = 2  
                else:
                    para = 2
        else:
            para = 2
        
        if self.current_token and self.current_token != "delim_comma":
            para = 2
        
        if para == 1:
            a = ("Line " + str(line) + " error: expecting valid value after sign at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # text declaration parameter checker
    def check_dec_t_val(self, line, context):
        para = 0

        if self.current_token == "identifier":
            self.consume()
            if self.current_token == "assi_eq":
                self.consume()
                if self.current_token == "delim_quote":
                    self.consume()
                    if self.current_token == "val_text":
                        self.consume()
                        if self.current_token == "delim_quote":
                            self.consume()
                        elif self.current_token is None:
                            para = 1
                        else:
                            para = 1
                    elif self.current_token == "delim_quote":
                        self.consume()
                    elif self.current_token is None:
                        para = 1
                    else:
                        para = 1 
                elif self.current_token is None:
                    para = 2  
                else:
                    para = 2 
        else:
            para = 2
        
        if self.current_token and self.current_token != "delim_comma":
            para = 2

        if para == 1:
            a = ("Line " + str(line) + " error: expecting enclosed text at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # boolean declaration parameter checker
    def check_dec_b_val(self, line, context):
        para = 0

        if self.current_token == "identifier":
            self.consume()
            if self.current_token == "assi_eq":
                self.consume()
                if self.current_token == "val_true" or self.current_token == "val_false":
                    self.consume()
                elif self.current_token is None:
                    para = 2
                else:
                    para = 2 
        else:
            para = 2
        
        if self.current_token and self.current_token != "delim_comma":
            para = 2
        
        if para == 2:
            a = ("Line " + str(line) + " error: expecting valid value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")

    # assignment statement parameter checker
    def check_assi_params(self, line, context):
        para = 0

        op = ["assi_eq", "assi_add", "assi_sub", "assi_mul", "assi_div", "assi_mod", "assi_indiv"]
        cons = ""
        
        if self.current_token in op:
            cons = self.current_token
            self.consume()

            values = ""
            inc = 0

            if self.current_token == "val_true" or self.current_token == "val_false":
                self.consume()
                if cons != "assi_eq" or self.current_token is not None:
                    para = 2
            elif self.current_token:
                while self.current_token:
                    x = self.current_token
                    add = ""         
                    if x == "identifier":
                        add = "x"
                        self.consume()
                    elif x == "ar_mul":
                        add = "*"
                        self.consume()
                    elif x == "ar_div":
                        add = "/"
                        self.consume()
                    elif x == "ar_mod":
                        add = "%"
                        self.consume()
                    elif x == "ar_indiv":
                        add = "//"
                        self.consume()
                    elif x == "pos_add":
                        add = "+"
                        self.consume()
                    elif x == "neg_sub":
                        add = "-"
                        self.consume()
                    elif x == "delim_paren_op":
                        add = "("
                        self.consume()
                    elif x == "delim_paren_clo":
                        add = ")"
                        self.consume()
                    elif x == "val_whole":
                        add = "1"
                        self.consume()
                    elif x == "val_decimal":
                        add = "2"
                        self.consume()
                    elif x == "delim_quote":
                        self.consume()
                        if self.current_token == "val_text":
                            self.consume()
                            if self.current_token == "delim_quote":
                                self.consume()
                                add = "y"
                            elif self.current_token is None:
                                para = 4
                            else:
                                para = 4
                        elif self.current_token is None:
                            para = 4
                        else:
                            para = 4
                    else:
                        inc = 1
                    values = values + " " + add
                if inc == 0:
                    valid_expression = re.compile(r"\b(?:[a-zA-Z_]\w*|\d+|\+|-|//|%|\*|\(|\)|\s+)*\b")
                    a = valid_expression.search(values)
                    if not a:
                        para = 6
                else:
                    para = 5
            else:
                para = 1
        else:
            para = 3

        if para == 1:
            a = ("Line " + str(line) + " error: expecting value at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")    
        if para == 2:
            a = ("Line " + str(line) + " error: invalid boolean assignment at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        elif para == 3:
            a = ("Line " + str(line) + " error: expecting assignment operator at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        elif para == 4:
            a = ("Line " + str(line) + " error: expecting enclosed text at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        elif para == 5:
            a = ("Line " + str(line) + " error: invalid token at " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
        elif para == 6:
            a = ("Line " + str(line) + " error: invalid " + str(context))
            self.error_log.append(a) 
            raise SyntaxError ("")
################################################ PARAMETER CHECKER FUNCTIONS ################################################