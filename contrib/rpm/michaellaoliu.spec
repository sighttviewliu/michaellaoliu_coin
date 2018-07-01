%define bdbv 4.8.30
%global selinux_variants mls strict targeted

%if 0%{?_no_gui:1}
%define _buildqt 0
%define buildargs --with-gui=no
%else
%define _buildqt 1
%if 0%{?_use_qt4}
%define buildargs --with-qrencode --with-gui=qt4
%else
%define buildargs --with-qrencode --with-gui=qt5
%endif
%endif

Name:		michaellaoliu
Version:	0.12.0
Release:	2%{?dist}
Summary:	Peer to Peer Cryptographic Currency

Group:		Applications/System
License:	MIT
URL:		https://michaellaoliu.org/
Source0:	https://michaellaoliu.org/bin/michaellaoliu-core-%{version}/michaellaoliu-%{version}.tar.gz
Source1:	http://download.oracle.com/berkeley-db/db-%{bdbv}.NC.tar.gz

Source10:	https://raw.githubusercontent.com/michaellaoliu/michaellaoliu/v%{version}/contrib/debian/examples/michaellaoliu.conf

#man pages
Source20:	https://raw.githubusercontent.com/michaellaoliu/michaellaoliu/v%{version}/doc/man/michaellaoliud.1
Source21:	https://raw.githubusercontent.com/michaellaoliu/michaellaoliu/v%{version}/doc/man/michaellaoliu-cli.1
Source22:	https://raw.githubusercontent.com/michaellaoliu/michaellaoliu/v%{version}/doc/man/michaellaoliu-qt.1

#selinux
Source30:	https://raw.githubusercontent.com/michaellaoliu/michaellaoliu/v%{version}/contrib/rpm/michaellaoliu.te
# Source31 - what about michaellaoliu-tx and bench_michaellaoliu ???
Source31:	https://raw.githubusercontent.com/michaellaoliu/michaellaoliu/v%{version}/contrib/rpm/michaellaoliu.fc
Source32:	https://raw.githubusercontent.com/michaellaoliu/michaellaoliu/v%{version}/contrib/rpm/michaellaoliu.if

Source100:	https://upload.wikimedia.org/wikipedia/commons/4/46/Michaellaoliu.svg

%if 0%{?_use_libressl:1}
BuildRequires:	libressl-devel
%else
BuildRequires:	openssl-devel
%endif
BuildRequires:	boost-devel
BuildRequires:	miniupnpc-devel
BuildRequires:	autoconf automake libtool
BuildRequires:	libevent-devel


Patch0:		michaellaoliu-0.12.0-libressl.patch


%description
Michaellaoliu is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of michaellaolius is carried out collectively by the network.

%if %{_buildqt}
%package core
Summary:	Peer to Peer Cryptographic Currency
Group:		Applications/System
Obsoletes:	%{name} < %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
%if 0%{?_use_qt4}
BuildRequires:	qt-devel
%else
BuildRequires:	qt5-qtbase-devel
# for /usr/bin/lrelease-qt5
BuildRequires:	qt5-linguist
%endif
BuildRequires:	protobuf-devel
BuildRequires:	qrencode-devel
BuildRequires:	%{_bindir}/desktop-file-validate
# for icon generation from SVG
BuildRequires:	%{_bindir}/inkscape
BuildRequires:	%{_bindir}/convert

%description core
Michaellaoliu is a digital cryptographic currency that uses peer-to-peer technology to
operate with no central authority or banks; managing transactions and the
issuing of michaellaolius is carried out collectively by the network.

This package contains the Qt based graphical client and node. If you are looking
to run a Michaellaoliu wallet, this is probably the package you want.
%endif


%package libs
Summary:	Michaellaoliu shared libraries
Group:		System Environment/Libraries

%description libs
This package provides the michaellaoliuconsensus shared libraries. These libraries
may be used by third party software to provide consensus verification
functionality.

