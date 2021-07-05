from django.core.exceptions import ValidationError

ACCEPTABLE_FILE_SIZE_LIMIT = 10485760 * 10  # 10 MB * 10 = 100 MB


def validate_file_size(file) -> None:
    limit = ACCEPTABLE_FILE_SIZE_LIMIT
    if file.size > limit:
        raise ValidationError('File too large. Size should not exceed 100 MB.')


def validate_involvement(involvement: float) -> None:
    if (involvement > 100) or (involvement < 0):
        raise ValidationError(
            'Invalid value. Involvement is in range [0, 100].')
