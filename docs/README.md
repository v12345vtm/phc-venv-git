# Project Peha
## Description
### Target
The target of the project is providing an easy to use user interface to a **Peha**networked module. This module is the core of a network that manages a numberof digital I/O which main purpose is controlling a domotica network ofelectrical devices as can be lamps, room lighting switches and other type ofcharges which can be controlled by motors, etc.
_CLARIFY THIS!!_
This interface has to provide monitoring of the current status (*ON/OFF*) ofthe outputs and allow its manual and remote control.
_GUESS:_However, the **Peha** system includes a basic program which provides to the userthe possibility to control locally the outputs, overriding the remote controlcommands.
### Technical plan
The initial idea is to build a web server which should communicate withthe **Peha** via its serial port. This  web server will provide both thecontrol of the communication stream and _simultaneously_ allow the user tosend commands via the same communication stream to specifically control anumber of outputs of the **Peha**.
This introduces a problem in the sense that the communication stream hasto attend at the same time two independent information flows:
* Retrieving data from the domotica bus controller.* Sending control data to the bus controller.
The web server will run on a **Raspberry Pi** module and will be basedin the **AIOHTTP** which provides the asynchronous behaviour required by the application character, which seems to be a good match for this case.
***WARNING***: AIOHTTP recommends the installation of the library *cchardet*which is available only up to Python 3.9!

### Details
There