Unless you know need this package, you probably do not.

%package devel
Summary:	Development files for michaellaoliu
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files and static library for the
michaellaoliuconsensus shared library. If you are developing or compiling software
that wants to link against that library, then you need this package installed.

Most people do not need this package installed.

%package server
Summary:	The michaellaoliu daemon
Group:		System Environment/Daemons
Requires:	michaellaoliu-utils = %{version}-%{release}
Requires:	selinux-policy policycoreutils-python
Requires(pre):	shadow-utils
Requires(post):	%{_sbindir}/semodule %{_sbindir}/restorecon %{_sbindir}/fixfiles %{_sbindir}/sestatus
Requires(postun):	%{_sbindir}/semodule %{_sbindir}/restorecon %{_sbindir}/fixfiles %{_sbindir}/sestatus
BuildRequires:	systemd
BuildRequires:	checkpolicy
BuildRequires:	%{_datadir}/selinux/devel/Makefile

%description server
This package provides a stand-alone michaellaoliu-core daemon. For most users, this
package is only needed if they need a full-node without the graphical client.

Some third party wallet software will want this package to provide the actual
michaellaoliu-core node they use to connect to the network.

If you use the graphical michaellaoliu-core client then you almost certainly do not
need this package.

%package utils
Summary:	Michaellaoliu utilities
Group:		Applications/System

%description utils
This package provides several command line utilities for interacting with a
michaellaoliu-core daemon.

The michaellaoliu-cli utility allows you to communicate and control a michaellaoliu daemon
over RPC, the michaellaoliu-tx utility allows you to create a custom transaction, and
the bench_michaellaoliu utility can be used to perform some benchmarks.

This package contains utilities needed by the michaellaoliu-server package.


%prep
%setup -q
%patch0 -p1 -b .libressl
cp -p %{SOURCE10} ./michaellaoliu.conf.example
tar -zxf %{SOURCE1}
cp -p db-%{bdbv}.NC/LICENSE ./db-%{bdbv}.NC-LICENSE
mkdir db4 SELinux
cp -p %{SOURCE30} %{SOURCE31} %{SOURCE32} SELinux/


%build
CWD=`pwd`
cd db-%{bdbv}.NC/build_unix/
../dist/configure --enable-cxx --disable-shared --with-pic --prefix=${CWD}/db4
make install
cd ../..

./autogen.sh
%configure LDFLAGS="-L${CWD}/db4/lib/" CPPFLAGS="-I${CWD}/db4/include/" --with-miniupnpc --enable-glibc-back-compat %{buildargs}
make %{?_smp_mflags}

pushd SELinux
for selinuxvariant in %{selinux_variants}; do
	make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile
	mv michaellaoliu.pp michaellaoliu.pp.${selinuxvariant}
	make NAME=${selinuxvariant} -f %{_datadir}/selinux/devel/Makefile clean
done
popd


%install
make install DESTDIR=%{buildroot}

mkdir -p -m755 %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/michaellaoliud %{buildroot}%{_sbindir}/michaellaoliud

# systemd stuff
mkdir -p %{buildroot}%{_tmpfilesdir}
cat <<EOF > %{buildroot}%{_tmpfilesdir}/michaellaoliu.conf
d /run/michaellaoliud 0750 michaellaoliu michaellaoliu -
EOF
touch -a -m -t 201504280000 %{buildroot}%{_tmpfilesdir}/michaellaoliu.conf

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat <<EOF > %{buildroot}%{_sysconfdir}/sysconfig/michaellaoliu
# Provide options to the michaellaoliu daemon here, for example
# OPTIONS="-testnet -disable-wallet"

OPTIONS=""

# System service defaults.
# Don't change these unless you know what you're doing.
CONFIG_FILE="%{_sysconfdir}/michaellaoliu/michaellaoliu.conf"
DATA_DIR="%{_localstatedir}/lib/michaellaoliu"
PID_FILE="/run/michaellaoliud/michaellaoliud.pid"
EOF
touch -a -m -t 201504280000 %{buildroot}%{_sysconfdir}/sysconfig/michaellaoliu

