#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Author homeway
# @Link http::homeway.me
# @Github https://github.com/grasses
# @Version 2018.06.02

'''
Socket服务端，用于FlyGuys数据传输
'''
import json
from websocket_server import WebsocketServer

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("=> New client connected and was given id %d" % client['id'])
	server.send_message_to_all("Hey all, a new client has joined us")

def client_left(client, server):
	print("=> Client(%d) disconnected" % client['id'])

def message_received(client, server, message):
	data = {"status": 1, "data": message, "type": "server"}

	try:
		recv_msg = json.loads(message)
		if recv_msg["type"] == "arduino":
			data["data"] = recv_msg["data"]
			server.send_message_to_all(json.dumps(data))
		elif recv_msg["type"] == "web":
			data["data"] = "=> recv_msg from web: " + recv_msg["data"]
			server.send_message(client, json.dumps(data))
	except:
		server.send_message(client, message)
	print("=> Client(%d) said: %s" % (client['id'], message))


PORT=9001
server = WebsocketServer(PORT, "0.0.0.0")
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
