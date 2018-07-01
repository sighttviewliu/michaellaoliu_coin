Sample init scripts and service configuration for michaellaoliud
==========================================================

Sample scripts and configuration files for systemd, Upstart and OpenRC
can be found in the contrib/init folder.

    contrib/init/michaellaoliud.service:    systemd service unit configuration
    contrib/init/michaellaoliud.openrc:     OpenRC compatible SysV style init script
    contrib/init/michaellaoliud.openrcconf: OpenRC conf.d file
    contrib/init/michaellaoliud.conf:       Upstart service configuration file
    contrib/init/michaellaoliud.init:       CentOS compatible SysV style init script

Service User
---------------------------------

All three Linux startup configurations assume the existence of a "michaellaoliu" user
and group.  They must be created before attempting to use these scripts.
The OS X configuration assumes michaellaoliud will be set up for the current user.

Configuration
---------------------------------

At a bare minimum, michaellaoliud requires that the rpcpassword setting be set
when running as a daemon.  If the configuration file does not exist or this
setting is not set, michaellaoliud will shutdown promptly after startup.

This password does not have to be remembered or typed as it is mostly used
as a fixed token that michaellaoliud and client programs read from the configuration
file, however it is recommended that a strong and secure password be used
as this password is security critical to securing the wallet should the
wallet be enabled.

If michaellaoliud is run with the "-server" flag (set by default), and no rpcpassword is set,
it will use a special cookie file for authentication. The cookie is generated with random
content when the daemon starts, and deleted when it exits. Read access to this file
controls who can access it through RPC.

By default the cookie is stored in the data directory, but it's location can be overridden
with the option '-rpccookiefile'.

This allows for running michaellaoliud without having to do any manual configuration.

`conf`, `pid`, and `wallet` accept relative paths which are interpreted as
relative to the data directory. `wallet` *only* supports relative paths.

For an example configuration file that describes the configuration settings,
see `contrib/debian/examples/michaellaoliu.conf`.

Paths
---------------------------------

### Linux

All three configurations assume several paths that might need to be adjusted.

Binary:              `/usr/bin/michaellaoliud`  
Configuration file:  `/etc/michaellaoliu/michaellaoliu.conf`  
Data directory:      `/var/lib/michaellaoliud`  
PID file:            `/var/run/michaellaoliud/michaellaoliud.pid` (OpenRC and Upstart) or `/var/lib/michaellaoliud/michaellaoliud.pid` (systemd)  
Lock file:           `/var/lock/subsys/michaellaoliud` (CentOS)  

The configuration file, PID directory (if applicable) and data directory
should all be owned by the michaellaoliu user and group.  It is advised for security
reasons to make the configuration file and data directory only readable by the
michaellaoliu user and group.  Access to michaellaoliu-cli and other michaellaoliud rpc clients
can then be controlled by group membership.

### Mac OS X

Binary:              `/usr/local/bin/michaellaoliud`  
Configuration file:  `~/Library/Application Support/Michaellaoliu/michaellaoliu.conf`  
Data directory:      `~/Library/Application Support/Michaellaoliu`  
Lock file:           `~/Library/Application Support/Michaellaoliu/.lock`  

Installing Service Configuration
-----------------------------------

### systemd

Installing this .service file consists of just copying it to
/usr/lib/systemd/system directory, followed by the command
`systemctl daemon-reload` in order to update running systemd configuration.

To test, run `systemctl start michaellaoliud` and to enable for system startup run
`systemctl enable michaellaoliud`

### OpenRC

Rename michaellaoliud.openrc to michaellaoliud and drop it in /etc/init.d.  Double
check ownership and permissions and make it executable.  Test it with
`/etc/init.d/michaellaoliud start` and configure it to run on startup with
`rc-update add michaellaoliud`

### Upstart (for Debian/Ubuntu based distributions)

Drop michaellaoliud.conf in /etc/init.  Test by running `service michaellaoliud start`
it will automatically start on reboot.

NOTE: This script is incompatible with CentOS 5 and Amazon Linux 2014 as they
use old versions of Upstart and do not supply the start-stop-daemon utility.

### CentOS

Copy michaellaoliud.init to /etc/init.d/michaellaoliud. Test by running `service michaellaoliud start`.

Using this script, you can adjust the path and flags to the michaellaoliud program by
setting the MICHAELLAOLIUD and FLAGS environment variables in the file
/etc/sysconfig/michaellaoliud. You can also use the DAEMONOPTS environment variable here.

### Mac OS X

Copy org.michaellaoliu.michaellaoliud.plist into ~/Library/LaunchAgents. Load the launch agent by
running `launchctl load ~/Library/LaunchAgents/org.michaellaoliu.michaellaoliud.plist`.

This Launch Agent will cause michaellaoliud to start whenever the user logs in.

NOTE: This approach is intended for those wanting to run michaellaoliud as the current user.
You will need to modify org.michaellaoliu.michaellaoliud.plist if you intend to use it as a
Launch Daemon with a dedicated michaellaoliu user.

Auto-respawn
-----------------------------------

Auto respawning is currently only configured for Upstart and systemd.
Reasonable defaults have been chosen but YMMV.
