
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

    CRNL = r'[\r\n]'
    CR_NL = CRNL
    MULTI_CRNL = r'[\r\n]+'
    MULTI_CRNL_BUT = r'[\r\n]*'