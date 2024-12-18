from my_struct import info
from my_struct import INTERNET_SETTINGS
from my_struct import winreg, threading, psutil, ctypes, subprocess

def on_quit():
	disable_proxy()
	info.stop_event_routine.set()
	info.stop_event_client.set()
	info.client.close()
	for proc in psutil.process_iter(['pid', 'name']):
		if proc.info['name'] == 'mitmdump.exe':
			proc.terminate()
			break
	if threading.current_thread() != info.monitor_thread:
		info.monitor_thread.join()
	if threading.current_thread() != info.receive_thread:
		info.receive_thread.join()
	quit()

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

def enable_proxy():
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