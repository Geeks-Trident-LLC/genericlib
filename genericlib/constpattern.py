
class PATTERN:

    ANYTHING = '.'
    ZOANYTHING = '.?'
    SOMETHING = '.*'
    EVERYTHING = '.+'

    SPACE = ' '
    SPACES = ' +'
    MTONESPACES = '  +'
    ATLONESPACES = '  +'
    ZOSPACE = ' ?'
    ZOSPACES = ' *'
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
    MIXED_NUMBER = r'[\(+-]?[0-9]*[.]?[0-9]+[)]?'

    LETTER = '[a-zA-Z]'
    LETTERS = '%s+' % LETTER

    ALPHABET_NUMERIC = '[a-zA-Z0-9]'

    SYMBOL = r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]'
    SYMBOLS = '%s+' % SYMBOL
    SYMBOLS_OR_GROUP = '%s( +%s)*' % (SYMBOLS, SYMBOLS)
    SYMBOLS_GROUP = '%s( +%s)+' % (SYMBOLS, SYMBOLS)

    GRAPH = r'[\x21-\x7e]'

    WORD = r'%s+' % ALPHABET_NUMERIC
    WORD_OR_WORDS = r'%s( +%s)*' % (WORD, WORD)
    WORDS = r'%s( +%s)+' % (WORD, WORD)

    MIXED_WORD = '%s+' % GRAPH
    MIXED_WORD_OR_WORDS = '%s( +%s)*' % (MIXED_WORD, MIXED_WORD)
    MIXED_WORDS = '%s( +%s)+' % (MIXED_WORD, MIXED_WORD)

    NON_WHITESPACE = r'\S'
    NON_WHITESPACES = r'%s+' % NON_WHITESPACE
    NON_WHITESPACES_OR_GROUP = r'%s( +%s)*' % (NON_WHITESPACES, NON_WHITESPACES)
    NON_WHITESPACES_GROUP = r'%s( +%s)+' % (NON_WHITESPACES, NON_WHITESPACES)
