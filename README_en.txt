# Installation and Usage Instructions

## Installation

1. Before launching the launcher for the first time, double-click on `mitmproxy-ca-cert.p12`.
   - Make sure to select "Local Computer" and not "Current User", then click "Next" until the end.

2. Authorize the `.exe` file in Windows Defender, otherwise it will be deleted.

3. When you launch in administrator mode, it installs the necessary dependencies for the program to function properly.
   - If you launch without administrator mode, it simply launches the player list.
   - If there is a problem, try launching in administrator mode, it might solve the issue.

## Usage

- To close the program, right-click on the hidden icons in Windows.
- If you close it through the task manager, you will lose internet connection.
  - Restarting the PC will not change anything.
  - If this happens, open PowerShell and run the following command:
    ```
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" -Name ProxyEnable -Value 0
    ```

## Known Bugs

- The server IP address or server name is incorrect when you change seas.
- There may be small ping spikes (to be verified).
