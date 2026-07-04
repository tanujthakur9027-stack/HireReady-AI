import io
import contextlib


def run_python(code):

    output = io.StringIO()

    safe_globals = {
        "__builtins__": {
            "print": print,
            "range": range,
            "len": len,
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "enumerate": enumerate,
            "zip": zip,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "sorted": sorted
        }
    }

    try:

        with contextlib.redirect_stdout(output):

            exec(code, safe_globals)

        return True, output.getvalue()

    except Exception as e:

        return False, str(e)