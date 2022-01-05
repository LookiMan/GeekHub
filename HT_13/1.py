"""
1. Створити клас Calc, який буде мати атребут last_result та 4 методи. 
Методи повинні виконувати математичні операції з 2-ма числами, а саме додавання, віднімання, множення, ділення.
- Якщо під час створення екземпляру класу звернутися до атребута last_result він повинен повернути пусте значення
- Якщо використати один з методів - last_result повенен повернути результат виконання попереднього методу.
- Додати документування в клас (можете почитати цю статтю: https://realpython.com/documenting-python-code/ )
"""
from typing import Optional, Union


class Calc(object):
    """The class implements four methods for adding, subtracting, multiplying and dividing two numbers

    Methods
    -------
    summa(first_number, second_number)
        returns the sum of numbers
    difference(first_number, second_number)
        returns the difference of numbers
    multiply(first_number, second_number)
        returns the result of multiplying numbers
    division(first_number, second_number)
        returns the result of dividing numbers

    last_result()
        returns the last saved calculation result

    """

    def __init__(self):
        """save last result"""

        self._last_result = None

    def summa(
        self, first_number: Union[int, float], second_number: Union[int, float]
    ) -> Union[int, float]:
        """returns the sum of numbers

        Parameters
        ----------
        first_number : int, float
            the first number to add
        second_number : int, float
            the second number to add

        Returns
        -------
        int, float
            the sum of the first and second number
        """

        self._last_result = first_number + second_number

        return self._last_result

    def difference(
        self, first_number: Union[int, float], second_number: Union[int, float]
    ) -> Union[int, float]:
        """returns the difference of numbers

        Parameters
        ----------
        first_number : int, float
            the first number to divide
        second_number : int, float
            the second number to divide

        Returns
        -------
        int, float
            the difference of the first and second number
        """

        self._last_result = first_number - second_number

        return self._last_result

    def multiply(
        self, first_number: Union[int, float], second_number: Union[int, float]
    ) -> Union[int, float]:
        """returns the result of multiplying numbers

        Parameters
        ----------
        first_number : int, float
            the first number to multiply
        second_number : int, float
            the second number to multiply

        Returns
        -------
        int, float
            the multiplying of the first and second number

        """

        self._last_result = first_number * second_number

        return self._last_result

    def division(
        self, first_number: Union[int, float], second_number: Union[int, float]
    ) -> Union[int, float]:
        """returns the result of dividing numbers

        Parameters
        ----------
        first_number : int, float
            the first number to multiply
        second_number : int, float
            the second number to multiply

        Returns
        -------
        int, float
            the division of the first and second number
        """

        if second_number == 0:
            self._last_result = "division by zero is impossible"
        else:
            self._last_result = first_number / second_number

        return self._last_result

    def last_result(self) -> Optional[Union[int, float]]:
        """return last result

        Returns
        -------
        optional union[int, float]
            returns the last saved calculation result
        """

        return self._last_result
