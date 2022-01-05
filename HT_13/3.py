"""
3. Напишіть програму, де клас «геометричні фігури» (figure) містить властивість color з початковим значенням white 
і метод для зміни кольору фігури, а його підкласи «овал» (oval) і «квадрат» (square) 
містять методи __init__ для завдання початкових розмірів об'єктів при їх створенні.
"""


class Figure(object):
    """Figure doc

    ...

    Attributes
    ----------
    color : str
        color of the figure

    Methods
    -------
    set_color(new_color: str)
        Set new figure color
    """

    color = "white"

    def set_color(self, new_color: str) -> None:
        """
        Set new color

        Parameters
        ----------
        new_color : str
            new color of the figure
        """

        self.color = new_color


class Oval(Figure):
    """Oval doc

    ...

    Attributes
    ----------
    color : str
        color of the figure
    radius : int
        oval radius

    Methods
    -------
    set_color(new_color: str)
        Set new figure color
    """

    def __init__(self, radius: int) -> None:
        """
        Parameters
        ----------
        radius : int
            oval radius
        """

        self.radius = radius


class Square(Figure):
    """Square doc

    ...

    Attributes
    ----------
    color : str
        color of the figure
    side : int
        square side

    Methods
    -------
    set_color(new_color: str)
        Set new figure color
    """

    def __init__(self, side: int) -> None:
        """
        Parameters
        ----------
        side : int
            square side
        """

        self.side = side
