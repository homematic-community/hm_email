# hm_email
A HomeMatic/CCU Addon to send emails from a CCU system either by directly calling a script from the CCU WebUI programming interface or via CUxD devices being used within the CCU system.

# Supported CCU devices

* HomeMatic CCU1
* HomeMatic CCU2 (http://www.eq-3.de/produkt-detail-zentralen-und-gateways/items/homematic-zentrale-ccu-2.html)
* RaspberryMatic (http://homematic-forum.de/forum/viewtopic.php?f=56&t=26917)

# Installation
1. Download installation archive (```email-X.X.X.tar.gz```) from 'releases' sub directory (https://github.com/jens-maus/hm_email/releases)
2. Log into your WebUI interface
3. Upload installation archive (don't unarchive tar.gz) to the WebUI
4. Start installation

# Configuration
After installation use the following URL to display the configuration dialog of the email addon on your CCU:

http://CCU/addons/email

where you have to replace 'CCU' with the ip address or hostname of your ccu device.

# Authors
Copyright (c) 2015 Harima-kun, Mathias, HMside, Jens Maus <mail@jens-maus.de>
