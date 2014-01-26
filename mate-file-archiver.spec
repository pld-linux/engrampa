#
# Conditional build:
%bcond_without	caja	# Caja (mate-file-manager) support
%bcond_with	gtk3	# use GTK+ 3.x instead of 2.x
#
Summary:	Engrampa - an archive manager for MATE
Summary(pl.UTF-8):	Engrampa - zarządca archiwów dla środowiska MATE
Summary(pt_BR.UTF-8):	Engrampa - gerenciador de arquivos compactados para o MATE
Name:		mate-file-archiver
Version:	1.6.0
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	8a23b4504605473f790ed9b3f58bfe6e
URL:		http://mate-desktop.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.26.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.22.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libxml2-progs
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils
%{?with_caja:BuildRequires:	mate-file-manager-devel >= 1.1.0}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.36
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
BuildRequires:	tar >= 1:1.22
# libegg
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	glib2 >= 1:2.26.0
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.22.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Suggests:	bzip2
Suggests:	gzip
Suggests:	p7zip
%ifarch %{ix86}
Suggests:	rar
%else
Suggests:	unrar
%endif
Suggests:	tar
Suggests:	zip
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

%package -n mate-file-manager-extension-engrampa
Summary:	Engrampa (archive manager) extension for Caja (MATE file manager)
Summary(pl.UTF-8):	Rozszerzenie Engrampa (zarządca archiwów) dla zarządcy plików Caja
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	mate-file-manager >= 1.1.0

%description -n mate-file-manager-extension-engrampa
Engrampa (archive manager) extension for Caja (MATE file manager).

%description -n mate-file-manager-extension-engrampa -l pl.UTF-8
Rozszerzenie Engrampa (zarządca archiwów) dla zarządcy plików Caja.

%prep
%setup -q

%build
mate-doc-prepare --copy --force
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_caja:--disable-caja-actions} \
	--disable-silent-rules \
	--disable-static \
	%{?with_gtk3:--with-gtk=3.0}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0/*.la

# just a copy of ur
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/ur_PK
# update naming convention
%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr@ije,sr@ijekavian}

# mate < 1.5 did not exist in pld, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/engrampa.convert

%find_lang engrampa --with-mate --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%scrollkeeper_update_post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f engrampa.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_bindir}/engrampa
%dir %{_libdir}/engrampa
%attr(755,root,root) %{_libdir}/engrampa/isoinfo.sh
%attr(755,root,root) %{_libdir}/engrampa/rpm2cpio
%{_datadir}/engrampa
%{_datadir}/glib-2.0/schemas/org.mate.engrampa.gschema.xml
%{_desktopdir}/engrampa.desktop
%{_iconsdir}/hicolor/*/apps/engrampa.*

%if %{with caja}
%files -n mate-file-manager-extension-engrampa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/caja/extensions-2.0/libcaja-engrampa.so
%endif
