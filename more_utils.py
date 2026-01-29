import random
import string

def generate_password(length=12, include_symbols=True):
    """Generate a random password with specified length."""
    characters = string.ascii_letters + string.digits
    if include_symbols:
        characters += string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
