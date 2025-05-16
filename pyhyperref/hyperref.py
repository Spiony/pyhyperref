from pylatex.utils import NoEscape
from pylatex.base_classes import (
    Command,
    Environment,
    CommandBase,
    SpecialArguments,
)
from pylatex.base_classes.command import Options, Arguments
from pylatex.package import Package

from pyhyperref.utils import Quantity


class FormEnvironment(Environment):
    _latex_name = "Form"
    packages = [Package("hyperref")]


class HyperRefCommand(CommandBase):
    packages = [Package("hyperref")]
    _name: str = None

    @property
    def latex_name(self):
        """Return the name of the class used in LaTeX."""
        return self.__class__.__name__ if not self._latex_name else self._latex_name

    @property
    def name(self):
        """Name of the variable"""
        return self._name


class CheckBox(HyperRefCommand):

    def __init__(self, name, label=""):

        self._name = name

        super().__init__(
            options=Options(
                # "checked",
                name=name,
                height="3mm",
                width="3mm",
            ),
            extra_arguments=SpecialArguments(label),
        )


class ChoiceMenu(HyperRefCommand):

    def __init__(
        self,
        name: str,
        choices: list[str],
        label: str = "",
        width: str = Quantity(0.8, Command("linewidth")).dumps(),
    ):
        self._name = name

        opt = Options("combo", name=name)
        # opt = Options("print", "combo", name=name, width=width)
        opt.escape = False

        super().__init__(
            options=opt,
            extra_arguments=Arguments(label, ",".join(choices)),
        )


class RadioButtons(HyperRefCommand):
    _latex_name = "ChoiceMenu"

    def __init__(self, name, choices, label=""):

        self._name = name

        opt = Options(
            "radio",
            align=2,
            bordercolor=Arguments(" ".join(["0", "0", "0"])).dumps(),
            radiosymbol=r"\ding{108}",
            # height="9pt",
            height="3mm",
            width="4mm",
            default=-1,
            name=name,
        )
        opt.escape = False
        super().__init__(
            options=opt,
            extra_arguments=Arguments(label, ",".join(choices)),
        )


class TextField(HyperRefCommand):

    def __init__(self, name, label, width=None):
        self._name = name
        opts = {"name": name}

        if width:
            opts["width"] = width

        opt = Options(**opts)

        super().__init__(
            options=opt,
            extra_arguments=Arguments(label),
        )
