#!/bin/bash
#
# Script to simplify start/stop of demo backend.
#

function execute()
{
	echo "Executing" $1
	cd ap_manager
	python upb_apmanager.py -a $1 -c $2
	sleep 1
	cd ../controller
	python tlnb_ctrl.py -a $1 -c $2
	python tlnb_api.py -a $1 -c $2
	sleep 2
	cd ../led_manager
	python led_manager.py -a $1 -c $2
	echo "done."
}


case "$1" in
	start*)
		execute $1 $2
	;;
	stop*)
		execute $1 $2
	;;
	restart*)
		execute $1 $2
	;;
	status*)
		execute $1 $2
	;;
	*)
		echo "Usage: $(basename $0) start|stop|restart [config.json]"
	;;
esac