from dataclasses import dataclass, fields
from pylatex import Document, Command, NoEscape
from pylatex.basic import NewLine
from pylatex.base_classes import LatexObject
from pyhyperref.hyperref import FormEnvironment, HyperRefCommand
from pyhyperref.utils import Quantity

from pylatex.package import Package


class DefCommand(Command):

    def dumps(self):
        return r"\def" + super().dumps()


baseLineSkip = Command("baselineskip")


@dataclass
class HyperRefDefaults:
    heightofSubmit: str | Command = Quantity(12, "pt")
    widthofSubmit: str | Command = Quantity(2, "cm")
    heightofReset: str | Command = Quantity(12, "pt")
    widthofReset: str | Command = Quantity(2, "cm")
    heightofCheckBox: str | Command = Quantity(0.8, baseLineSkip)
    widthofCheckBox: str | Command = Quantity(0.8, baseLineSkip)
    heightofChoiceMenu: str | Command = Quantity(0.8, baseLineSkip)
    widthofChoiceMenu: str | Command = Quantity(0.8, baseLineSkip)
    heightofText: str | Command = Quantity(0.8, baseLineSkip)
    heightofTextMultiline: str | Command = Quantity(0.8, baseLineSkip)
    widthofText: str | Command = Quantity(3, "cm")


class FormDocument(Document):

    def __init__(
        self,
        default_filepath="default_filepath",
        hyperRefDefaults: HyperRefDefaults = HyperRefDefaults(),
        **kwargs,
    ):
        super().__init__(default_filepath, **kwargs)
        self.preamble.append(Package("xcolor", options="table"))

        for field in fields(HyperRefDefaults):
            name = field.name
            value = getattr(hyperRefDefaults, field.name)
            self.preamble.append(
                DefCommand("Default" + name[0].upper() + name[1:], arguments=value)
            )

        self.formVariables: list[str] = []
        self.form = FormEnvironment()

        self.append(self.form)

    def registerVariable(self, obj: LatexObject):
        if isinstance(obj, HyperRefCommand):
            name = obj.name

            if name in self.formVariables:
                raise ValueError
            self.formVariables.append(name)

    def extendForm(self, objs: list[LatexObject], newLine: bool = True):

        for obj in objs:
            self.registerVariable(obj)

        self.form.extend(objs)

        if newLine:
            self.form.append(NewLine())

    def appendForm(self, obj: LatexObject):

        self.registerVariable(obj)

        self.form.append(obj)
