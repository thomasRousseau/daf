#DAF
##Disk Analysis Framework

*This is a Eurecom ongoing project which aims to provide a disk analysis framework for incident response missions. It is implemented in python under the GNU General Public Licence.*

###Installation:
```
apt-get install python-pip
pip install -r requirements.txt
```

###Objective:
DAF is a tool that aims to help investigator throught forensic disk analysis. It can not replace a fully qualified investigator but could help people to access easily information present in many places of the disk.

In the long term, DAF should also be able to make some correlation between different elements, in order to provide a better view of what happened in the disk.

##Usage:
DAF is a python2 tool working on Linux. It should work on disk using a Windows operating system, version 7 and later.

The tool presents some options:

```
> python daf.py -h

Options:
  -h, --help            show this help message and exit
  -i DISK_PATH, --input-disk=DISK_PATH
                        Set the base path of the mounted disk to analyze
  -n SESSION_NAME, --session-name=SESSION_NAME
                        Set the session name to SESSION_NAME
  -d DIRECTORY, --session-directory=DIRECTORY
                        Put the files created during session into DIRECTORY
  -p PLUGINS_DIRECTORY, --plugins-directory=PLUGINS_DIRECTORY
                        Specify the directory of the plugins
  -y SYSTEM_HIVE, --system-hive=SYSTEM_HIVE
                        Specify the absolute path to the system hive
  -o SOFTWARE_HIVE, --software-hive=SOFTWARE_HIVE
                        Specify the absolute path to the software hive
  -a SAM_HIVE, --sam-hive=SAM_HIVE
                        Specify the absolute path to the sam hive
  -u USERS_HIVES, --users-hives=USERS_HIVES
                        Specify a list of (username, user_hive) couples
  -c CONT, --continue=CONT
                        Specify a list of (username, user_hive) couples
```

The *-i* option is mandatory, as it is the path to the disk to analyze.

Then you can choose a session name, which by default will be *default-session* and a session directory which will by default be *sessions/default-session-<start_time>*. In this directory, files will be put while you are using the different plugins, so that if you ask for a command that you already used, you can choose to play it again or see the output from the last time you used it. It also permit to retrieve a previous session if you had to stop your analysis.

By default the tool will look for the registry hives at the usual locations on the disk, but if for any reason they are not at this location, you can specify the path to the different hives.

##Examples:

```
> python daf.py -i ../disk2 
------------------------------
   Disk Analysis Framework
------------------------------

 21:40:13> default_session: display_installed_browsers
List of installed browsers:

Name: Internet Explorer
Version: 11.0.9600.17420

Name: Google Chrome
Version: 48.0.2564.82
User: IEUser

 21:40:22> default_session: help
EOF
    Ctrl+D command quit the program.
----------------------------

display_config
    Display the configuration parameters of the disk to analyze.
----------------------------

display_installed_browsers
    Display the installed browsers. (Only support Chrome, Chromium, Firefox and IE for now)
----------------------------

exit
    Exit the program.
----------------------------

get_session_directory
    Return the session directory.
----------------------------

get_session_name
    Return the session name.
----------------------------

help
    Display this help.
----------------------------

quit
    Exit the program.
----------------------------

set_session_directory
    Argument: new folder name in relative name
        Change the session directory.
----------------------------

set_session_name
    Argument: new session name 
        Change the session name.
----------------------------
```

##For developpers:
###Structure of the framework:

The framework is based on four different levels:

Framework:

This level aims to handle the sessions created by the framework and the renderer. Indeed when launching the tool, a session will be created in order to permit the user to continue a previous analysis and, when executing a command that has already been executed, give the choice to the user to relaunch it or to directly display the previous result. This second functionality can be really interesting for plugins that take a long time to compute.

When creating a session, the framework store informations such as the session name and the UUID of the disk in a file registered in a session folder. Then, when a command is executed, the output of the command is stored on an other file in the same folder. The framework provide some options and commands to change the session name and the session folder.

Plugins:

This level is the one where the different commands the user can use are created. More details on how the plugins are made are given in the last part of this document.

Objects:

In this level, there are the different objects that represent elements of the filesystem. Basically the idea is to regroup information present in the filesystem and that is related to a specific interface. For example there is a USB object that look for information about a USB key that has been plugged in the system, and regroup them.

Filesystem:

This level is the lower level of the framework. His goal is to provide some API functions to get information present in the file system. For example it can be functions to parse a specific file format, access the registry key, ...


###How to create new plugins:

In order to create a new plugin, you need to create a new python file in the plugins directory. In this file, create a new class with a session object as a parameter of the \_\_init\_\_ function. 

Then, the different functions of this class will be the commands the users can use. These functions should take as input an argument parameter that represent a string containing what the user write as command parameters. If it is useful for the plugin, you can parse these parameters to make an interactive plugin.

The functions should also return a string which is what will be printed to the user as output of the command. 

The first multi-line comment, just after the function declaration, is what will be printed for the command when calling the help. 


###How to mount a vmdk disk on Linux

You are going to need the `affuse` tool as well as the `mmls` command :

```
apt-get update && apt-get install afflib-tools sleuthkit
```

Locate your vmdk file

```
mkdir raw mount
affuse -o allow_other disk.vmdk raw
mmls raw/disk.vmdk.raw
```

This should get you an output similar to this :

```
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

     Slot    Start        End          Length       Description
00:  Meta    0000000000   0000000000   0000000001   Primary Table (#0)
01:  -----   0000000000   0000002047   0000002048   Unallocated
02:  00:00   0000002048   0000206847   0000204800   NTFS (0x07)
03:  00:01   0000206848   0266332159   0266125312   NTFS (0x07)
04:  -----   0266332160   0266338303   0000006144   Unallocated
```

We can now figure the mount offset : 
**Offset = (Address of the begining of your disk partition) x (Unit size)**


Here : 
**Offset = 206848*512 = 105906176**

```
mount -o ro,loop,offset=105906176 raw/disk.vmdk.raw mount
```

Your disk is now mounted on the mount folder
