import re
url_re = re.compile(r'^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?', re.IGNORECASE)
