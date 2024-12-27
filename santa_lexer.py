# santa_lexer.py
import ply.lex as lex

OPERATORS = {
    'GIVE': '+',
    'TAKE': '-',
    'MULTIPLY_JOY': '*',
    'SHARE': '/',
    'LEFTOVER_MAGIC': '%',
    'POWER_OF_BELIEF': '**',
    'MORE_FESTIVE': '>',
    'LESS_FESTIVE': '<',
    'SAME_GIFT': '==',
    'FLOOR_CHIMNEY': '//',
    'ROUND_PRESENTS': 'round',
    'MIN_GIFT': 'min',
    'MAX_GIFT': 'max'
}

tokens = (
    # Basic types and declarations
    'WRAP', 'AS', 'MERRY', 'IDENTIFIER', 'NUMBER', 'STRING',
    'JINGLE', 'TINSEL', 'GIFT', 'SPIRIT', 'SNOWFLAKE', 'SLEIGH', 'STOCKING',

    # Control structures
    'NICE', 'NAUGHTY', 'THEN', 'END_OF_LIST',
    'WHILE_CHRISTMAS_SPIRIT', 'DO', 'STILL_BELIEVING',
    'FOR_EACH_CHILD', 'IN', 'CHECKED_TWICE',
    'AROUND_THE_CHRISTMAS_TREE', 'UNTIL_CHRISTMAS',

    # Functions and workshops
    'WORKSHOP', 'OPENS', 'CLOSES', 'RETURNS',
    'MAGIC_WORKSHOP', 'AWAIT_CHRISTMAS',
    'QUICK_ELF', 'ARROW',

    # Error handling
    'BELIEVE', 'DOUBT', 'KEEP_FAITH',

    # Operators
    'GIVE', 'TAKE', 'MULTIPLY_JOY', 'SHARE', 'LEFTOVER_MAGIC',
    'POWER_OF_BELIEF', 'MORE_FESTIVE', 'LESS_FESTIVE', 'SAME_GIFT',
    'FLOOR_CHIMNEY', 'ROUND_PRESENTS', 'MIN_GIFT', 'MAX_GIFT',

    # Methods
    'PACK', 'PEEK_INSIDE', 'UNWRAP', 'SPARKLE', 'WRAP_STRING',
    'UNTANGLE', 'COUNT_JOYS', 'TO_TINSEL', 'TO_JINGLE', 'MEASURE',
    'TRIM_TREE', 'JINGLE_CASE', 'SILENT_NIGHT', 'GIFT_WRAP',
    'FIND_CHIMNEY', 'REPLACE_COAL',

    # Punctuation
    'DOT', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE', 'COLON', 'AT', 'LT', 'GT',

    # Values
    'HO', 'NAH',

    # Special keywords
    'DELIVER', 'QUANTUM_GIFT'
)

# Simple tokens
t_DOT = r'\.'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'
t_AT = r'@'
t_LT = r'<'
t_GT = r'>'
t_ARROW = r'->'

def t_NUMBER(t):
    r'\d*\.?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = float(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    keywords = {
        # Methods first (to prevent conflicts with declarations)
        'WRAP_STRING': 'WRAP_STRING',
        'SPARKLE': 'SPARKLE',
        'UNTANGLE': 'UNTANGLE',
        'COUNT_JOYS': 'COUNT_JOYS',
        'TO_TINSEL': 'TO_TINSEL',
        'TO_JINGLE': 'TO_JINGLE',
        'TRIM_TREE': 'TRIM_TREE',
        'JINGLE_CASE': 'JINGLE_CASE',
        'SILENT_NIGHT': 'SILENT_NIGHT',
        'GIFT_WRAP': 'GIFT_WRAP',
        'FIND_CHIMNEY': 'FIND_CHIMNEY',
        'REPLACE_COAL': 'REPLACE_COAL',
        'PACK': 'PACK',
        'PEEK_INSIDE': 'PEEK_INSIDE',
        'UNWRAP': 'UNWRAP',
        'MEASURE': 'MEASURE',

        # Operators
        'GIVE': 'GIVE',
        'TAKE': 'TAKE',
        'MULTIPLY_JOY': 'MULTIPLY_JOY',
        'SHARE': 'SHARE',
        'LEFTOVER_MAGIC': 'LEFTOVER_MAGIC',
        'POWER_OF_BELIEF': 'POWER_OF_BELIEF',
        'MORE_FESTIVE': 'MORE_FESTIVE',
        'LESS_FESTIVE': 'LESS_FESTIVE',
        'SAME_GIFT': 'SAME_GIFT',
        'FLOOR_CHIMNEY': 'FLOOR_CHIMNEY',
        'ROUND_PRESENTS': 'ROUND_PRESENTS',
        'MIN_GIFT': 'MIN_GIFT',
        'MAX_GIFT': 'MAX_GIFT',

        # Declaration keywords
        'WRAP_TEXT': 'WRAP_TEXT',  # Only one WRAP entry
        'AS': 'AS',
        'MERRY': 'MERRY',
        'JINGLE': 'JINGLE',
        'TINSEL': 'TINSEL',
        'GIFT': 'GIFT',
        'SPIRIT': 'SPIRIT',
        'SNOWFLAKE': 'SNOWFLAKE',
        'SLEIGH': 'SLEIGH',
        'STOCKING': 'STOCKING',

        # Control structures
        'NICE': 'NICE',
        'NAUGHTY': 'NAUGHTY',
        'THEN': 'THEN',
        'END_OF_LIST': 'END_OF_LIST',
        'WHILE_CHRISTMAS_SPIRIT': 'WHILE_CHRISTMAS_SPIRIT',
        'DO': 'DO',
        'STILL_BELIEVING': 'STILL_BELIEVING',
        'FOR_EACH_CHILD': 'FOR_EACH_CHILD',
        'IN': 'IN',
        'CHECKED_TWICE': 'CHECKED_TWICE',
        'AROUND_THE_CHRISTMAS_TREE': 'AROUND_THE_CHRISTMAS_TREE',
        'UNTIL_CHRISTMAS': 'UNTIL_CHRISTMAS',

        # Functions
        'WORKSHOP': 'WORKSHOP',
        'OPENS': 'OPENS',
        'CLOSES': 'CLOSES',
        'RETURNS': 'RETURNS',
        'MAGIC_WORKSHOP': 'MAGIC_WORKSHOP',
        'AWAIT_CHRISTMAS': 'AWAIT_CHRISTMAS',
        'QUICK_ELF': 'QUICK_ELF',

        # Error handling
        'BELIEVE': 'BELIEVE',
        'DOUBT': 'DOUBT',
        'KEEP_FAITH': 'KEEP_FAITH',

        # Values
        'HO': 'HO',
        'NAH': 'NAH',

        # Special keywords
        'DELIVER': 'DELIVER',
        'QUANTUM_GIFT': 'QUANTUM_GIFT',
    }
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print(f"❌ Ho ho NO! Invalid character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()