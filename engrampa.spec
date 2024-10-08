#
# Conditional build:
%bcond_without	caja	# Caja support
#
Summary:	Engrampa - an archive manager for MATE
Summary(pl.UTF-8):	Engrampa - zarządca archiwów dla środowiska MATE
Summary(pt_BR.UTF-8):	Engrampa - gerenciador de arquivos compactados para o MATE
Name:		engrampa
Version:	1.28.2
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://pub.mate-desktop.org/releases/1.28/%{name}-%{version}.tar.xz
# Source0-md5:	5a9e58842f019eddaa30d9fa85c7e957
URL:		https://wiki.mate-desktop.org/mate-desktop/applications/engrampa/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.9
%{?with_caja:BuildRequires:	caja-devel >= 1.17.1}
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.50.0
BuildRequires:	gtk+3-devel >= 3.22.0
BuildRequires:	json-glib-devel >= 0.14.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libxml2-progs
BuildRequires:	mate-common
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	scrollkeeper
BuildRequires:	tar >= 1:1.22
# libegg
BuildRequires:	xorg-lib-libICE-devel >= 1.0.0
BuildRequires:	xorg-lib-libSM-devel >= 1.0.0
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	glib2 >= 1:2.50.0
Requires:	gtk+3 >= 3.22.0
Requires:	json-glib >= 0.14.0
Suggests:	bzip2
Suggests:	cpio
Suggests:	gzip
Suggests:	p7zip
%ifarch %{ix86}
Suggests:	rar
%else
Suggests:	unrar
%endif
Suggests:	tar
Suggests:	zip
Obsoletes:	mate-file-archiver < 1.8.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Engrampa is an archive manager for the MATE environment. It's a fork
of File Roller from GNOME. With Engrampa you can: create and modify
archives; view the content of an archive; view and modify a file
contained in the archive; extract files from the archive.

%description -l pl.UTF-8
Engrampa to zarządca archiwów dla środowiska MATE. Jest to
odgałęzienie programu File Roller z GNOME. Przy jego pomocy można:
tworzyć i modyfikować archiwa, oglądać ich zawartość, oglądać i
modyfikować poszczególne pliki zawarte w archiwum oraz rozpakowywać
pliki z archiwów.

%description -l pt_BR.UTF-8
Engrampa é um gerenciador de pacotes de arquivos compactados para o
ambiente MATE. Com ele é possível criar arquivos, visualizar o
conteúdo de arquivos existentes, visualizar um arquivo contido em um
pacote e extrair os arquivos de um pacote.

%package -n caja-extension-engrampa
Summary:	Engrampa (archive manager) extension for Caja (MATE file manager)
Summary(pl.UTF-8):	Rozszerzenie Engrampa (zarządca archiwów) dla zarządcy plików Caja
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	caja >= 1.17.1
Obsoletes:	mate-file-manager-extension-engrampa < 1.8.0

%description -n caja-extension-engrampa
Engrampa (archive manager) extension for Caja (MATE file manager).

%description -n caja-extension-engrampa -l pl.UTF-8
Rozszerzenie Engrampa (zarządca archiwów) dla zarządcy plików Caja.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_caja:--disable-caja-actions} \
	--disable-silent-rules \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0/*.la

# outdated copies of es,ur
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{es_ES,ur_PK}
# not supported by glibc (2.34)
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{frp,ie,jv,ku_IQ,pms}

%find_lang engrampa --with-mate

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f engrampa.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/engrampa
%attr(755,root,root) %{_libexecdir}/engrampa-server
%dir %{_libexecdir}/engrampa
%attr(755,root,root) %{_libexecdir}/engrampa/isoinfo.sh
%{_datadir}/engrampa
%{_datadir}/metainfo/engrampa.appdata.xml
%{_datadir}/dbus-1/services/org.mate.Engrampa.service
%{_datadir}/glib-2.0/schemas/org.mate.engrampa.gschema.xml
%{_desktopdir}/engrampa.desktop
%{_iconsdir}/hicolor/*/actions/*-archive.png
%{_iconsdir}/hicolor/*/apps/engrampa.*
%{_mandir}/man1/engrampa.1*

%if %{with caja}
%files -n caja-extension-engrampa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/caja/extensions-2.0/libcaja-engrampa.so
%{_datadir}/caja/extensions/libcaja-engrampa.caja-extension
%endif
