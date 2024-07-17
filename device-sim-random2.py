#!/usr/bin/env python 
import sys
import os
import time
import random
import socket
import binascii
import random
import string

#=================================================================
# Variables to change behavior 
#=================================================================
#interface = "ens224" #interface to be used
interface = "eth1" #interface to be used
prob_bad = 0.4 #probability of client using bad urls
max_goodurls = 4 #number of good url to be used for every client
max_badurls = 2 #number of bad urls if client behaves bad -> defined by prob_bad
device_count = 33 #number of devices to be emulated
NAS_IP=bytearray(b'\x0a\xc8\x00\xfe') # depends on your FGT Config
#NAS_IP = "10.200.0.254"
FRAMED_IP=bytearray(b'\x0a\xc8\x00') #should correlate with host_subnet
#FRAMED_IP = "10.100.0."
host_subnet = ['10.200.0.']
UDP_IP = "10.200.0.254" #IP of FGT listening to RSSO
UDP_PORT = 1813
server_ip = 'www.google.com' #IP for ping
debug = 0 #set to anything >0 to enable debug output to console

#Precrafted Radius Packet
RADIUS_Header=bytearray(b'\x04\x02')
RADIUS_Header2=bytearray(b'\x29\xb4\x94\x23\xa0\x8e\x1c\xda\x78\x18\x91\x8a\xa1\x97\xcc\x7f\x28\x06\x00\x00\x00\x03\x2c\x13\x35\x38\x45\x32\x34\x32\x43\x34\x2d\x30\x30\x30\x30\x30\x30\x30\x46\x2d\x06\x00\x00\x00\x01')
RADIUS_Footer=bytearray(b'\x05\x06\x00\x00\x18\x01\x3d\x06\x00\x00\x00\x13\x20\x13\x30\x30\x3a\x31\x30\x3a\x66\x33\x3a\x34\x61\x3a\x66\x35\x3a\x31\x30\x1e\x20\x30\x30\x3a\x31\x30\x3a\x66\x33\x3a\x34\x61\x3a\x66\x35\x3a\x31\x30\x3a\x49\x6e\x66\x4c\x61\x62\x5f\x38\x30\x32\x31\x78\x1f\x13\x66\x63\x3a\x36\x34\x3a\x62\x61\x3a\x39\x30\x3a\x32\x38\x3a\x35\x64\x4d\x11\x43\x4f\x4e\x4e\x45\x43\x54\x20\x38\x30\x32\x2e\x31\x31\x61\x19\x07\x73\x74\x61\x66\x66\x29\x06\x00\x00\x00\x00\x2f\x06\x00\x00\x00\x00\x30\x06\x00\x00\x00\x00\x2a\x06\x00\x00\x00\x00\x2b\x06\x00\x00\x00\x00\x1a\x0c\x00\x00\x3e\x6f\x01\x06\x00\x00\x00\x07\x1a\x0c\x00\x00\x3e\x6f\x02\x06\x41\x50\x2d\x37\x21\x16\xfe\x80\x00\x00\x00\x00\x00\x00\x01\xd9\x93\x8b\x56\x1a\x4f\x4d\x00\x00\x00\x32')
#Constants for RADIUS Packet
PACKETSIZE=247 #size of precrafted packet without username
name_index = 0
host_index = 0
username_list = [
"Toccara Bieniek",
"Kandis Schwein",
"Joie Pounders",
"Geralyn Arjona",
"Marla Kull",
"Joseph Farren",
"Dinorah Verdi",
"Valene Afanador",
"Caroline Boggs",
"Kareen Darling",
"Randee Walford",
"Dominica Southworth",
"Dayle Bellantoni",
"Julius Catalano",
"Julieann Aquilar",
"Kristi Vuong",
"Dewayne Sproul",
"Scottie Hyer",
"Haywood Schmit",
"Lizzette Czech",
"Lorinda Mill",
"Kaylee Boudreaux",
"Tommye Strickland",
"Sharolyn Zelaya",
"Wendy Marshell",
"Jonell Parikh",
"Shalon Headley",
"Rosana Hobson",
"Nicol Bergeron",
"Lidia Hackbarth",
"Kiana Orlowski",
"Jinny Komar",
"Alma Regner",
"Tobias Skowronski",
"Cleopatra Thomson",
"Josephine Stelle",
"Jessia Shaver",
"Efren Dunbar",
"Darius Saxon",
"Cindie Marksberry",
"Paulette Kindrick",
"Josefina Clifford",
"Michaela Shewmaker",
"Lovetta Backman",
"Mireille Schurman",
"Garfield Stayton",
"Hosea Seelye",
"Manuel Kenny",
"Charlene Aiello",
"Elwood Freeberg",
]  



