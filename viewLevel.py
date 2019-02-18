#!/usr/bin/python
# Example file with custom commands, located at /magical/commands/example.py

import lldb
import fblldbbase as fb
import pdb


def lldbcommands():
    return [PrintViewLevel()]


class PrintViewLevel(fb.FBCommand):
    def name(self):
        return 'pviewlevel'

    def description(self):
        return 'View in subviews level.'

    def args(self):
        return [
            fb.FBCommandArgument(arg='subviews', type='UIView *', help='This is subviews.'),
            fb.FBCommandArgument(arg='view', type='UIView *', help='This is view')
        ]


#   def options(self):
#     return [
#       fb.FBCommandArgument(short='-s', long='--subviews', arg='color', type='string', default='red', help='A color name such as \'red\', \'green\', \'magenta\', etc.'),
#       fb.FBCommandArgument(short='-w', long='--width', arg='width', type='CGFloat', default=2.0, help='Desired width of border.')
#     ]

    def run(self, arguments, options):
        # It's a good habit to explicitly cast the type of all return
        # values and arguments. LLDB can't always find them on its own.
        subviews = fb.evaluateInputExpression(arguments[0])
        # subviews = subviewsOfView(selfView)
        view = fb.evaluateInputExpression(arguments[1])

        index = fb.evaluateIntegerExpression('[[' + subviews + ' subviews] indexOfObject:' + view + ']')
        # index = fb.evaluateIntegerExpression('[(id)' + subviews + '.subviews indexOfObject:' + view + ']')

        # index = fb.evaluateExpression('[(UIView *)%s.subviews indexOfObject:(UIView *)%s]' % (subviews, view))

        # pdb.set_trace()
        print ('index: %d' % index)
        # lldb.debugger.HandleCommand('po [((UIView *)%s).subviews indexOfObject:((UIView *)%s)]' % (arguments[0], arguments[1]))

    def subviewsOfView(view):
        return fb.evaluateObjectExpression('[' + view + ' subviews]')
