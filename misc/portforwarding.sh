#!/bin/bash
# This script connects to a public machine and tunnels port 6680 for the public API
# to the client machine on which this script is executed.
#
# ssh -R 0.0.0.0:6680:127.0.0.1:6680 gtc
# 0.0.0.0 - Address to which the remote server listens (0.0.0.0 for all)
# 6680 - Remote port that is opened on the server
# 127.0.0.1 - Local address to which remote packets are forwarded
# 6680 - Local port on which the server runs (machine on which the script is executed)
# gtc - Shortcut from SSH client config. Can also be: user@hostname.tld
# 
# Tunnel is open as long as the ssh connection is alive. 

ssh -R 0.0.0.0:6680:127.0.0.1:6680 gtc