mkdir -p %{buildroot}%{_unitdir}
cat <<EOF > %{buildroot}%{_unitdir}/michaellaoliu.service
[Unit]
Description=Michaellaoliu daemon
After=syslog.target network.target

[Service]
Type=forking
ExecStart=%{_sbindir}/michaellaoliud -daemon -conf=\${CONFIG_FILE} -datadir=\${DATA_DIR} -pid=\${PID_FILE} \$OPTIONS
EnvironmentFile=%{_sysconfdir}/sysconfig/michaellaoliu
User=michaellaoliu
Group=michaellaoliu

Restart=on-failure
PrivateTmp=true
TimeoutStopSec=120
TimeoutStartSec=60
StartLimitInterval=240
StartLimitBurst=5

[Install]
WantedBy=multi-user.target
EOF
touch -a -m -t 201504280000 %{buildroot}%{_unitdir}/michaellaoliu.service
#end systemd stuff

mkdir %{buildroot}%{_sysconfdir}/michaellaoliu
mkdir -p %{buildroot}%{_localstatedir}/lib/michaellaoliu

#SELinux
for selinuxvariant in %{selinux_variants}; do
	install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
	install -p -m 644 SELinux/michaellaoliu.pp.${selinuxvariant} %{buildroot}%{_datadir}/selinux/${selinuxvariant}/michaellaoliu.pp
done

