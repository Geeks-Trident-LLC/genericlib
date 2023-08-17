
class PATTERN:

    ANYTHING = '.'
    ZOANYTHING = '.?'
    SOMETHING = '.*'
    EVERYTHING = '.+'

    SPACE = ' '
    SPACES = ' +'
    MTONESPACES = '  +'
    MORETHANONESPACES = MTONESPACES
    ATLONESPACES = '  +'
    ATLEASTONESPACES = ATLONESPACES
    ZOSPACE = ' ?'
    ZOSPACES = ' *'
    SPACEATSOS = '^ '
    SPACESATSOS = '^ +'
    SPACEATEOS = ' $'
    SPACESATEOS = ' +$'

    WHITESPACE = r'\s'
    WHITESPACES = r'\s+'
    ZOWHITESPACES = r'\s*'

    CRNL = r'\r?\n|\r'
    CR_NL = CRNL
    MULTICRNL = r'[\r\n]+'
    ZOMULTICRNL = r'[\r\n]*'

    DIGIT = '[0-9]'
    DIGITS = '%s+' % DIGIT

    NUMBER = '[0-9]*[.]?[0-9]+'
    MIXED_NUMBER = r'[+\(\[\$-]?(\d+([,:/-]\d+)*)?[.]?\d+[\]\)%a-zA-Z]*'

    LETTER = '[a-zA-Z]'
    LETTERS = '%s+' % LETTER

    ALPHABET_NUMERIC = '[a-zA-Z0-9]'

    SYMBOL = r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]'
    SYMBOLS = '%s+' % SYMBOL
    SYMBOLS_OR_PHRASE = '%s( %s)*' % (SYMBOLS, SYMBOLS)
    SYMBOLS_OR_GROUP = '%s( +%s)*' % (SYMBOLS, SYMBOLS)
    SYMBOLS_PHRASE = '%s( %s)+' % (SYMBOLS, SYMBOLS)
    SYMBOLS_GROUP = '%s( +%s)+' % (SYMBOLS, SYMBOLS)
    CHECK_SYMBOL = '%s$' % SYMBOL
    CHECK_SYMBOLS = '%s$' % SYMBOLS
    CHECK_SYMBOLS_GROUP = ' *%s *$' % SYMBOLS_GROUP

    SPACE_SYMBOL = r'[ \x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]'
    MULTI_SPACE_SYMBOLS = '%s+' % SPACE_SYMBOL

    GRAPH = r'[\x21-\x7e]'

    WORD = r'%s+' % ALPHABET_NUMERIC
    WORDS = r'%s( %s)*' % (WORD, WORD)
    PHRASE = r'%s( %s)+' % (WORD, WORD)
    WORD_OR_GROUP = r'%s( +%s)*' % (WORD, WORD)
    WORD_GROUP = r'%s( +%s)+' % (WORD, WORD)

    MIXED_WORD = '%s+' % GRAPH
    MIXED_WORDS = '%s( %s)*' % (MIXED_WORD, MIXED_WORD)
    MIXED_PHRASE = '%s( %s)+' % (MIXED_WORD, MIXED_WORD)
    MIXED_WORD_OR_GROUP = '%s( +%s)*' % (MIXED_WORD, MIXED_WORD)
    MIXED_WORD_GROUP = '%s( +%s)+' % (MIXED_WORD, MIXED_WORD)

    NON_WHITESPACE = r'\S'
    NON_WHITESPACES = r'%s+' % NON_WHITESPACE
    NON_WHITESPACES_OR_PHRASE = r'%s( %s)*' % (NON_WHITESPACES, NON_WHITESPACES)
    NON_WHITESPACES_PHRASE = r'%s( %s)+' % (NON_WHITESPACES, NON_WHITESPACES)
    NON_WHITESPACES_OR_GROUP = r'%s( +%s)*' % (NON_WHITESPACES, NON_WHITESPACES)
    NON_WHITESPACES_GROUP = r'%s( +%s)+' % (NON_WHITESPACES, NON_WHITESPACES)
