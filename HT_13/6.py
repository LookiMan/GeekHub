"""
6. Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.
"""


class Factory(object):
    """

    Attributes
    ----------
    _amount_instances : int
        variable class instance counter

    Methods
    -------
    amount_instances(cls) -> int
        Returns the number of instances of the Factory class
    """

    _amount_instances = 0

    def __init__(self) -> None:
        type(self)._amount_instances += 1

    def __del__(self) -> None:
        type(self)._amount_instances -= 1

    @classmethod
    def amount_instances(cls) -> int:
        """
        Returns
        -------
        int
            Returns the number of instances of the Factory class
        """

        return cls._amount_instances
