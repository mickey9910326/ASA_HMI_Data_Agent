from asa_hmi_data_agent.cli_tools.commands import *
from asa_hmi_data_agent.cli_tools.socket_handler import SocketHandler

import argparse
import progressbar
import time

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
    startCmd = {
        'cmd': AdtCmd.LOADER.value,
        'subcmd': AdtSubCmdLoader.START.value,
        'port': args.port,
        'hexfile': args.hexfile,
        'set': args.set
    }
    stateCmd = {
        'cmd' : AdtCmd.LOADER.value,
        'subcmd' : AdtSubCmdLoader.STATE.value,
    }

    adtsh = SocketHandler()
    res = adtsh.send_cmd(startCmd)
    if res is None:
        print('error!')
        return
    max = res['max']

    widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    progressbar.Counter(format='%(percentage)0.2f%%'),
    ]
    bar = progressbar.ProgressBar(max_value=max, widgets=widgets)

    times = 0
    while times != max:
        time.sleep(0.01)
        res = adtsh.send_cmd(stateCmd)
        if res is None:
            print('error!')
            return
        times = res['times']
        bar.update(times)

if __name__ == '__main__':
    run()
