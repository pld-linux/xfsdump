Summary:	Tools for the XFS filesystem
Summary(pl):	Narzêdzia do systemu plikowego XFS
Name:		xfsdump
Version:	2.2.6
Release:	1
License:	GPL
Group:		Applications/Archiving
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
# Source0-md5:	e6282e66993c692d444cc21b5f8bb3eb
BuildRequires:	autoconf
BuildRequires:	e2fsprogs-devel
BuildRequires:	xfsprogs-devel >= 2.1.2-2
BuildRequires:	attr-devel
BuildRequires:	dmapi-devel >= 2.0.5-1
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

%description -l pl
Pakiet zawiera programy xfsdump, xfsrestore i inne narzêdzia do
administracji systemami plików XFS.

xfsdump kontroluje system plików oraz wykrywa, które czê¶ci wymagaj±
wykonania kopii zapasowej, a nastêpnie kopiuje te dane na podany dysk,
ta¶mê lub inne medium danych. Program u¿ywa specyficznych dla XFS
funkcji optymalizuj±cych kopiê zapasow± (równie¿ znane jako
rozszerzone atrybuty kopii zapasowych XFS). Stworzone kopie zapasowe
s± "endian safe" i przez to mog± byæ przenoszone pomiêdzy maszynami
Linuksowymi oraz IRIX pracuj±cymi na ró¿nych architekturach.

xfsrestore wykonuje operacjê przeciwn± do xfsdump; mo¿e on odzyskaæ
system plików z kopii zapasowej. Inkrementalne kopie zapasowe mog± byæ
u¿ywane w³±cznie z pe³n± kopi±.

%prep
%setup  -q

%build
DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}"; export DEBUG
%{__autoconf}
CPPFLAGS="-I/usr/include/ncurses"
%configure

%{__make} \
	LIBUUID="-luuid" \
	OPTIMIZER="%{rpmcflags} -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV
%{__make} install DIST_MANIFEST="$DIST_INSTALL"
%{__make} install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"

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
