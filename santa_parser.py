# santa_parser.py
import ply.yacc as yacc
from santa_lexer import tokens

precedence = (
    ('left', 'DOT'),  # Highest precedence for method and function chaining
    ('left', 'GIVE', 'TAKE'),
    ('left', 'MULTIPLY_JOY', 'SHARE', 'LEFTOVER_MAGIC', 'FLOOR_CHIMNEY'),
    ('left', 'MIN_GIFT', 'MAX_GIFT', 'ROUND_PRESENTS'),
    ('right', 'POWER_OF_BELIEF'),
    ('left', 'MORE_FESTIVE', 'LESS_FESTIVE', 'SAME_GIFT'),
)

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement
                     | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : variable_declaration
                | assignment_statement
                | if_statement
                | loop_statement
                | deliver_statement
                | method_call_statement
                | workshop_definition
                | error_handling
                | function_call_statement
                | decorator_statement
                | await_statement
                | lambda_statement'''
    p[0] = p[1]

def p_variable_declaration(p):
    '''variable_declaration : WRAP IDENTIFIER AS type
                          | WRAP IDENTIFIER AS QUANTUM_GIFT LT type GT
                          | WRAP IDENTIFIER AS GIFT LT type GT'''
    if len(p) == 5:
        p[0] = ('declare', p[2], p[4])
    elif p[4] == 'QUANTUM_GIFT':
        p[0] = ('declare_quantum', p[2], p[6])
    else:  # GIFT<TYPE>
        p[0] = ('declare_typed_array', p[2], p[6])

def p_type(p):
    '''type : MERRY
            | JINGLE
            | TINSEL
            | GIFT
            | SPIRIT
            | SNOWFLAKE
            | SLEIGH
            | STOCKING'''
    p[0] = p[1]

def p_assignment_statement(p):
    '''assignment_statement : IDENTIFIER AS expression'''
    p[0] = ('assign', p[1], p[3])

def p_if_statement(p):
    '''if_statement : NICE expression THEN statement_list NAUGHTY statement_list END_OF_LIST'''
    p[0] = ('if', p[2], p[4], p[6])

def p_loop_statement(p):
    '''loop_statement : while_loop
                     | foreach_loop
                     | count_loop'''
    p[0] = p[1]

def p_while_loop(p):
    '''while_loop : WHILE_CHRISTMAS_SPIRIT condition DO statement_list STILL_BELIEVING'''
    p[0] = ('while', p[2], p[4])

def p_foreach_loop(p):
    '''foreach_loop : FOR_EACH_CHILD IN expression DO statement_list CHECKED_TWICE'''
    p[0] = ('foreach', 'IN', p[3], p[5])

def p_count_loop(p):
    '''count_loop : AROUND_THE_CHRISTMAS_TREE expression DO statement_list UNTIL_CHRISTMAS'''
    p[0] = ('count', p[2], p[4])

def p_lambda_expression(p):
    '''lambda_expression : QUICK_ELF LPAREN IDENTIFIER RPAREN ARROW expression'''
    p[0] = ('lambda', p[3], p[6])

def p_deliver_statement(p):
    '''deliver_statement : DELIVER expression'''
    p[0] = ('deliver', p[2])

def p_await_statement(p):
    '''await_statement : AWAIT_CHRISTMAS expression'''
    p[0] = ('await', p[2])

def p_method_call_statement(p):
    '''method_call_statement : method_call'''
    p[0] = p[1]

def p_function_call_statement(p):
    '''function_call_statement : function_call'''
    p[0] = p[1]

def p_workshop_definition(p):
    '''workshop_definition : WORKSHOP IDENTIFIER LPAREN parameter_list RPAREN RETURNS type OPENS statement_list CLOSES
                         | WORKSHOP IDENTIFIER LPAREN parameter_list RPAREN OPENS statement_list CLOSES
                         | MAGIC_WORKSHOP IDENTIFIER LPAREN parameter_list RPAREN OPENS statement_list CLOSES'''
    if p[1] == 'WORKSHOP':
        if len(p) == 11:
            p[0] = ('workshop', p[2], p[4], p[7], p[9])
        else:
            p[0] = ('workshop', p[2], p[4], None, p[7])
    else:
        p[0] = ('magic_workshop', p[2], p[4], p[7])

def p_parameter_list(p):
    '''parameter_list : parameter
                     | parameter_list COMMA parameter
                     | empty'''
    if len(p) == 2:
        if p[1] is None:
            p[0] = []
        else:
            p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_parameter(p):
    '''parameter : type IDENTIFIER
                | GIFT LT type GT IDENTIFIER'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (f'GIFT<{p[3]}>', p[5])

def p_error_handling(p):
    '''error_handling : BELIEVE statement_list DOUBT statement_list KEEP_FAITH'''
    p[0] = ('try_catch', p[2], p[4])

def p_decorator_statement(p):
    '''decorator_statement : AT IDENTIFIER workshop_definition'''
    p[0] = ('decorator', p[2], p[3])

