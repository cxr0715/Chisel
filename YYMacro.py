#!/usr/bin/python
# Example file with custom commands, located at /magical/commands/example.py

import lldb
import fblldbbase as fb
import pdb


def lldbcommands():
    return [
        GetCoreMacro(),
        GetCoreIMacro(),
        BRIDGEMacro(),
        ]


class GetCoreMacro(fb.FBCommand):
    def name(self):
        return 'GetCore'

    def description(self):
        return 'GetCore Macro'

    def args(self):
        return [
            fb.FBCommandArgument(arg='GetCore', type='string', help='This is Core Name.'),
            fb.FBCommandArgument(arg='Method', type='string', help='This is Core Method/Property Name.'),
        ]

    def run(self, arguments, options):
        # pdb.set_trace()
        object = lldb.SBCommandReturnObject()
        coreName = fb.evaluateExpression('((' + arguments[0] + ' *)[CoreManager getCore:[' + arguments[0] + ' class]])')
        result = fb.evaluateObjectExpression('(id)[' + coreName + ' %s]' % arguments[1])
        print ('result: {}'.format(result))
        print ('<{}: {}>'.format(arguments[0], coreName))
        lldb.debugger.HandleCommand('po [(%s *)%s %s]' % (arguments[0], coreName, arguments[1]))


class GetCoreIMacro(fb.FBCommand):
    def name(self):
        return 'GetCoreI'

    def description(self):
        return 'GetCoreI Macro'

    def args(self):
        return [
            fb.FBCommandArgument(arg='GetCoreI', type='string', help='This is CoreI Name.'),
            fb.FBCommandArgument(arg='Method', type='string', help='This is CoreI Method/Property Name.'),
        ]

    def run(self, arguments, options):
        # pdb.set_trace()
        coreName = fb.evaluateExpression('[CoreManager getCoreFromProtocol:(Protocol *)objc_getProtocol("'+ arguments[0] +'")]')
        print ('<{}: {}>'.format(arguments[0], coreName))
        lldb.debugger.HandleCommand('po [%s %s]' % (coreName, arguments[1]))

        
class BRIDGEMacro(fb.FBCommand):
    def name(self):
        return 'BRIDGE'

    def description(self):
        return 'BRIDGE Macro'

    def args(self):
        return [
            fb.FBCommandArgument(arg='BRIDGE', type='string', help='This is BRIDGE Name.'),
            fb.FBCommandArgument(arg='Method', type='string', help='This is BRIDGE Method/Property Name.'),
        ]

    def run(self, arguments, options):
        # pdb.set_trace()
        bridgeName = fb.evaluateExpression('[[YYBridgeSet shareInstance] getBridgeWithProtocol:(Protocol *)objc_getProtocol("' + arguments[0] + '")]')
        print ('<{}: {}>'.format(arguments[0], bridgeName))
        lldb.debugger.HandleCommand('po [%s %s]' % (bridgeName, arguments[1]))
