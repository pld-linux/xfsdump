Summary:	Tools for the XFS filesystem
Summary(pl):	Narzêdzia do systemu plikowego XFS
Name:		xfsdump
Version:	2.0.1
Release:	1
License:	GPL
Group:		Applications/Archiving
URL:		http://oss.sgi.com/projects/xfs/
Source0:	ftp://oss.sgi.com/projects/xfs/download/cmd_tars/%{name}-%{version}.src.tar.gz
Patch0:		%{name}-miscfix.patch
BuildRequires:	autoconf
BuildRequires:	e2fsprogs-devel
BuildRequires:	xfsprogs-devel >= 1.2.7
BuildRequires:	attr-devel
BuildRequires:	dmapi-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%patch0 -p1

%build
DEBUG="%{?debug:-DDEBUG}%{!?debug:-DNDEBUG}"; export DEBUG
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV
%{__make} install DIST_MANIFEST="$DIST_INSTALL"
%{__make} install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/xfsrq.8
echo ".so man8/xfsdq.8" > $RPM_BUILD_ROOT%{_mandir}/man8/xfsrq.8

gzip -9nf doc/{CHANGES,README.*}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.gz
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) /sbin/*
%{_mandir}/man8/*
