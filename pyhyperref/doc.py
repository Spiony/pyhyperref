from dataclasses import dataclass, fields
from pylatex import Document, Command, NoEscape
from pylatex.basic import NewLine
from pylatex.base_classes import LatexObject
from pyhyperref.hyperref import FormEnvironment, HyperRefCommand

from pylatex.package import Package


class DefCommand(Command):

    def dumps(self):
        return r"\def" + super().dumps()


@dataclass
class HyperRefDefaults:
    heightofSubmit: str = "12pt"
    widthofSubmit: str = "2cm"
    heightofReset: str = "12pt"
    widthofReset: str = "2cm"
    heightofCheckBox: str = r"0.8\baselineskip"
    widthofCheckBox: str = r"0.8\baselineskip"
    heightofChoiceMenu: str = r"0.8\baselineskip"
    widthofChoiceMenu: str = r"0.8\baselineskip"
    heightofText: str = r"\baselineskip"
    heightofTextMultiline: str = r"4\baselineskip"
    widthofText: str = "3cm"


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
                DefCommand(
                    "Default" + name[0].upper() + name[1:], arguments=NoEscape(value)
                )
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
