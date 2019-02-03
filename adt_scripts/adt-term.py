import argparse
from util import *

def argHandler():
    parser = argparse.ArgumentParser(description='Controll the terminal in adt.')
    subparsers = parser.add_subparsers(dest='subcmd')

    # parser for the "open" command
    parser_open = subparsers.add_parser('open', help='Open the terminal in adt.')
    parser_open.add_argument(
        '-P', '-p', '--port',
        dest='port', action ='store', type = str,
        help='assign the port to load'
    )
    parser_open.add_argument(
        '-b', '--baudrate',
        dest='baudrate', action ='store', type = int,
        default=38400,
        help='assign the baudrate'
    )
    parser_open.add_argument(
        '-i', '--id',
        dest='id', action ='store', type = int,
        default=1,
        help='assign the terminal ID to open, available num is 1, 2 \n Default is 1.'
    )

    # parser for the "close" command
    parser_close = subparsers.add_parser('close', help='Close the terminal in adt.')
    parser_close.add_argument(
        '-i', '--id',
        dest='id', action ='store', type = int,
        default=1,
        help='assign the terminal ID to close, available num is 1, 2. \n Default is 1.'
    )

    # parser for the "close" command
    parser_clear = subparsers.add_parser('clear', help='Clear the terminal in adt.')
    parser_clear.add_argument(
        '-i', '--id',
        dest='id', action ='store', type = int,
        default=1,
        help='assign the terminal ID to clear, available num is 1, 2. \n Default is 1.'
    )
    args = parser.parse_args()
    return args

def termOpen(port, baudrate, id):
    adtsh = AdtSocketHandler()
    cmd = {
        'cmd'    : AdtCmd.TERM.value,
        'subcmd' : AdtSubCmdTerm.OPEN.value,
        'port'     : port,
        'baudrate' : baudrate,
        'id'       : id
    }
    res = adtsh.send_cmd(cmd)

    if res['err']:
        print('Open port {} in terminal {} error.'.format(port, id))
        print('Error msg: {}'.format(res['msg']))

def termClose(id):
    adtsh = AdtSocketHandler()
    cmd = {
        'cmd'    : AdtCmd.TERM.value,
        'subcmd' : AdtSubCmdTerm.CLOSE.value,
        'id'     : id
    }
    res = adtsh.send_cmd(cmd)

    if res['err']:
        print('Close terminal {} error.'.format(id))
        print('Error msg: {}'.format(res['msg']))

def termClear(id):
    adtsh = AdtSocketHandler()
    cmd = {
        'cmd'    : AdtCmd.TERM.value,
        'subcmd' : AdtSubCmdTerm.CLEAR.value,
        'id'     : id
    }
    res = adtsh.send_cmd(cmd)

    if res['err']:
        print('Clear terminal {} error.'.format(id))
        print('Error msg: {}'.format(res['msg']))

def run():
    args = argHandler()
    if args.subcmd == 'open':
        termOpen(args.port, args.baudrate, args.id)
    elif args.subcmd == 'close':
        termClose(args.id)
    elif args.subcmd == 'clear':
        termClear(args.id)

if __name__ == '__main__':
    run()
