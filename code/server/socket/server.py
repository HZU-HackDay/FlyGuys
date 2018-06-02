#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author homeway
# @Link http::homeway.me
# @Github https://github.com/grasses
# @Version 2018.06.02

'''
Socket服务端，用于FlyGuys数据传输
'''
import json, threading, time
from websocket_server import WebsocketServer

msg = {"status": 1, "data": "", "type": "server"}

def new_client(client, server):
	msg["data"] = "=> New client, id={:d}".format(client['id'])
	server.send_message_to_all(json.dumps(msg))
	print(msg)

def client_left(client, server):
	msg["data"] = "=> Client({:d}) disconnected".format(client['id'])
	server.send_message_to_all(json.dumps(msg))
	print(msg)

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
		server.send_message_to_all(json.dumps(msg))
		count += 1
		time.sleep(2)

PORT=9001
server = WebsocketServer(PORT, "0.0.0.0")
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)

t = threading.Thread(target=send_heatbeat, args=(server, ), name='LoopThread')
t.start()
server.run_forever()