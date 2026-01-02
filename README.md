#The project itself works on python and contains 2 files: (server.py & client.py). 

1. To use CMDgram You will need to install python to your computer
2.  If you want to text someone who is not on your same Wi-Fi network as you you will need to:

Option 1: (Port Forwarding)
This involves telling your home router that any traffic coming in on port 55555 should be sent directly to your computer.
1 Find your Local IP: Open CMD and type ipconfig. Look for "IPv4 Address" (usually starts with 192.168...).
2 Access Router Settings: Type your Gateway IP (also from ipconfig) into a web browser.
3 Port Forward: Look for "Port Forwarding" settings. Create a rule to forward port 55555 (TCP) to your Local IP.
4 Find your Public IP: Go to a site like "WhatIsMyIP.com". This is the IP you give your friend.
5 Update Client: Your friend must change SERVER_IP in client.py to your Public IP.

Option 2: (Ngrok) - **YOU NEED TO PAY FOR THIS**
If you don't want to mess with router settings, you can use a tool like Ngrok. It creates a "tunnel" from the internet to your local machine.
1 Download Ngrok: Get it from [ngrok.com](https://ngrok.com/) and set it up.
2 Start the Tunnel: In your terminal, run: ngrok tcp 55555
3 Get the Address: Ngrok will give you a forwarding address that looks like 0.tcp.ngrok.io:12345.
4 Update the Files:
5 Server: Keep the code as is (listening on 55555).
6 Client: Change SERVER_IP to "0.tcp.ngrok.io" and PORT to 12345 (or whatever numbers Ngrok gave you).

### **Before first use:**

**server.py** instructions:

Run It on your computer **if you are a host**
(You do not have to change anything here for it to work)

**client.py** instructions:

change  -----> _SERVER_IP_ **On line 6** to your host public IP adress (https://www.whatsmyip.org/)
change port **if needed**
