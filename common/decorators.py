from common.utils import JsonError, errorlog, redirecterror

def test_error(fn):
    def decorator(request, *args, **kwargs):
        try:
            return fn(request, *args, **kwargs)
        except Exception as e:
            errorlog(repr(e), function=fn)
            if request.method == 'POST':
                return JsonError('Unknown error')
            else:
                return redirecterror(request, 'Unknown error')
    return decorator