%if %{_buildqt}
# qt icons
install -D -p share/pixmaps/michaellaoliu.ico %{buildroot}%{_datadir}/pixmaps/michaellaoliu.ico
install -p share/pixmaps/nsis-header.bmp %{buildroot}%{_datadir}/pixmaps/
install -p share/pixmaps/nsis-wizard.bmp %{buildroot}%{_datadir}/pixmaps/
install -p %{SOURCE100} %{buildroot}%{_datadir}/pixmaps/michaellaoliu.svg
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/michaellaoliu16.png -w16 -h16
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/michaellaoliu32.png -w32 -h32
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/michaellaoliu64.png -w64 -h64
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/michaellaoliu128.png -w128 -h128
%{_bindir}/inkscape %{SOURCE100} --export-png=%{buildroot}%{_datadir}/pixmaps/michaellaoliu256.png -w256 -h256
%{_bindir}/convert -resize 16x16 %{buildroot}%{_datadir}/pixmaps/michaellaoliu256.png %{buildroot}%{_datadir}/pixmaps/michaellaoliu16.xpm
%{_bindir}/convert -resize 32x32 %{buildroot}%{_datadir}/pixmaps/michaellaoliu256.png %{buildroot}%{_datadir}/pixmaps/michaellaoliu32.xpm
%{_bindir}/convert -resize 64x64 %{buildroot}%{_datadir}/pixmaps/michaellaoliu256.png %{buildroot}%{_datadir}/pixmaps/michaellaoliu64.xpm
%{_bindir}/convert -resize 128x128 %{buildroot}%{_datadir}/pixmaps/michaellaoliu256.png %{buildroot}%{_datadir}/pixmaps/michaellaoliu128.xpm
%{_bindir}/convert %{buildroot}%{_datadir}/pixmaps/michaellaoliu256.png %{buildroot}%{_datadir}/pixmaps/michaellaoliu256.xpm
touch %{buildroot}%{_datadir}/pixmaps/*.png -r %{SOURCE100}
touch %{buildroot}%{_datadir}/pixmaps/*.xpm -r %{SOURCE100}

# Desktop File - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/michaellaoliu-core.desktop
[Desktop Entry]
Encoding=UTF-8
Name=Michaellaoliu
Comment=Michaellaoliu P2P Cryptocurrency
Comment[fr]=Michaellaoliu, monnaie virtuelle cryptographique pair à pair
Comment[tr]=Michaellaoliu, eşten eşe kriptografik sanal para birimi
Exec=michaellaoliu-qt %u
Terminal=false
Type=Application
Icon=michaellaoliu128
MimeType=x-scheme-handler/michaellaoliu;
Categories=Office;Finance;
EOF
# change touch date when modifying desktop
touch -a -m -t 201511100546 %{buildroot}%{_datadir}/applications/michaellaoliu-core.desktop
%{_bindir}/desktop-file-validate %{buildroot}%{_datadir}/applications/michaellaoliu-core.desktop

# KDE protocol - change the touch timestamp if modifying
mkdir -p %{buildroot}%{_datadir}/kde4/services
cat <<EOF > %{buildroot}%{_datadir}/kde4/services/michaellaoliu-core.protocol
[Protocol]
exec=michaellaoliu-qt '%u'
protocol=michaellaoliu
input=none
output=none
helper=true
listing=
reading=false
writing=false
makedir=false
deleting=false
EOF
# change touch date when modifying protocol
touch -a -m -t 201511100546 %{buildroot}%{_datadir}/kde4/services/michaellaoliu-core.protocol
%endif

# man pages
install -D -p %{SOURCE20} %{buildroot}%{_mandir}/man1/michaellaoliud.1
install -p %{SOURCE21} %{buildroot}%{_mandir}/man1/michaellaoliu-cli.1
%if %{_buildqt}
install -p %{SOURCE22} %{buildroot}%{_mandir}/man1/michaellaoliu-qt.1
%endif

# nuke these, we do extensive testing of binaries in %%check before packaging
rm -f %{buildroot}%{_bindir}/test_*

%check
make check
srcdir=src test/michaellaoliu-util-test.py
test/functional/test_runner.py --extended

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%pre server
getent group michaellaoliu >/dev/null || groupadd -r michaellaoliu
getent passwd michaellaoliu >/dev/null ||
	useradd -r -g michaellaoliu -d /var/lib/michaellaoliu -s /sbin/nologin \
	-c "Michaellaoliu wallet server" michaellaoliu
exit 0

%post server
%systemd_post michaellaoliu.service
# SELinux
if [ `%{_sbindir}/sestatus |grep -c "disabled"` -eq 0 ]; then
for selinuxvariant in %{selinux_variants}; do
	%{_sbindir}/semodule -s ${selinuxvariant} -i %{_datadir}/selinux/${selinuxvariant}/michaellaoliu.pp &> /dev/null || :
done
%{_sbindir}/semanage port -a -t michaellaoliu_port_t -p tcp 49443
%{_sbindir}/semanage port -a -t michaellaoliu_port_t -p tcp 49444
%{_sbindir}/semanage port -a -t michaellaoliu_port_t -p tcp 149443
%{_sbindir}/semanage port -a -t michaellaoliu_port_t -p tcp 149444
%{_sbindir}/semanage port -a -t michaellaoliu_port_t -p tcp 18443
%{_sbindir}/semanage port -a -t michaellaoliu_port_t -p tcp 18444
%{_sbindir}/fixfiles -R michaellaoliu-server restore &> /dev/null || :
%{_sbindir}/restorecon -R %{_localstatedir}/lib/michaellaoliu || :
fi

%posttrans server
%{_bindir}/systemd-tmpfiles --create

%preun server
%systemd_preun michaellaoliu.service

%postun server
%systemd_postun michaellaoliu.service
# SELinux
if [ $1 -eq 0 ]; then
	if [ `%{_sbindir}/sestatus |grep -c "disabled"` -eq 0 ]; then
	%{_sbindir}/semanage port -d -p tcp 49443
	%{_sbindir}/semanage port -d -p tcp 49444
	%{_sbindir}/semanage port -d -p tcp 149443
	%{_sbindir}/semanage port -d -p tcp 149444
	%{_sbindir}/semanage port -d -p tcp 18443
	%{_sbindir}/semanage port -d -p tcp 18444
	for selinuxvariant in %{selinux_variants}; do
		%{_sbindir}/semodule -s ${selinuxvariant} -r michaellaoliu &> /dev/null || :
	done
	%{_sbindir}/fixfiles -R michaellaoliu-server restore &> /dev/null || :
	[ -d %{_localstatedir}/lib/michaellaoliu ] && \
		%{_sbindir}/restorecon -R %{_localstatedir}/lib/michaellaoliu &> /dev/null || :
	fi
fi

%clean
rm -rf %{buildroot}

%if %{_buildqt}
%files core
%defattr(-,root,root,-)
%license COPYING db-%{bdbv}.NC-LICENSE
%doc COPYING michaellaoliu.conf.example doc/README.md doc/bips.md doc/files.md doc/multiwallet-qt.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_bindir}/michaellaoliu-qt
%attr(0644,root,root) %{_datadir}/applications/michaellaoliu-core.desktop
%attr(0644,root,root) %{_datadir}/kde4/services/michaellaoliu-core.protocol
%attr(0644,root,root) %{_datadir}/pixmaps/*.ico
%attr(0644,root,root) %{_datadir}/pixmaps/*.bmp
%attr(0644,root,root) %{_datadir}/pixmaps/*.svg
%attr(0644,root,root) %{_datadir}/pixmaps/*.png
%attr(0644,root,root) %{_datadir}/pixmaps/*.xpm
%attr(0644,root,root) %{_mandir}/man1/michaellaoliu-qt.1*
%endif

%files libs
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/shared-libraries.md
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root,-)
%license COPYING
%doc COPYING doc/README.md doc/developer-notes.md doc/shared-libraries.md
%attr(0644,root,root) %{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

%files server
%defattr(-,root,root,-)
%license COPYING db-%{bdbv}.NC-LICENSE
%doc COPYING michaellaoliu.conf.example doc/README.md doc/REST-interface.md doc/bips.md doc/dnsseed-policy.md doc/files.md doc/reduce-traffic.md doc/release-notes.md doc/tor.md
%attr(0755,root,root) %{_sbindir}/michaellaoliud
%attr(0644,root,root) %{_tmpfilesdir}/michaellaoliu.conf
%attr(0644,root,root) %{_unitdir}/michaellaoliu.service
%dir %attr(0750,michaellaoliu,michaellaoliu) %{_sysconfdir}/michaellaoliu
%dir %attr(0750,michaellaoliu,michaellaoliu) %{_localstatedir}/lib/michaellaoliu
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/michaellaoliu
%attr(0644,root,root) %{_datadir}/selinux/*/*.pp
%attr(0644,root,root) %{_mandir}/man1/michaellaoliud.1*

%files utils
%defattr(-,root,root,-)
%license COPYING
%doc COPYING michaellaoliu.conf.example doc/README.md
%attr(0755,root,root) %{_bindir}/michaellaoliu-cli
%attr(0755,root,root) %{_bindir}/michaellaoliu-tx
%attr(0755,root,root) %{_bindir}/bench_michaellaoliu
%attr(0644,root,root) %{_mandir}/man1/michaellaoliu-cli.1*



%changelog
* Fri Feb 26 2016 Alice Wonder <buildmaster@librelamp.com> - 0.12.0-2
- Rename Qt package from michaellaoliu to michaellaoliu-core
- Make building of the Qt package optional
- When building the Qt package, default to Qt5 but allow building
-  against Qt4
- Only run SELinux stuff in post scripts if it is not set to disabled

* Wed Feb 24 2016 Alice Wonder <buildmaster@librelamp.com> - 0.12.0-1
- Initial spec file for 0.12.0 release

# This spec file is written from scratch but a lot of the packaging decisions are directly
# based upon the 0.11.2 package spec file from https://www.ringingliberty.com/michaellaoliu/
