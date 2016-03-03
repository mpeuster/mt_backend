#!/bin/python
import socket
import time
import argparse
import logging

BRIDGE_IP = "192.168.123.101"
BRDIGE_PORT = 8899

COMMANDS = {
    "all_on": "\x42\x00\x55",
    "all_off": "\x41\x00\x55",
    "group_on_1": "\x45\x00\x55",
    "group_off_1": "\x46\x00\x55",
    "group_on_2": "\x47\x00\x55",
    "group_off_2": "\x48\x00\x55",
    "group_on_3": "\x49\x00\x55",
    "group_off_3": "\x4A\x00\x55",
    "group_on_4": "\x4B\x00\x55",
    "group_off_4": "\x4C\x00\x55"
}


COLORS = {
    "violet": "\x00",
    "blue": "\x10",
    "lightblue": "\x20",
    "aqua": "\x30",
    "mint": "\x40",
    "lightgreen": "\x50",
    "green": "\x60",
    "lime": "\x70",
    "yellow": "\x80",
    "yelloworange": "\x90",
    "orange": "\xA0",
    "red": "\xB0",
    "pink": "\xC0",
    "fusia": "\xD0",
    "lilac": "\xE0",
    "lavendar": "\xF0"
}


def send_command(cmd_key):
    print "Sending: %s" % cmd_key
    send_udp(COMMANDS[cmd_key])


def send_udp(hex_value):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(hex_value, (BRIDGE_IP, BRDIGE_PORT))
        time.sleep(0.2)
    except:
        print "Send error!"


def turn_group_on(gid):
    if gid > 0 and gid < 5:
        send_command("group_on_%d" % gid)
    elif gid == 0:  # GID== means switch all
        send_command("all_on")
    else:
        print "Error: There is no group with ID: %d" % gid


def turn_group_off(gid):
    if gid > 0 and gid < 5:
        send_command("group_off_%d" % gid)
    elif gid == 0:  # GID== means switch all
        send_command("all_off")
    else:
        print "Error: There is no group with ID: %d" % gid


def set_color(color_name):
    print "Set color: %s" % color_name
    hex_color = COLORS[color_name]
    cmd = "\x40{0}\x55"
    send_udp(cmd.format(str(hex_color)))


def set_group_color(gid, color_name):
    turn_group_on(gid)
    set_color(color_name)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", dest="action",
                        choices=['on', 'off', 'color'],
                        help="Action which should be performed.")
    parser.add_argument("-c", "--color", dest="color",
                        choices=['blue', 'green', 'red', 'violet', 'yellow',
                                 'pink', 'lightgreen', 'lightblue'],
                        default="red", help="Color argument.")
    parser.add_argument("-g", "--group", dest="group", type=int, default=0,
                        help="Group ID (1-4), 0 = ALL")
    params = parser.parse_args()
    return params


def main():
    # parse command line parameters
    params = parse_arguments()
    if params.action == "on":
        turn_group_on(params.group)
    elif params.action == "off":
        turn_group_off(params.group)
    elif params.action == "color":
        set_group_color(params.group, params.color)
    else:
        print "Missing action argument."
        exit(1)
    print "Done."
    exit(0)

if __name__ == '__main__':
    main()
