Summary:	Tools for the XFS filesystem
Summary(pl.UTF-8):	Narzędzia do systemu plikowego XFS
Name:		xfsdump
Version:	2.2.45
Release:	1
License:	GPL
Group:		Applications/Archiving
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}_%{version}-1.tar.gz
# Source0-md5:	9f4f6da94d14e638639a542b0fa8a722
Patch0:		%{name}-miscfix.patch
Patch1:		%{name}-libtool.patch
URL:		http://oss.sgi.com/projects/xfs/
BuildRequires:	attr-devel >= 2.4.15
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libuuid-devel
BuildRequires:	ncurses-devel
BuildRequires:	xfsprogs-devel >= 2.6.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		_bindir		/usr/sbin

%description
The xfsdump package contains xfsdump, xfsrestore and a number of other
utilities for administering XFS filesystems.

xfsdump examines files in a filesystem, determines which need to be
backed up, and copies those files to a specified disk, tape or other
storage medium. It uses XFS-specific directives for optimizing the
dump of an XFS filesystem, and also knows how to backup XFS extended
attributes. Backups created with xfsdump are "endian safe" and can
thus be transfered between Linux machines of different architectures
and also between IRIX machines.

xfsrestore performs the inverse function of xfsdump; it can restore a
full backup of a filesystem. Subsequent incremental backups can then
be layered on top of the full backup. Single files and directory
subtrees may be restored from full or partial backups.

%description -l pl.UTF-8
Pakiet zawiera programy xfsdump, xfsrestore i inne narzędzia do
administracji systemami plików XFS.

xfsdump kontroluje system plików oraz wykrywa, które części wymagają
wykonania kopii zapasowej, a następnie kopiuje te dane na podany dysk,
taśmę lub inne medium danych. Program używa specyficznych dla XFS
funkcji optymalizujących kopię zapasową (również znane jako
rozszerzone atrybuty kopii zapasowych XFS). Stworzone kopie zapasowe
są "endian safe" i przez to mogą być przenoszone pomiędzy maszynami
linuksowymi oraz IRIX pracującymi na różnych architekturach.

xfsrestore wykonuje operację przeciwną do xfsdump; może on odzyskać
system plików z kopii zapasowej. Przyrostowe kopie zapasowe mogą być
używane włącznie z pełną kopią.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

rm -f aclocal.m4

%build
%{__aclocal} -I m4
%{__autoconf}
CPPFLAGS="-I/usr/include/ncurses"
%configure \
	DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}" \
	OPTIMIZER="%{rpmcflags} -I/usr/include/ncurses"

%{__make} \
	LIBUUID="-luuid"

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV

%{__make} install \
	DIST_MANIFEST="$DIST_INSTALL"
%{__make} install-dev \
	DIST_MANIFEST="$DIST_INSTALL_DEV"

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/xfsrq.8*
echo ".so man8/xfsdq.8" > $RPM_BUILD_ROOT%{_mandir}/man8/xfsrq.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/{CHANGES,README.*}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
