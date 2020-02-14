import binascii
import machine
import micropython
import pycom
import socket
import struct
import sys
import time

#Importamos la clase que coge los datos del ruuvi
from prog_prueba import returnRuuvi

from network import LoRa
from pysense import Pysense
from SI7006A20 import SI7006A20 		# Humidity and Temperature Sensor
from LTR329ALS01 import LTR329ALS01 	# Digital Ambient Light Sensor
from raw2lux import raw2Lux             # ... additional library for the light sensor

RED = 0xFF0000
YELLOW = 0xFFFF33
GREEN = 0x007F00
OFF = 0x000000
def flash_led_to(color=GREEN, t1=1):
    pycom.rgbled(color)
    time.sleep(t1)
    pycom.rgbled(OFF)


# SET HERE THE VALUES OF YOUR APP AND DEVICE
THE_DEV_EUI = '70B3D549904816D5'
THE_APP_EUI = '70B3D57ED002854D'
THE_APP_KEY = 'B8B577EDBF0EABC27A368C5C37735D9A'


def join_lora(force_join = False):
    '''Joining The Things Network '''
    print('Joining TTN')

    # restore previous state
    if not force_join:
        lora.nvram_restore()

    if not lora.has_joined() or force_join == True:

        # create an OTA authentication params
        app_eui = binascii.unhexlify(THE_APP_EUI.replace(' ','')) # these settings can be found from TTN
        app_key = binascii.unhexlify(THE_APP_KEY.replace(' ','')) # these settings can be found from TTN
        dev_eui = binascii.unhexlify(THE_DEV_EUI.replace(' ',''))
        # join a network using OTAA if not previously done
        lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
        #lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

        # wait until the module has joined the network
        while not lora.has_joined():
            time.sleep(2.5)
            print('not yet joined...')

        # saving the state
        lora.nvram_save()

        # returning whether the join was successful
        if lora.has_joined():
            flash_led_to(GREEN)
            print('LoRa Joined')
            return True
        else:
            flash_led_to(RED)
            print('LoRa Not Joined')
            return False

    else:
        return True

pycom.heartbeat(False) # Disable the heartbeat LED

# Let's see if you inserted the required data
if THE_APP_EUI == 'VOID':
	print("You must set the values of your app and device first!!")
	sys.exit()

# Getting the LoRa MAC
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("Device LoRa MAC:", binascii.hexlify(lora.mac()))

flash_led_to(YELLOW)
# joining TTN
join_lora(True)

py = Pysense()
tempHum = SI7006A20(py)
ambientLight = LTR329ALS01(py) 

while True:
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
    s.setblocking(True)

    temperature = tempHum.temperature()
    humidity = tempHum.humidity()
    luxval = raw2Lux(ambientLight.light())
    print(temperature,humidity,luxval)

    #print("Read sensors: temp. {} hum. {} lux: {}".format(temperature, humidity, luxval)) #mt 11/02/2020
    # Packing sensor data as byte sequence using 'struct'
    # Data is represented as 3 float values, each of 4 bytes, byte orde 'big-endian'
    # for more infos: https://docs.python.org/3.6/library/struct.html
    sensorLopy = struct.pack(">fff", temperature, humidity, luxval) #mt 11/02/2020
    print(sensorLopy)
    aux = returnRuuvi() #mt 11/02/2020
    #[x]= struct.unpack(">f", aux) #mt 11/02/2020
    #payload= struct.pack(">f", aux)
    print(aux)
    #print(payload)
    s.send(aux)
    flash_led_to(GREEN)

    time.sleep(30)
