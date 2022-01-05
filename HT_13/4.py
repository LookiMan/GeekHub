"""
4. Видозмініть програму так, щоб метод __init__ мався в класі «геометричні фігури» 
та приймав кольор фігури при створенні екземпляру, а методи __init__ підкласів доповнювали його та додавали початкові розміри.

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
    set_color(new_color: str) -> None
        Set new figure color
    """

    def __init__(self, color: str) -> None:
        """
        Parameters
        ----------

        color : str
            color of the figure
        """

        self.color = color

    def set_color(self, new_color: str) -> None:
        """
        Set new figure color

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

    def __init__(self, color: str, radius: int) -> None:
        """
        Parameters
        ----------
        color : str
            color of the figure
        radius : int
            oval radius
        """

        super().__init__(color)
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

    def __init__(self, color: str, side: int) -> None:
        """
        Parameters
        ----------
        color : str
            color of the figure
        side : int
            square side
        """

        super().__init__(color)
        self.side = side
