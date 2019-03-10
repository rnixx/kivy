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


###############################################################################
# Tests
###############################################################################

class LangFlowTestCase(unittest.TestCase):

    def test_elif_without_related_if(self):
        try:
            Parser.debugger = True
            Parser(content=elif_without_related_if)
            self.fail('Expected to fail')
        except ParserException as e:
            self.assertTrue(str(e).find('elif without related if') > -1)

    def test_else_without_related_if(self):
        try:
            Parser.debugger = True
            Parser(content=else_without_related_if)
            self.fail('Expected to fail')
        except ParserException as e:
            # import pdb; pdb.set_trace()
            self.assertTrue(str(e).find('else without related if') > -1)


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
