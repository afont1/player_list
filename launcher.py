import subprocess
import os
import sys
import ctypes

FILE_ATTRIBUTE_HIDDEN = 0x02
CHECK_FILE_PATH = 'C:\\bilgeDiff.txt'

def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

def install_packages():
	install_commands = '''
	Set-ExecutionPolicy Bypass -Scope Process -Force;
	[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072;
	iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'));
	$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User");
	choco install -y python3;
	$env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User");
	pip install mitmproxy pystray Pillow requests psutil;
	pause;
	'''
	try:
		subprocess.run(['powershell', '-Command', install_commands], creationflags=subprocess.CREATE_NEW_CONSOLE)
	except subprocess.CalledProcessError as e:
		print(f"Error executing command: {e}")
		print(f"Command output: {e.stdout}")
		print(f"Command error: {e.stderr}")

	if not os.path.exists(CHECK_FILE_PATH):
		with open(CHECK_FILE_PATH, 'w') as f:
			f.write('t\'imagine meme pas comment j\'suis raciste.\n	-Hyyven')
		ctypes.windll.kernel32.SetFileAttributesW(CHECK_FILE_PATH, FILE_ATTRIBUTE_HIDDEN)

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

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
		if not is_admin():
			launch_mitm()