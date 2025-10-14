from typing import Any, Callable


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Transforms a function into a curried version.
    
    Args:
        function: The function to be curried
        arity: The number of arguments the function expects
        
    Returns:
        A curried version of the input function
    """
    # Handle exceptions
    if len(function(*args)) != arity:
        raise ValueError('Invalid number of arguments')
    if arity < 0:
        raise ValueError('Arity have to be positive')
    def curry(*args: Any) -> Any:
        # If enough arguments have been accumulated, call the original function
        if arity <= len(args):
            return function(*args)
        else:
            # Otherwise return a new function that remembers current arguments
            def new(*new_args: Any) -> Any:
                all_ar = args + new_args
                return curry(*all_ar)
            return new

    return curry


def uncurry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Transforms a curried function back into normal form.
    
    Args:
        function: The curried function to uncurry
        arity: The number of arguments the original function expected
        
    Returns:
        An uncurried version of the input function
    """
    # Handle exceptions
    if len(function(*args)) != arity:
        raise ValueError('Invalid number of arguments')
    if arity < 0:
        raise ValueError('Arity have to be positive')
    def uncurry(*args: Any) -> Any:
        # Sequentially apply all arguments to the curried function
        res = function
        for ar in args:
            res = res(ar)
        return res

    return uncurry