def p_method_call(p):
    '''method_call : IDENTIFIER DOT method_name LPAREN RPAREN
                  | IDENTIFIER DOT method_name LPAREN expression_list RPAREN
                  | method_call DOT method_name LPAREN RPAREN
                  | method_call DOT method_name LPAREN expression_list RPAREN'''
    if isinstance(p[1], str):
        if len(p) == 6:
            p[0] = ('method_call', p[1], p[3], [])
        else:
            p[0] = ('method_call', p[1], p[3], p[5])
    else:
        prev_call = p[1]
        if len(p) == 6:
            p[0] = ('method_call', ('method_result', prev_call), p[3], [])
        else:
            p[0] = ('method_call', ('method_result', prev_call), p[3], p[5])

def p_method_chain(p):
    '''method_chain : method_name LPAREN RPAREN
                   | method_name LPAREN expression_list RPAREN'''
    def create_call(obj):
        if len(p) == 4:
            return ('method_call', obj, p[1], [])
        else:
            return ('method_call', obj, p[1], p[3])
    p[0] = create_call

def p_method_name(p):
    '''method_name : IDENTIFIER
                  | PACK
                  | PEEK_INSIDE
                  | UNWRAP
                  | SPARKLE
                  | WRAP_STRING
                  | UNTANGLE
                  | COUNT_JOYS
                  | TO_TINSEL
                  | TO_JINGLE
                  | MEASURE
                  | MORE_FESTIVE
                  | LESS_FESTIVE
                  | TRIM_TREE
                  | JINGLE_CASE
                  | SILENT_NIGHT
                  | GIFT_WRAP
                  | FIND_CHIMNEY
                  | REPLACE_COAL'''
    p[0] = p[1]

def p_expression(p):
    '''expression : simple_expression
                 | arithmetic_expression
                 | array_literal
                 | dictionary_literal
                 | boolean_literal
                 | method_call
                 | function_call
                 | comparison_expression
                 | lambda_expression
                 | dictionary_access'''
    p[0] = p[1]

def p_lambda_statement(p):
    '''lambda_statement : lambda_expression'''
    p[0] = p[1]

def p_lambda_expression(p):
    '''lambda_expression : QUICK_ELF LPAREN IDENTIFIER RPAREN ARROW expression'''
    p[0] = ('lambda', p[3], p[6])

def p_simple_expression(p):
    '''simple_expression : NUMBER
                        | STRING
                        | IDENTIFIER'''
    p[0] = ('value', p[1])

def p_arithmetic_expression(p):
    '''arithmetic_expression : expression GIVE expression
                           | expression TAKE expression
                           | expression MULTIPLY_JOY expression
                           | expression SHARE expression
                           | expression LEFTOVER_MAGIC expression
                           | expression POWER_OF_BELIEF expression
                           | expression FLOOR_CHIMNEY expression
                           | expression ROUND_PRESENTS expression
                           | expression MIN_GIFT expression
                           | expression MAX_GIFT expression
                           | LPAREN arithmetic_expression RPAREN'''
    if len(p) == 4 and p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = ('arithmetic', p[2], p[1], p[3])

def p_comparison_expression(p):
    '''comparison_expression : expression MORE_FESTIVE expression
                           | expression LESS_FESTIVE expression
                           | expression SAME_GIFT expression'''
    p[0] = ('comparison', p[2], p[1], p[3])

def p_array_literal(p):
    '''array_literal : LBRACKET expression_list RBRACKET
                    | LBRACKET RBRACKET'''
    if len(p) == 4:
        p[0] = ('array', p[2])
    else:
        p[0] = ('array', [])

def p_dictionary_literal(p):
    '''dictionary_literal : LBRACE key_value_list RBRACE
                        | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = ('dictionary', p[2])
    else:
        p[0] = ('dictionary', [])

def p_key_value_list(p):
    '''key_value_list : key_value
                     | key_value_list COMMA key_value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_key_value(p):
    '''key_value : STRING COLON expression'''
    p[0] = (p[1], p[3])

def p_dictionary_access(p):
    '''dictionary_access : IDENTIFIER LBRACKET expression RBRACKET'''
    p[0] = ('dictionary_access', p[1], p[3])

def p_expression_list(p):
    '''expression_list : expression
                      | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_boolean_literal(p):
    '''boolean_literal : HO
                      | NAH'''
    p[0] = ('boolean', p[1] == 'HO')

def p_function_composition(p):
    '''function_composition : IDENTIFIER DOT IDENTIFIER
                          | function_composition DOT IDENTIFIER'''
    if isinstance(p[1], str):
        p[0] = ('function_composition', [p[1], p[3]])
    else:
        funcs = p[1][1].copy()
        funcs.append(p[3])
        p[0] = ('function_composition', funcs)

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN expression_list RPAREN
                    | IDENTIFIER LPAREN RPAREN
                    | function_composition LPAREN expression_list RPAREN
                    | function_composition LPAREN RPAREN'''
    if isinstance(p[1], str):  # Simple function call
        p[0] = ('function_call', p[1], [] if len(p) == 4 else p[3])
    else:  # Function composition
        p[0] = ('function_call', p[1], [] if len(p) == 4 else p[3])

def p_function_chain(p):
    '''function_chain : IDENTIFIER
                     | function_chain DOT IDENTIFIER'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + '.' + p[3]

def p_empty(p):
    '''empty :'''
    pass

def p_condition(p):
    '''condition : comparison_expression
                | boolean_literal'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"🎅 Syntax error at '{p.value}', line {p.lineno}")
    else:
        print("🎅 Syntax error at EOF")

parser = yacc.yacc()