device_type_list = [
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; BOIE9;ENUS)", #win7
  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1.", #win7 64 bits
  "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1", #Linux ubuntu
  "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070719 CentOS/1.5.0.12-3.el5.centos Firefox/1.5.0.12", #Linux CentOS
  "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8", # MAC OS X
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.35.1 (KHTML, like Gecko) Version/6.1 Safari/537.35.1", #MAC OS X 10.9
  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; Xbox)XBMC/3.3-DEV-r31572 (Xbox; http://www.xbmc.org)", #Xbox
  "Opera/9.30 (Nintendo Wii; U; ; 2071; Wii Shop Channel/1.0; en)", #Wii
  "Mozilla/5.0 (Linux; U; Android 2.3.4; en-us; Kindle Fire Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1", #kindle fire
  "Mozilla/5.0 (BlackBerry; U; BlackBerry 9860; en-GB) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.0.0.296 Mobile Safari/534.11+", #blackBerry
  "Mozilla/5.0 (Linux; Android 4.1.2; Nexus 7 Build/JZO54K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19", #Nexus
  "Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko", #surface 2
  "Mozilla/5.0 (iPad; CPU iPhone OS 501 like Mac OS X) AppleWebKit/534.46 (KHTML like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3", #iPAD
  "Mozilla/5.0 (iphone; U; CPU iPhone OS 4_3_5 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5", #iPhone
  "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4", #iPhone 6 Plus
  "Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53" #ipad
]

mac_prefix = hex(random.randrange(256))[2:]
mac_prefix2 = hex(random.randrange(256))[2:]

def striplist(l):
    return([x.strip() for x in l])

