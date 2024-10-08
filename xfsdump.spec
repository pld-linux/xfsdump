Summary:	Tools for the XFS filesystem
Summary(pl.UTF-8):	Narzędzia do systemu plikowego XFS
Name:		xfsdump
Version:	3.2.0
Release:	1
License:	GPL v2
Group:		Applications/Archiving
Source0:	https://www.kernel.org/pub/linux/utils/fs/xfs/xfsdump/%{name}-%{version}.tar.xz
# Source0-md5:	12137c2f5c3c84c39e97f52ff6c24092
Patch0:		%{name}-miscfix.patch
Patch1:		%{name}-pl.po-update.patch
URL:		https://xfs.wiki.kernel.org/
BuildRequires:	attr-devel >= 2.4.15
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	libuuid-devel
BuildRequires:	ncurses-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xfsprogs-devel >= 2.6.9
BuildRequires:	xz
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

%{__rm} aclocal.m4

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__cp} include/install-sh .
CPPFLAGS="%{rpmcppflags} -I/usr/include/ncurses"
%configure \
	DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}" \
	OPTIMIZER="%{rpmcflags} %{rpmcppflags} -I/usr/include/ncurses"

%{__make} \
	V=1

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

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/xfsdump

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/{CHANGES,README.xfsdump}
%attr(755,root,root) %{_sbindir}/xfsdump
%attr(755,root,root) %{_sbindir}/xfsrestore
%attr(755,root,root) %{_sbindir}/xfsinvutil
%{_mandir}/man8/xfsdump.8*
%{_mandir}/man8/xfsinvutil.8*
%{_mandir}/man8/xfsrestore.8*
