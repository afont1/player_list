from my_struct import info
from my_struct import threading, time, http, json, requests
from interface import launch_interface
from server_gestion import receive_messages
from utils import is_admin, enable_proxy

def request(flow: http.HTTPFlow) -> None:
	url = flow.request.url
	if "/permission/validate" in url:
		try:
			data = json.loads(flow.request.content)
			if "Users" in data:
				for _users in data["Users"]:
					xuid = _users["Xuid"]
					if xuid.isnumeric():
						with info.xuid_list_lock:
							info.xuid_list.append(xuid)
		except Exception as e:
			print(f"Unexpected error request: {e}")
			pass
	if "https://e5ed.playfabapi.com/Event/WriteTelemetryEvents" in url:
		try:
			data = json.loads(flow.request.content)
			if "Events" in data:
				for e in data["Events"]:
					if e["Name"] == "client_connected_to_network":
						info.gamertags_list = []
						break
		except:
			pass

def response(flow: http.HTTPFlow) -> None:
	url = flow.request.url
	if "/sessionTemplates/" in url:
		try:
			data = json.loads(flow.response.content)
			properties = data["properties"]
			info.server_name = properties["system"]["matchmaking"]["serverConnectionString"]
			info.stamp_id = properties["custom"]["StampId"]
			info.server_ip = properties["custom"]["GameServerAddress"]
			print(f"Server Name: {info.server_name}, Stamp ID: {info.stamp_id}, Server IP: {info.server_ip}")
		except Exception as e:
			print(f"Unexpected error response: {e}")
			pass

def routine():
	while not info.stop_event_routine.is_set():
		time.sleep(1)
		with info.xuid_list_lock:
			if len(info.xuid_list) >= 1:
				if info.previous_server_ip is not None:
					info.is_same_server = (info.server_ip == info.previous_server_ip)
				else:
					info.is_same_server = False
				
				message = {
						'XUID': info.xuid_list,
					}
				try:
					info.client.send(json.dumps(message).encode('utf-8'))
				except requests.exceptions.RequestException as e:
					print(f"Erreur lors de l'envoi du message: {e}")
				info.xuid_list.clear()
				info.previous_server_ip = info.server_ip

if not is_admin():
	info.interface_thread = threading.Thread(target=launch_interface, daemon=True)
	info.interface_thread.start()
	enable_proxy()
	info.receive_thread = threading.Thread(target=receive_messages, daemon=False)
	info.receive_thread.start()
	info.monitor_thread = threading.Thread(target=routine, daemon=True)
	info.monitor_thread.start()
