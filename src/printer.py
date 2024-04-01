import enum


class term_colors(enum.Enum):
    """
    Class to define colors for the terminal output

    Attributes:
    -----------
    BLUE : str
        The color for the blue text.
    GREEN : str
        The color for the green text.
    YELLOW : str
        The color for the yellow text.
    RED : str
        The color for the red text.
    PURPLE : str
        The color for the purple text.
    YELLOW : str
        The color for the purple text.
    RESET : str
        The color for resetting the text color.
    BOLD : str
        The color for bold text.
    """

    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[33m"
    RED = "\033[91m"
    PURPLE = "\033[95m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
