import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _

# Acceptable mobile number format:
#   - Exactly 11 digits
#   - Starts with '09'
mobile_regex = RegexValidator(regex=r'^\+?09?\d{10}$',
                              message=_(
                                  'Phone number must be entered in the format:'
                                  " '09123456789'. Only 11 digits allowed."))


# Acceptable national ID format:
#   - Exactly 11 digits
#   - Meets validation criteria
def validate_national_ID(input: str):
    if input.isdecimal() is False:
        raise ValidationError(_('National ID must contain only numbers.'), )
    elif not re.search(r'^\d{10}$', input):
        raise ValidationError(_('National ID must have exactly 10 digits.'), )
    elif not is_valid(input):
        raise ValidationError(_('National ID is invalid.'), )
    else:
        return True


# Inspired by: https://gist.github.com/ebraminio/5292017
def is_valid(input: str):
    check = int(input[9])
    s = sum([int(input[x]) * (10 - x) for x in range(9)]) % 11
    validation = check == s if s < 2 else check + s == 11
    return validation
