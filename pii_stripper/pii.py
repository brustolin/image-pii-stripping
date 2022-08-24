import re


CREDITCARD_REGEX = r"""
(?x)
    (?:  # vendor specific prefixes
          3[47]\d      # amex (no 13-digit version) (length: 15)
        | 4\d{3}       # visa (16-digit version only)
        | 5[1-5]\d\d   # mastercard
        | 65\d\d       # discover network (subset)
        | 6011         # discover network (subset)
    )

    # "wildcard" remainder (allowing dashes in every position because of variable length)
    ([-\s]?\d){12}
"""

EMAIL_REGEX = r"""
(?x)
    \b
        [a-zA-Z0-9.!\#$%&'*+/=?^_`{|}~-]+
        @
        [a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*
    \b
"""


def is_pii(text):
    return re.match(CREDITCARD_REGEX, text) or re.match(EMAIL_REGEX, text)
