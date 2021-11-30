"""
Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
P.S. Повинен вертатись генератор.
P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній: https://docs.python.org/3/library/stdtypes.html#range
"""


"""

https://github.com/python/cpython/blob/main/Objects/rangeobject.c

"""

def _validate_type(instance):
    if not isinstance(instance, int):
        raise TypeError(f'\'{type(instance).__name__}\' object cannot be interpreted as an integer')


def _iter_positive_range(start, stop, step):
    while start < stop:
        yield start
        
        start += step


def _iter_negative_range(start, stop, step):
    while start > stop:
        yield start
        
        start += step


def crange(*args):
    start = 0
    step = 1

    if len(args) > 0:
        _validate_type(args[0])
        stop = args[0]
        
    if len(args) > 1:
        _validate_type(args[0])
        _validate_type(args[1])

        start = args[0]
        stop = args[1]
    
    if len(args) > 2:
        _validate_type(args[2])

        step = args[2]

        if step == 0:
            raise ValueError('crange() arg 3 must not be zero')
    
    if start < stop and step > 0:
        return _iter_positive_range(start, stop, step)
    elif start > stop and step < 0:
        return _iter_negative_range(start, stop, step)
    else:
        return _iter_positive_range(0, 0, 1)


def main():
    print('range(5)')
    print('range:', list(range(5)))
    print('crange:', list(crange(5)))

    print('range(-5, 5)')
    print('range:', list(range(-5, 5)))
    print('crange:', list(crange(-5, 5)))
    
    print('range(-5, 5, 2)')
    print('range:', list(range(-5, 5, 2)))
    print('crange:', list(crange(-5, 5, 2)))

    print('\nrange(15, 30, -3)')
    print('range:', list(range(15, 30, -3)))
    print('crange:', list(crange(15, 30, -3)))
    
    print('\nrange(15, 2)')
    print('range:', list(range(15, 2)))
    print('crange:', list(crange(15, 2)))

    print('\nrange(1, 4, 6)')
    print('range:', list(range(1, 4, 6)))
    print('crange:', list(crange(1, 4, 6)))

    print('\nrange(0, -10, -1)')
    print('range:', list(range(0, -10, -1)))
    print('crange:', list(crange(0, -10, -1)))

    print('\nrange(0, 10, 0)')
    try:
        print('range:', list(range(0, 10, 0)))
    except Exception as exc:
        print(exc)
    try:
        print('crange:', list(crange(0, 10, 0)))
    except Exception as exc:
        print(exc)


if __name__ == '__main__':
    main()



