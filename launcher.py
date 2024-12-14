import subprocess
import os
import sys
import ctypes
import threading
import psutil
import winreg

FILE_ATTRIBUTE_HIDDEN = 0x02
CHECK_FILE_PATH = 'C:\\bilgeDiff.txt'
INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Internet Settings', 0, winreg.KEY_SET_VALUE | winreg.KEY_QUERY_VALUE)

def disable_proxy():
	try:
		_, reg_type = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyEnable')
	except FileNotFoundError:
		reg_type = winreg.REG_DWORD
	winreg.SetValueEx(INTERNET_SETTINGS, 'ProxyEnable', 0, reg_type, 0)

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False
	
def download_file():
	thread = threading.Thread(target=launch_mitm_dl)
	thread.start()

	import requests
	proxies = {
		'http': 'http://127.0.0.1:20000',
		'https': 'http://127.0.0.1:20000',
	}
	cert_url = 'http://mitm.it/cert/cer'
	cert_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), 'mitmproxy-ca-cert.cer')
	response = requests.get(cert_url, proxies=proxies)
	with open(cert_path, 'wb') as f:
		f.write(response.content)
	
	on_quit(thread)

def install_certificate():
	cert_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), 'mitmproxy-ca-cert.cer')
	print(f"Certificat path: {cert_path}")
	if not os.path.exists(cert_path):
		print(f"Le fichier {cert_path} n'existe pas.")
		return
	try:
		subprocess.run([
			'powershell.exe',
			f'Import-Certificate -FilePath "{cert_path}" -CertStoreLocation cert:\\LocalMachine\\Root'
		], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
		os.remove(cert_path)
	except subprocess.CalledProcessError as e:
		print(f"Erreur lors de l'installation du certificat: {e}")

def install_packages():
	install_commands = '''
	Set-ExecutionPolicy Bypass -Scope Process -Force;
	[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
	iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'));
	$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User");
	choco install -y python3;
	$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User");
	pip install mitmproxy pystray Pillow requests psutil;
	'''
	try:
		subprocess.run(['powershell', '-Command', install_commands], creationflags=subprocess.CREATE_NEW_CONSOLE)
	except subprocess.CalledProcessError as e:
		print(f"Error executing command: {e}")
		print(f"Command output: {e.stdout}")
		print(f"Command error: {e.stderr}")
	
	download_file()
	install_certificate()

	if not os.path.exists(CHECK_FILE_PATH):
		with open(CHECK_FILE_PATH, 'w') as f:
			f.write('t\'imagine meme pas comment j\'suis raciste.\n	-Hyyven')
		ctypes.windll.kernel32.SetFileAttributesW(CHECK_FILE_PATH, FILE_ATTRIBUTE_HIDDEN)
	
def on_quit(thread):
	disable_proxy()
	for proc in psutil.process_iter(['pid', 'name']):
		if proc.info['name'] == 'mitmdump.exe':
			proc.terminate()
			break
	if threading.current_thread() != thread:
		thread.join()

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def launch_mitm_dl():
	command = [
		'mitmdump',
		'--quiet',
		'-p', '20000',
	]
	try:
		subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
		# subprocess.run(command)
	except subprocess.CalledProcessError as e:
		print(f"Error executing command: {e}")
		print(f"Command output: {e.stdout}")
		print(f"Command error: {e.stderr}")
		

def launch_mitm():
	mitm_script = resource_path('mitm.py')
	allowed_hosts = 'playfabapi\\.com|privacy\\.xboxlive\\.com|sessiondirectory\\.xboxlive\\.com'
	command = [
		'mitmdump',
		'--quiet',
		'--allow-hosts', allowed_hosts,
		'-p', '20000',
		'-s', mitm_script,
	]
	try:
		subprocess.run(command, creationflags=subprocess.CREATE_NO_WINDOW)
		# subprocess.run(command)
	except subprocess.CalledProcessError as e:
		print(f"Error executing command: {e}")
		print(f"Command output: {e.stdout}")
		print(f"Command error: {e.stderr}")

if __name__ == "__main__":
	if not os.path.exists(CHECK_FILE_PATH) or is_admin():
		if not is_admin():
			ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
			sys.exit()
		install_packages()
	else:
		if os.path.exists(CHECK_FILE_PATH) and not is_admin():
			launch_mitm()