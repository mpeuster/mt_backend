mt_backend
==================
Code of master thesis project (backend part)
Also used for GT demo.

Contact: peuster [at] mail.upb.de

#### Contents:
 * /ap_manager: UPB Access Point management component (same as MobiMesh's component, but only for tests)
 * /controller: Backend controller + API server
 * /misc: e.g. development client (e.g. for debugging)

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



### Run the backend controller without access points

 1. Start management daemon: <code>$ python mnt2d.py -a start</code>
 2. Start API server: <code>$ python mnt2api.py -a start</code>

 Now the backend API will be available at http://127.0.0.1:6680/.

 API description: https://github.com/mobimesh/GTDemo-2015/wiki/Controller-Interface-Description

 However, there are no access point definitions in the system since no access point management component is connected.

### Run the backend controller with access points



### Log outputs:
* /tmp/mnt2d.log
* /tmp/mnt2api.log