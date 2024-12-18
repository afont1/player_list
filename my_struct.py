import threading
import socket
import threading
import winreg
import psutil
import ctypes
import subprocess
import json
import requests
import time
from mitmproxy import http

INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE)
# HOST = '213.199.55.22'
HOST = '127.0.0.1'
PORT = 5000

class PL_info:
	def __init__(self):
		self.server_response = None
		self.stop_event_client = threading.Event()
		self.stop_event_routine = threading.Event()
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.previous_server_ip = None
		self.monitor_thread = None
		self.server_ip = "unknown"
		self.server_name = "unknown"
		self.stamp_id = "unknown"
		self.is_same_server = False
		self.xuid_list = []
		self.xuid_list_lock = threading.Lock()
		self.gamertags_list = []
		self.interface_thread = None

info = PL_info()

