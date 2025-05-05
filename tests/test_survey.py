import unittest
from pylatex import Document, Command
from pyhyperref.hyperref import (
    CheckBox,
    ChoiceMenu,
    RadioButtons,
    TextField,
)
from pyhyperref.doc import FormDocument, HyperRefDefaults

from pylatex.basic import LineBreak, NewLine
from pylatex import Section
from pylatex.basic import LineBreak

from pyhyperref.elements import RadioQuestion


from dataclasses import dataclass


@dataclass
class Survey:
    room: str
    cleanliness: int
    quietness: int
    nurses: int
    eggs: bool
    breakfast_grains: bool
    fruit: bool
    yogurt: bool

    def __post_init__(self):
        self.cleanliness = int(self.cleanliness)
        self.quietness = int(self.quietness)
        self.nurses = int(self.nurses)


if __name__ == "__main__":

    doc = FormDocument(
        "test",
        hyperRefDefaults=HyperRefDefaults(
            heightofText="9pt",
            widthofText="5cm",
        ),
    )

    doc.extendForm(
        [
            Section("General"),
            "Select bedroom option: ",
            ChoiceMenu("room", ["single bedroom", "shared bedroom"]),
        ]
    )

    doc.extendForm(
        [
            Section("Questions"),
            RadioQuestion(
                "How would you rate the cleanliness of the hospital?",
                "cleanliness",
                [str(i + 1) for i in range(4)],
            ),
            LineBreak(),
            RadioQuestion(
                "Was your room quiet at night?",
                "quietness",
                [str(i + 1) for i in range(4)],
            ),
            LineBreak(),
            RadioQuestion(
                " Did doctors and nurses listen carefully to you? ",
                "nurses",
                [str(i + 1) for i in range(4)],
            ),
            LineBreak(),
        ]
    )

    doc.extendForm(
        [
            Section("Multiple Choice"),
            CheckBox("mp:eggs"),
            "Eggs (scrambled, boiled, omelet)",
            NewLine(),
            CheckBox("mp:breakfast_grains"),
            "Cereal or oatmeal",
            NewLine(),
            CheckBox("mp:fruit"),
            "Fresh fruit",
            NewLine(),
            CheckBox("mp:yogurt"),
            "Yogurt or smoothies ",
        ]
    )

    doc.extendForm(
        [
            Section("Text answers"),
            TextField("tx:name", label="Name:"),
            NewLine(),
            TextField("tx:city", label="City:", width="5cm"),
        ]
    )

    print(doc.formVariables)

    doc.generate_pdf(clean=True, clean_tex=False)
