mt_backend
==================
Code of master thesis project (backend part).

Also used for GT demo.

Contact: peuster [at] mail.upb.de

#### Contents:
* <code>ap_manager/</code>: UPB Access Point management component (same as MobiMesh's component, but only for tests)
* <code>controller/</code>: Backend controller + API server
* <code>misc/</code>: e.g. development client (e.g. for debugging)

## User Guide

Tested on: Ubuntu Server 14.04 LTS

Get code from: https://github.com/mpeuster/mt_backend

### Install required packages and database

* MongoDB: <code>$ sudo apt-get install mongodb</code>
* Python PIP: <code>$ sudo apt-get install python-pip</code>
* ZeroMQ: <code>$ sudo apt-get install python-zmq</code>
* MongoEngine: <code>$ sudo pip install mongoengine</code>
* Tornado: <code>$ sudo pip install tornado</code>
* Flask: <code>$ sudo pip install flask</code>
* FlaskRestful (installed from sources):
  + <code>$ git clone https://github.com/twilio/flask-restful.git</code>
  + <code>$ cd flask-restful</code>
  + <code>$ sudo python setup.py develop</code>


### Configuration
There is a central configuration file for the management daemon and the API server:

* <code>controller/config.json</code>

This file can be used e.g. to specify the location of the network management API provided by e.g. MobiMesh's management component.

### Log outputs:
* <code>/tmp/mnt2d.log</code>
* <code>/tmp/mnt2api.log</code>

### Run backend controller without access points

1. Start management daemon: <code>$ python mnt2d.py -a start</code>
2. Start API server: <code>$ python mnt2api.py -a start</code>

Now the backend API will be available at http://127.0.0.1:6680/.

API description: https://github.com/mobimesh/GTDemo-2015/wiki/Controller-Interface-Description

However, there are no access point definitions in the system since no access point management component is connected.

### Run backend controller with access points

1. Configure network manager API in <code>config.json</code>:

	e.g. for UPB's AP manager component: 

	```json
	"apmanager": {
		"host": "127.0.0.1",
		"port": 6681
	},
	```

2. Start network manager component
	
	e.g. UPB's AP manager: <code>$ python upb_apmanager.py -a start</code>

3. Start management controller: <code>$ python tlnb_ctrl.py -a start</code>
4. Start API server: <code>$ python tlnb_api.py -a start</code>


