mt_backend
==================
Code of master thesis project (backend part).

Also used for GT demo.

Contact: peuster [at] mail.upb.de

#### Contents:
* <code>controller/</code>: Backend controller + API server
* <code>ap_manager/</code>: UPB Access Point management component (same as MobiMesh's component, but for UPB testbed)
* <code>misc/</code>: e.g. development client (e.g. for debugging)

## User Guide

Tested on: Ubuntu Server 14.04 LTS

Get code from: https://github.com/mpeuster/mt_backend

### General

The backend consists of two components, the API server and the controller which are started as Unix daemons (both are placed in the 'controller/' directory):

* <code>python tlnb_api.py -a start|restart|stop</code>: two layer network backend API
* <code>python tlnb_ctrl.py -a start|restart|stop</code>: two layer network backend controller

The API server provides the public REST API to all other components of the demo testbed. It receives status updates from UEs and stores them into a central database. It also informs the controller component about changes, by using ZeroMQ messaging. The controller components uses the current system state, stored in the database and runs an optimization algorithm, which decides what APs to switch off or on, and computes the assignment between UEs and APs. These results are then written back into the database and are accessible over the public REST API (e.g. a GET request on the UE endpoint returns to which AP a specific UE is currently assigned).

The controller component also acts as a REST client and communicates with the network controller (provided by MobiMESH). It uses this connection to control the APs (e.g. black and white listing of MAC address to emulate AP switching).

All backend components can run on different physical machines. However, the example configuration file in the repository assumes that all components run on the same machine. 

### Install required packages and database

* MongoDB: <code>$ sudo apt-get install mongodb</code>
* Python PIP: <code>$ sudo apt-get install python-pip</code>
* ZeroMQ: <code>$ sudo apt-get install python-zmq</code>
* MongoEngine: <code>$ sudo pip install mongoengine</code>
* Requests: <code>$ sudo pip install requests</code>
* Tornado: <code>$ sudo pip install tornado</code>
* Flask: <code>$ sudo pip install flask</code>
* FlaskRestful (installed from sources):
  + <code>$ git clone https://github.com/twilio/flask-restful.git</code>
  + <code>$ cd flask-restful</code>
  + <code>$ sudo python setup.py develop</code>


### Install



* <code>git clone git@github.com:mpeuster/mt_backend.git</code>
* <code>cd mt_backend/controller/</code>

### Configuration
There is a central configuration file for the management daemon and the API server:

* <code>controller/config.json</code>

This file can be used e.g. to specify the location of the network management API provided by e.g. MobiMesh's management component. Furthermore, details about used access points (e.g. SSIDs/BSSIDs/Location) can be configured in this file.

### Run backend controller without access points

1. Start management daemon: <code>$ python tlnb_ctrl.py -a start</code>
2. Start API server: <code>$ python tlnb_api.py -a start</code>

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

### Log outputs:
* <code>/tmp/tlnb_ctrl.log</code>
* <code>/tmp/tlnb_api.log</code>

### Usage

When the controller and the API server are started, you can register an UE with a POST request in the system. After this you can update it's status (context) with PUT requests. During this, the controller will always compute the AP with the smallest distance to the UE and assign this AP to the UE. You can receive this assignment with a GET request on the UE endpoint. At the end the UE can be removed from the system with a DELETE request.

For detailed API documentation see: https://github.com/mobimesh/GTDemo-2015/wiki/Controller-Interface-Description

If something breaks (e.g. a UE is registered and can not be removed) you should simply restart the control daemon:

* <code>$ python tlnb_ctrl.py -a restart</code>

This will <b> clear the complete database </b> and the whole system is in an empty state again.

### Tests

You can run the API test suite with:

* <code>$ python test.py</code>

This will test most of the API's functionalities. It automatically starts the API and control component and stops them afterwards. However, if you run the system without a connected access point manager, and thus without access point definitions, one of the test cases will fail (assignment test). 




