# from kivy.lang import Builder
from kivy.lang import Parser
from kivy.lang import ParserException
# from kivy.properties import BooleanProperty
# from kivy.properties import ListProperty
# from kivy.uix.widget import Widget
import unittest


###############################################################################
# Mock objects
###############################################################################

elif_without_related_if = '''
<Widget>:
    elif self.cond:
        Label:
            text: 'Label'
'''

else_without_related_if = '''
<Widget>:
    else:
        Label:
            text: 'Label'
'''

incomplete_if = '''
<Widget>:
    if:
        Label:
            text: 'if'
'''

incomplete_elif = '''
<Widget>:
    if self.cond:
        Label:
            text: 'if'
    elif:
        Label:
            text: 'elif'
'''

incomplete_for = '''
<Widget>:
    for:
        Label:
            text: 'for'
'''

if_elif_else = '''
<Widget>:
    if self.cond_1:
        Label:
            text: 'if'
    elif self.cond_2:
        Label:
            text: 'elif'
    else:
        Label:
            text: 'else'
'''

for_loop = '''
<Widget>:
    for it in self.items:
        Label:
            text: it.text
'''

within_graphics_instructions = '''
<Widget>:
    canvas:
        if root.cond:
            Color:
                rgba: 1, 1, 1, 1
        else:
            Color:
                rgba: 0, 0, 0, 1
'''


###############################################################################
# Tests
###############################################################################

class LangFlowTestCase(unittest.TestCase):

    def test_elif_without_related_if(self):
        try:
            Parser(content=elif_without_related_if)
            self.fail('Expected to fail')
        except ParserException as e:
            self.assertTrue(str(e).find('elif without related if') > -1)

    def test_else_without_related_if(self):
        try:
            Parser(content=else_without_related_if)
            self.fail('Expected to fail')
        except ParserException as e:
            self.assertTrue(str(e).find('else without related if') > -1)

    def test_parse_incomplete_if(self):
        try:
            Parser(content=incomplete_if)
            self.fail('Expected to fail')
        except ParserException as e:
            self.assertTrue(str(e).find('Incomplete flow control statement') > -1)

    def test_parse_incomplete_elif(self):
        try:
            Parser(content=incomplete_elif)
            self.fail('Expected to fail')
        except ParserException as e:
            self.assertTrue(str(e).find('Incomplete flow control statement') > -1)

    def test_parse_incomplete_for(self):
        try:
            Parser(content=incomplete_for)
            self.fail('Expected to fail')
        except ParserException as e:
            self.assertTrue(str(e).find('Incomplete flow control statement') > -1)

    def test_parse_if_elif_else(self):
        parser = Parser(content=if_elif_else)
        children = parser.rules[0][1].children

        rule = children[0]
        self.assertEqual(rule.name, 'if')
        self.assertEqual(rule.flow_statement, 'self.cond_1')
        self.assertEqual(rule.children[0].name, 'Label')
        self.assertEqual(rule.children[0].properties['text'].value, "'if'")

        rule = children[1]
        self.assertEqual(rule.name, 'elif')
        self.assertEqual(rule.flow_statement, 'self.cond_2')
        self.assertEqual(rule.children[0].name, 'Label')
        self.assertEqual(rule.children[0].properties['text'].value, "'elif'")

        rule = children[2]
        self.assertEqual(rule.name, 'else')
        self.assertEqual(rule.flow_statement, 'True')
        self.assertEqual(rule.children[0].name, 'Label')
        self.assertEqual(rule.children[0].properties['text'].value, "'else'")

    def test_parse_for_loop(self):
        parser = Parser(content=for_loop)
        children = parser.rules[0][1].children

        rule = children[0]
        self.assertEqual(rule.name, 'for')
        self.assertEqual(rule.flow_statement, 'it in self.items')
        self.assertEqual(rule.children[0].name, 'Label')
        self.assertEqual(rule.children[0].properties['text'].value, 'it.text')

    def test_parse_within_graphics_instructions(self):
        parser = Parser(content=within_graphics_instructions)
        children = parser.rules[0][1].canvas_root.children

        rule = children[0]
        self.assertEqual(rule.name, 'if')
        self.assertEqual(rule.flow_statement, 'root.cond')
        self.assertEqual(rule.children[0].name, 'Color')
        self.assertEqual(rule.children[0].properties['rgba'].value, "1, 1, 1, 1")

        rule = children[1]
        self.assertEqual(rule.name, 'else')
        self.assertEqual(rule.flow_statement, 'True')
        self.assertEqual(rule.children[0].name, 'Color')
        self.assertEqual(rule.children[0].properties['rgba'].value, "0, 0, 0, 1")


# condition_rule = """
# <ConditionContainingWidget>:
#     if self.cond:
#         Label:
#             text: 'Condition True'
#     else:
#         Label:
#             text: 'Condition False'
# """


# class ConditionContainingWidget(Widget):
#     cond = BooleanProperty(True)


# loop_rule = """
# <LoopContainingWidget>:
#     for item in self.items:
#         Label:
#             text: item.text
# """


# class ListItem(object):

#     def __init__(self, text):
#         self.text = text


# class LoopContainingWidget(Widget):
#     items = ListProperty([ListItem('1'), ListItem('2')])
