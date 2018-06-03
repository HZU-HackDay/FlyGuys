#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author homeway
# @Link http://homeway.me
# @Github https://github.com/grasses
# @Version 2018.06.03

'''
Socket服务端，用于FlyGuys数据传输，联合了蓝牙模块
'''
import json, threading, time, syslog, sys, serial, random
from websocket_server import WebsocketServer

msg = {"status": 1, "data": "", "type": "server"}
bluetooth_port = "/dev/tty.LIU_01-DevB"
music_list = ["maliao", "morning_energy", "hdl", "bg"]

def new_client(client, server):
	msg["data"] = "=> New client, id={:d}".format(client['id'])
	server.send_message_to_all(json.dumps(msg))
	print(msg)

def client_left(client, server):
	msg["data"] = "=> Client({:d}) disconnected".format(client['id'])
	server.send_message_to_all(json.dumps(msg))
	print(msg)

def send_to_all(server, message):
	print("=> {:s}".format(message))
	server.send_message_to_all(json.dumps(message))

def message_received(client, server, message):
	try:
		recv_msg = json.loads(message)
		if recv_msg["type"] == "arduino":
			msg["data"] = recv_msg["data"]
			server.send_message_to_all(json.dumps(msg))
		elif recv_msg["type"] == "web":
			msg["data"] = "=> recv_msg from web: " + recv_msg["data"]
			server.send_message(client, json.dumps(msg))
	except:
		server.send_message(client, message)
	print("=> Client(%d) said: %s" % (client['id'], message))

def send_heatbeat(server):
	data = ["left", "right"]
	msg = {"status": 1, "data": data[0], "type": "server"}
	print("=> start send_heatbeat threading...")

	count = 0
	while True:
		msg["data"] = data[count % 2]
		send_to_all(server, msg)
		count += 1
		time.sleep(2)

def bluetooth(server):
	bluetooth_serial = serial.Serial(bluetooth_port, 9600, timeout=1)
	while bluetooth_serial.inWaiting():
		time.sleep(0.3)
		print("=> wait Bluetooth available...")

	send = ""
	time.sleep(1.5)
	last_one_action = "K"

	while (True):
		send = "Everything Ok, time={:d}\n".format(int(time.time()))
		bluetooth_serial.flush()
		send = str(send)

		count = 0
		check_times = 5
		not_send = False
		count += 1
		recv_msg = bluetooth_serial.readline().strip('\n\r')
		if recv_msg != "":
			print ("<= From arduino: {:s}".format(recv_msg))
			msg["type"] = "server"
			
			if recv_msg == "U":
				msg["data"] = "up"
				try:
					send_to_all(server, msg)
				except:
					print("ERROR1_UP")
			elif recv_msg == "D":
				msg["data"] = "down"
				try:
					send_to_all(server, msg)
				except:
					print("ERROR1_DOWN")

			elif recv_msg == "L":
				msg["data"] = "left"
				try:
					send_to_all(server, msg)
				except:
					print("ERROR1_LEFT")

			elif recv_msg == "R":
				msg["data"] = "right"
				try:
					send_to_all(server, msg)
				except:
					print("ERROR1_RIGHT")

			elif recv_msg == "X":
				msg["data"] = "null"
				try:
					send_to_all(server, msg)
				except:
					print("ERROR1_NULL")

			elif (recv_msg == "K"):
				if str(last_one_action) != str("K"):
					msg["type"] = "music"
					msg["data"] = str(music_list[int(random.randint(0, 3))])
				else:
					msg["type"] = "server"
					msg["data"] = "up"
				try:
					send_to_all(server, msg)
				except:
					print("ERROR1_K")
			last_one_action = recv_msg
		else:
			print("NULL")

def main():
	PORT = 9001
	server = WebsocketServer(PORT, "0.0.0.0")
	server.set_fn_new_client(new_client)
	server.set_fn_client_left(client_left)
	server.set_fn_message_received(message_received)

	'''
	t = threading.Thread(target=send_heatbeat, args=(server, ), name='LoopThread')
	t.start()
	'''
	t = threading.Thread(target=bluetooth, args=(server, ), name='Bluetooth')
	t.start()
	server.run_forever()

if __name__ == "__main__":
	main()