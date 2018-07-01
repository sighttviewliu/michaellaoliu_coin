
Debian
====================
This directory contains files used to package michaellaoliud/michaellaoliu-qt
for Debian-based Linux systems. If you compile michaellaoliud/michaellaoliu-qt yourself, there are some useful files here.

## michaellaoliu: URI support ##


michaellaoliu-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install michaellaoliu-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your michaellaoliu-qt binary to `/usr/bin`
and the `../../share/pixmaps/michaellaoliu128.png` to `/usr/share/pixmaps`

michaellaoliu-qt.protocol (KDE)