def send_accounting( name, host):
	USERNAME=username_list[ name ]
	
	MESSAGE = bytearray()
	MESSAGE += RADIUS_Header 
	#print "len after Header", len(MESSAGE)
	MESSAGE += binascii.unhexlify(b'{:04x}'.format(len(USERNAME)+PACKETSIZE))
	#print "len after size", len(MESSAGE)
	MESSAGE += RADIUS_Header2
	#print "len after Header2", len(MESSAGE)
	#Adding Username
	MESSAGE += b'\x01' + binascii.unhexlify(b'{:02x}'.format(len(USERNAME)+2)) + USERNAME
	#print "len after user", len(MESSAGE)
	#Adding NAS-IP
	MESSAGE += b'\x04\x06' + NAS_IP
	#print "len after NAS", len(MESSAGE)
	#Adding Framed-IP
	MESSAGE += b'\x08\x06' + FRAMED_IP + binascii.unhexlify(b'{:02x}'.format(host))
	#print "len after Framed", len(MESSAGE)
	
	MESSAGE += RADIUS_Footer
	#print "len after Header", len(MESSAGE)
	
	print "[info] Sending Radius Message:", USERNAME, host, len(MESSAGE), "to", UDP_IP, ":", UDP_PORT 
	
	sock = socket.socket(socket.AF_INET, # Internet
		socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	sock.close
	del MESSAGE
	#print "len after del", len(MESSAGE)
	
	
def run_iteration():
	for index in range(0, int(device_count)):
		subnet_index = int(index/250)
		host_index = index%250 + 2
		name_index = index % len(username_list)
		default_gw = host_subnet[subnet_index] + '254'
		host_ip = host_subnet[subnet_index] + str(host_index)
		print("[info] ==================" + str(index) + "=================== ")  
		print "changing interface " + interface
		cmd = 'ifconfig ' + interface + ' down'
		if debug:
			print(cmd)
		os.system(cmd)
		mac_address = '00:0c:'+ mac_prefix +':'+ mac_prefix2 +':' + hex(subnet_index)[2:]+ ":" + hex(host_index)[2:]
		cmd = 'ifconfig ' + interface + ' hw ether ' + mac_address
		if debug:
			print(cmd)
		os.system(cmd)
		cmd = 'ifconfig ' + interface + ' ' + host_ip + ' netmask 255.255.255.0'
		if debug:
			print(cmd)
		os.system(cmd)
		cmd = 'route del default'
		if debug:
			print(cmd)
		os.system(cmd)
		cmd = 'route add default gw ' + default_gw + ' ' + interface
		if debug:
			print(cmd)
		os.system(cmd)

		cmd = 'ifconfig ' + interface + ' up'
		if debug:
			print(cmd)
		os.system(cmd)


		time.sleep(2)

		print "[info]-sending RADACCT MSG User:" + username_list[name_index] + " IP:" + host_ip
		send_accounting( name_index, host_index)

		print("[info]- retrieving " + str(max_goodurls) + " good urls")
		for rungood in range (1, max_goodurls):
			cmd_curl = 'wget --quiet -T 2 -t 1 -i ' + goodurls[random.randint(0, nogoodurls-1)] + ' --no-check-certificate --delete-after --user-agent=\"' + device_type_list[ host_index % len(device_type_list)] + '\"'

		if (random.random()<=prob_bad):
			print("[info]- retrieving " + str(max_badurls) + " bad urls")
			for runbad in range (1, max_badurls):
				cmd_curl = 'wget --quiet -T 2 -t 1 -i ' + badurls[random.randint(0, nobadurls-1)] + ' --no-check-certificate --delete-after --user-agent=\"' + device_type_list[ host_index % len(device_type_list)] + '\"'
		
		#cmd_curl = 'curl -silent -A \"' + device_type_list[ host_index % len(device_type_list)] + '\" -output-document=/dev/null http://'+ server_ip
		#cmd_curl = 'wget --quiet -T 2 -t 1 https://www.theuselesswebindex.com/website --no-check-certificate --delete-after --user-agent=\"' + device_type_list[ host_index % len(device_type_list)] + '\"'
		#cmd_curl = 'wget --quiet -T 2 -t 1 https://www.discuvver.com/jump2.php --no-check-certificate --delete-after --user-agent=\"' + device_type_list[ host_index % len(device_type_list)] + '\"'
		cmd_ping = 'ping -q -c 2 '+ server_ip
		if debug:
			print(cmd_curl)
		os.system(cmd_curl)
		if debug:
			print(cmd_ping)
		os.system(cmd_ping)
		print("[info] ================== End =================== \n")
    

#while True:


if not os.path.isfile('/fortipoc/goodurls.txt'):
    print("can't find goodurls.txt")
    exit()
if not os.path.isfile('/fortipoc/badurls.txt'):
    print("can't find badurls.txt")
    exit()
f = open('/fortipoc/goodurls.txt', 'r+')
goodurls = striplist([line for line in f.readlines()]) #striplist removes whitespaces from entries (esp. CR/LF) see define at top
f.close()
f = open('/fortipoc/badurls.txt', 'r+')
badurls = striplist([line for line in f.readlines()])  #striplist removes whitespaces from entries (esp. CR/LF) see define at top
f.close()

nogoodurls = len (goodurls)
nobadurls = len (badurls)

print "Loaded " + str(nogoodurls) + " good urls and " + str(nobadurls) + " bad urls"

run_iteration()
  
cmd = 'ifconfig ' + interface + ' down'
if debug:
	print(cmd)
os.system(cmd)   
mac_address = '00:0c:29:7f:2d:64'
cmd = 'ifconfig ' + interface + ' hw ether ' + mac_address
if debug:
	print(cmd)
os.system(cmd)
host_ip = '10.200.0.1'
cmd = 'ifconfig ' + interface + ' ' + host_ip + ' netmask 255.255.255.0'
if debug:
	print(cmd)
os.system(cmd)
cmd = 'route del default'
if debug:
	print(cmd)
os.system(cmd)
cmd = 'route add default gw 10.200.0.254 ' + interface
if debug:
	print(cmd)
os.system(cmd)
cmd = 'ifconfig ' + interface + ' up'
if debug:
	print(cmd)
os.system(cmd)
time.sleep(2)

while True:
  run_iteration()
