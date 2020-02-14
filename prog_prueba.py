from ruuvitag.scanner import RuuviTagScanner
import ustruct
import struct
import math

rts = RuuviTagScanner()

def pack_temp(temp):
    """Temperature in 0.005 degrees as signed short"""
    temp_conv = round(round(temp, 2) / 0.005)
    temp_int16 = ustruct.pack('!h', temp_conv)
    return temp_int16


def pack_hum(hum):
    """Humidity in 0.0025 percent as unsigned short"""
    hum_conv = round(round(hum, 2) / 0.0025)
    hum_int16 = ustruct.pack('!H', hum_conv)
    return hum_int16

def returnRuuvi2():
	for ruuvitag in rts.find_ruuvitags(timeout=10):
		if ruuvitag:
			print(ruuvitag)
			print(ruuvitag.temperature)
			print(ruuvitag.humidity)
			#id_payload = ruuvitag.mac.encode()
			temp_payload = pack_temp(ruuvitag.temperature)
			hum_payload = pack_hum(ruuvitag.humidity)
			payload = temp_payload + hum_payload
			print(payload)
			return payload
	return 0

def returnRuuvi():
	for ruuvitag in rts.find_ruuvitags(timeout=20):
		if ruuvitag:
			print(ruuvitag)
			print(ruuvitag.temperature, ruuvitag.humidity)
			#print(ruuvitag.humidity)
			temp=int(math.floor(ruuvitag.temperature*100))
			hum=int(math.floor(ruuvitag.humidity*100))
			print(temp,hum)
			payload = struct.pack('>h',temp) + struct.pack('>H',hum)
			print(payload)
			return payload
		else:
			print(ruuvitag)
	return ustruct.pack(">f", 0)
	#return returnRuuvi() no se puede usar recursividad, da stack overflow
