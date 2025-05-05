from pylatex.base_classes import Command

from pyhyperref.hyperref import HyperRefCommand, RadioButtons


class TextQuestion(HyperRefCommand):

    def __init__(self, question, variable, answers):
        self.question = question
        self.variable = variable
        self.answers = answers

        self._name = variable

    def dumps(self):
        questionString = ""

        questionString += self.question
        btn = RadioButtons(self.variable, self.answers)
        questionString += Command("hfil").dumps()
        questionString += btn.dumps()
        questionString += Command("hfil").dumps()

        return questionString


class RadioQuestion(HyperRefCommand):

    def __init__(self, question, variable, answers):
        self.question = question
        self.variable = variable
        self.answers = answers

        self._name = variable

    def dumps(self):
        questionString = ""

        questionString += self.question
        btn = RadioButtons(self.variable, self.answers)
        questionString += Command("hfil").dumps()
        questionString += btn.dumps()
        questionString += Command("hfil").dumps()

        return questionString
