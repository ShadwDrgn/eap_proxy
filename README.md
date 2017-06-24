Run with:
python eap_proxy.py <ONT_INTERFACE_NAME> <MODEM_INTERFACE_NAME>

Example: python eap_proxy.py eth0 eth1

This should run on an EdgerouterLite and many other devices without issue. You may need to restart dhcp for your ethernet device on your WAN to get this working(After it's proxied all the EAP packets the first time). You may need to create a vlan 0 on your ONT device to be your WAN, and you almost certainly have to clone the mac of your modem on the ONT device interface. I'm terrible at documentation, so good luck.
