import random
import string


__all__ = ['generate_link_id']


def generate_link_id(
        chars: str = string.ascii_uppercase + string.digits,
        size: int = 16):
    return ''.join(random.SystemRandom().choice(chars)
                   for _ in range(size))
