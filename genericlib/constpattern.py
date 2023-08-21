from .refpattern import REF_PATTERN

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

    # DIGIT = '[0-9]'
    # DIGITS = '%s+' % DIGIT
    DIGIT = REF_PATTERN.digit
    DIGITS = REF_PATTERN.digits

    # NUMBER = '[0-9]*[.]?[0-9]+'
    # MIXED_NUMBER = r'[+\(\[\$-]?(\d+([,:/-]\d+)*)?[.]?\d+[\]\)%a-zA-Z]*'
    NUMBER = REF_PATTERN.number
    MIXED_NUMBER = REF_PATTERN.mixed_number

    # LETTER = '[a-zA-Z]'
    # LETTERS = '%s+' % LETTER
    LETTER = REF_PATTERN.letter
    LETTERS = REF_PATTERN.letters

    # ALPHABET_NUMERIC = '[a-zA-Z0-9]'
    ALPHABET_NUMERIC = REF_PATTERN.alphanumeric

    # PUNCT = r'[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]'
    PUNCT = REF_PATTERN.punctuation
    PUNCTS = '%s+' % PUNCT
    PUNCTS_OR_PHRASE = '%s( %s)*' % (PUNCTS, PUNCTS)
    PUNCTS_OR_GROUP = '%s( +%s)*' % (PUNCTS, PUNCTS)
    PUNCTS_PHRASE = '%s( %s)+' % (PUNCTS, PUNCTS)
    PUNCTS_GROUP = '%s( +%s)+' % (PUNCTS, PUNCTS)
    CHECK_PUNCT = '%s$' % PUNCT
    CHECK_PUNCTS = '%s$' % PUNCTS
    CHECK_PUNCTS_GROUP = ' *%s *$' % PUNCTS_GROUP

    SPACE_PUNCT = r'[ \x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]'
    MULTI_SPACE_PUNCTS = '%s+' % SPACE_PUNCT

    # GRAPH = r'[\x21-\x7e]'
    GRAPH = REF_PATTERN.graph

    # WORD = r'%s+' % ALPHABET_NUMERIC
    WORD = REF_PATTERN.word
    WORDS = r'%s( %s)*' % (WORD, WORD)
    PHRASE = r'%s( %s)+' % (WORD, WORD)
    WORD_OR_GROUP = r'%s( +%s)*' % (WORD, WORD)
    WORD_GROUP = r'%s( +%s)+' % (WORD, WORD)

    # MIXED_WORD = '%s+' % GRAPH
    MIXED_WORD = REF_PATTERN.mixed_word
    MIXED_WORDS = '%s( %s)*' % (MIXED_WORD, MIXED_WORD)
    MIXED_PHRASE = '%s( %s)+' % (MIXED_WORD, MIXED_WORD)
    MIXED_WORD_OR_GROUP = '%s( +%s)*' % (MIXED_WORD, MIXED_WORD)
    MIXED_WORD_GROUP = '%s( +%s)+' % (MIXED_WORD, MIXED_WORD)

    NON_WHITESPACE = REF_PATTERN.non_whitespace
    NON_WHITESPACES = r'%s+' % NON_WHITESPACE
    NON_WHITESPACES_OR_PHRASE = r'%s( %s)*' % (NON_WHITESPACES, NON_WHITESPACES)
    NON_WHITESPACES_PHRASE = r'%s( %s)+' % (NON_WHITESPACES, NON_WHITESPACES)
    NON_WHITESPACES_OR_GROUP = r'%s( +%s)*' % (NON_WHITESPACES, NON_WHITESPACES)
    NON_WHITESPACES_GROUP = r'%s( +%s)+' % (NON_WHITESPACES, NON_WHITESPACES)
