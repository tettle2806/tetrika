import inspect


def strict(func):
    sig = inspect.signature(func)
    annotations = func.__annotations__

    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f"Argument '{name}' must be of type {expected_type.__name__}, got {type(value).__name__}")

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))  # >>> 3
print(sum_two(1, 2.4))  # >>> TypeError
