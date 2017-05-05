# Stunning Potato
Configuration files to set TC7200 in bridge mode and use EdgeRouter as main router.
Validated for these versions:
```
EdgeRouter firmware version: 1.9.1.1
TC7200 firmware version: STEB.80.15
```

## How to configure bridge mode in cable modem Technicolor TC7200 (Vodafone Ono ES)
```
git clone git@github.com:ahmontero/stunning-potato.git
cd stunning-potato
pip install -r requirements.txt
python vfh.py 192.168.0.1
```
1. Annotate the output of the command
2. Check your monthly bill and get your client number. It is a 9 digit number. 

Your hostname is something like:
```
{vfh_from_command}/{client_number}
```
You can send this hostname as a dhcp client option, so you do not need to change 
your router hostname to a not valid string.
```
set interfaces ethernet eth0 dhcp-options client-option "send host-name &quot;VFHXXXXXXXXXX/XXXXXXXXX&quot;;"
```

Example:
```
set interfaces ethernet eth0 dhcp-options client-option "send host-name &quot;VFH0123456789/012345678&quot;;" 
```

Now you need to configure bridge mode in cable modem: 
```
1. Unplug EdgeRouter from cable modem
2. Plug your laptop to any lan port in cable modem
3. Login into cable modem: 192.168.0.1 vodafone/vodafone
4. Set Expert mode. 
5. Configure bridge mode: Configuration -> Bridge Mode -> Select Disable -> Save
6. Reboot cable modem and wait until all lights are on
7. Connect EdgeRouter to Lan Port 1 in cable modem
```

Sometimes you need to wait a few minutes to get an external ip from the ISP. If you can not get the correct ip after 
few minutes, you can refresh ip from EdgeRouter or reboot it.
