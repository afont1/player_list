import subprocess
import json
import requests
import threading	
import time
import pystray 
import winreg
import psutil
import base64
from io import BytesIO
from PIL import Image
from mitmproxy import http

ENCODED_ICON = "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"
INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE)

previous_server_ip = None
icon = None
server_ip = "unknown"
server_name = "unknown"
stamp_id = "unknown"
is_same_server = False
xuid_list = []
xuid_list_lock = threading.Lock()
stop_event = threading.Event()
webhook_url = '####'

def enable_proxy(proxy):
	try:
		_, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyServer')
	except FileNotFoundError:
		reg_type = winreg.REG_SZ
	winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyServer', 0, reg_type, '127.0.0.1:20000')
	try:
		_, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyEnable')
	except FileNotFoundError:
		reg_type = winreg.REG_DWORD
	winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, reg_type, 1)

def disable_proxy():
	try:
		_, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyEnable')
	except FileNotFoundError:
		reg_type = winreg.REG_DWORD
	winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, reg_type, 0)

def get_machine_id():
	try:
		result = subprocess.check_output(['wmic', 'csproduct', 'get', 'uuid'])
		result = result.decode().split('\n')[1].strip()
		return (result)
	except Exception as e:
		return (None)
	
def get_image_from_base64(encoded_string):
    image_data = base64.b64decode(encoded_string)
    return Image.open(BytesIO(image_data))

def request(flow: http.HTTPFlow) -> None:
	url = flow.request.url
	if "/permission/validate" in url:
		try:
			data = json.loads(flow.request.content)
			if "Users" in data:
				for _users in data["Users"]:
					xuid = _users["Xuid"]
					if xuid.isnumeric():
						with xuid_list_lock:
							xuid_list.append(xuid)
		except Exception as e:
			print(f"Unexpected error request: {e}")
			pass

def response(flow: http.HTTPFlow) -> None:
	global server_name, stamp_id, server_ip, is_same_server
	url = flow.request.url
	if "/sessionTemplates/" in url:
		try:
			data = json.loads(flow.response.content)
			properties = data["properties"]
			server_name = properties["system"]["matchmaking"]["serverConnectionString"]
			stamp_id = properties["custom"]["StampId"]
			server_ip = properties["custom"]["GameServerAddress"]
			print(f"Server Name: {server_name}, Stamp ID: {stamp_id}, Server IP: {server_ip}")
		except Exception as e:
			print(f"Unexpected error response: {e}")
			pass

def routine():
	global previous_server_ip
	is_same_server = False
	while not stop_event.is_set():
		time.sleep(1)
		with xuid_list_lock:
			if len(xuid_list) >= 1:
				if previous_server_ip is not None:
					is_same_server = (server_ip == previous_server_ip)
				else:
					is_same_server = False
				message = {
					'content': f'XUID: {xuid_list}\nSERVER_NAME: {server_name}\nSTAMP_ID: {stamp_id}\nSERVER_IP: {server_ip}\nIS_SAME_SERVER: {is_same_server}\nUID: {get_machine_id()}'
				}
				try:
					requests.post(webhook_url, json=message, timeout=10, verify=False)
				except requests.exceptions.RequestException as e:
					print(f"Erreur lors de l'envoi du message: {e}")
				xuid_list.clear()
				previous_server_ip = previous_server_ip

def on_quit(icon):
	disable_proxy()
	stop_event.set()
	for proc in psutil.process_iter(['pid', 'name']):
		if proc.info['name'] == 'mitmdump.exe':
			proc.terminate()
			break
	icon.stop()
	if threading.current_thread() != monitor_thread:
		monitor_thread.join()
	if threading.current_thread() != icon_thread:
		icon_thread.join()
	quit()

def run_icon():
	icon = pystray.Icon("Bilge Diff", title="Bilge Diff")
	try:
		icon.icon = get_image_from_base64(ENCODED_ICON)
	except Exception:
		icon.icon = Image.new("RGB", (64, 64), (255, 255, 255))
	icon.menu = pystray.Menu(pystray.MenuItem("Quit", on_quit))
	icon.run()

enable_proxy(f'127.0.0.1:20000')
monitor_thread = threading.Thread(target=routine, daemon=True)
monitor_thread.start()
icon_thread = threading.Thread(target=run_icon, daemon=True)
icon_thread.start()