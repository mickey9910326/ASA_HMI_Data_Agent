import zmq
import json
import argparse
import progressbar
from util import *

def argHandler():
    parser = argparse.ArgumentParser(description='tell adt to load hex into asa-series board')
    parser.add_argument('-H', '--hex',
                        dest='hexfile', action ='store', type = str,
                        help='assign hex file to be load')
    parser.add_argument('-P', '-p', '--port',
                        dest='port', action ='store', type = str,
                        help='assign the port to load')
    parser.add_argument('-s', '-S', '--set',
                        dest='set', action ='store', type = int,
                        default=0,
                        help='use existing set (1~N)')
    args = parser.parse_args()
    return args

def run():
    args = argHandler()
    print(args)
    startCmd = {
        'cmd' : AdtCmd.LOADER.value,
        'subcmd' : AdtSubCmdLoader.START.value,
        'set' : args.set,
        'hex' : args.hexfile,
        'port' : args.port
    }
    stateCmd = {
        'cmd' : AdtCmd.LOADER.value,
        'subcmd' : AdtSubCmdLoader.STATE.value,
    }

    adtsh = AdtSocketHandler()
    res = adtsh.send_cmd(startCmd)
    if res is None:
        return

    print(res)
    print(type(res))
    max = res['times']
    widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    progressbar.Counter(format='%(percentage)0.2f%%'),
    ]
    bar = progressbar.ProgressBar(max_value=max, widgets=widgets)

    times = 0
    while times != max:
        state = adtsh.send_cmd(stateCmd)
        if res is None:
            return
        times = state['times']
        bar.update(times)

if __name__ == '__main__':
    run()
