# Checklist for fresh Raspbian instalation:
#### Initial setup
* [x] set up wifi using `sudo raspi-config`
* [x] turn on SSH server using `sudo raspi-config`
#### Secure SSH
* [x] add public key to `/root/.ssh/authorized_keys` for remote access
* [x] remove password for `pi` account
* [x] update OS (`apt update && apt upgrade`)
#### Deploy Project
* [x] install `git`
* [x] clone project to `/opt/raspberry-iot` (`cd /opt && git clone git@github.com:pchecinski/raspberry-iot.git`)
* [x] change setting in `/opt/raspberry-iot/settings.py`
* [x] install `python3-pip`
* [x] install pip3 dependencies `pip3 install pyserial pymongo Adafruit_DHT`
* [x] setup project as service `cp /opt/rasberry-iot/rasbperry-iot.service /lib/systemd/system/raspberry-iot.service`
* [x] test and enable service (start, status, enable) `systemctl enable raspberry-iot`
### Setup OpenVPN access
* [x] install openvpn client `apt install openvpn`
* [x] get VPN config from server `scp -P33444 vps.checinski.dev:/root/raspberry.conf /etc/openvpn/raspberry.conf`
* [x] start VPN `systemctl start openvpn@raspberry`
* [x] check status `systemctl status openvpn@raspberry`
* [x] add VPN to system startup `systemctl enable openvpn@raspberry`
### Setup Zabbix Agent monitoring 
* [x] download zabbix 4.0 repository `wget https://repo.zabbix.com/zabbix/4.0/raspbian/pool/main/z/zabbix-release/zabbix-release_4.0-3+$(lsb_release -sc)_all.deb`
* [x] install it `dpkg -i zabbix-release_4.0-3+$(lsb_release -sc)_all.deb`
* [x] install zabbix-agent `apt update && apt -y install zabbix-agent`
* [x] change Server and ServerActive to 10.8.0.1, change Hostname to "Raspberry Pi" in `/etc/zabbix/zabbix_agentd.conf`
* [x] restart zabbix-agent `systemctl restart zabbix-agent`
