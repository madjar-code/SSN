import hashlib
from urllib.parse import urlencode
from typing import TypeAlias


SizeString: TypeAlias = str
URLString: TypeAlias = str


def get_gravatar(email: str, size: SizeString = '200') -> URLString:
    """Return Gravatar link from email"""
    
    gravatar_url: URLString = "//www.gravatar.com/avatar/" + \
        hashlib.md5(email.encode('utf-8')).hexdigest() + '?'
    gravatar_url += urlencode({'d': 'retro', 's': str(size)})

    return gravatar_url