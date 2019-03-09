# from kivy.lang import Builder
from kivy.lang import Parser
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
import unittest


condition_rule = """
<ConditionContainingWidget>:
    if self.cond:
        Label:
            text: 'Condition True'
    else:
        Label:
            text: 'Condition False'
"""


class ConditionContainingWidget(Widget):
    cond = BooleanProperty(True)


loop_rule = """
<LoopContainingWidget>:
    for item in self.items:
        Label:
            text: item.text
"""


class ListItem(object):

    def __init__(self, text):
        self.text = text


class LoopContainingWidget(Widget):
    items = ListProperty([ListItem('1'), ListItem('2')])


class LangFlowTestCase(unittest.TestCase):

    def test_parse_condition(self):
        parser = Parser(content=condition_rule)
