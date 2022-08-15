
class PATTERN:

    ANYTHING = '.'
    ANYTHING_BUT = '.?'
    SOMETHING = '.*'
    EVERYTHING = '.+'

    SPACE = ' '
    SPACES = ' +'
    SPACE_BUT = ' ?'
    SPACES_BUT = ' *'
    SPACE_AT_END_OF_STR = ' $'
    SPACES_AT_END_OF_STR = ' +$'

    WHITESPACE = r'\s'
    WHITESPACES = r'\s+'
    WHITESPACES_BUT = r'\s*'

    CRNL = r'[\r\n]'
    CR_NL = CRNL
    MULTI_CRNL = r'[\r\n]+'
    MULTI_CRNL_BUT = r'[\r\n]*'

    DIGIT = '[0-9]'
    DIGITS = '%s+' % DIGIT

    NUMBER = '[0-9]*[.]?[0-9]+'
    MIXED_NUMBER = r'[\(+-]?[0-9]*[.]?[0-9]+[)]?'

    LETTER = '[a-zA-Z]'
    LETTERS = '%s+' % LETTER

    ALPHABET_NUMERIC = '[a-zA-Z0-9]'

    SYMBOL = r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]'
    SYMBOLS = '%s+' % SYMBOL
    SYMBOLS_GROUP = '%s( +%s)+' % (SYMBOLS, SYMBOLS)

    GRAPH = r'[\x21-\x7e]'

    WORD = r'\w+'
    WORDS = r'%s( %s)*' % (WORD, WORD)
    FLEX_WORDS = r'%s( +%s)*' % (WORD, WORD)
    MIXED_WORD = '%s+' % GRAPH
    MIXED_WORDS = '%s( %s)*' % (MIXED_WORD, MIXED_WORD)
    MIXED_FLEX_WORDS = '%s( +%s)*' % (MIXED_WORD, MIXED_WORD)
