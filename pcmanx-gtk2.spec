%define version 0.3.5
%define release %mkrel 3

Summary:   	User-friendly telnet client designed for BBS browsing
Name:      	pcmanx-gtk2
Version:   	%{version}
Release:   	%{release}
License: 	GPL
Group:    	Networking/Other
Source0:	%{name}-%{version}.tar.gz
Url:       	http://pcmanx.csie.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gtk2-devel
BuildRequires:	X11-devel
BuildRequires:	intltool

%description
An easy-to-use telnet client mainly targets BBS users.
PCMan X is a newly developed GPL'd version of PCMan, a full-featured famous BBS
client formerly designed for MS Windows only.
It aimed to be an easy-to-use yet full-featured telnet client facilitating BBS
browsing with the ability to process double-byte characters.

%prep

%setup
%configure --disable-shared

%build
make

%install
make install-strip DESTDIR=$RPM_BUILD_ROOT

# icon
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
install -m 644 $RPM_BUILD_ROOT%{_datadir}/pixmaps/pcmanx.png $RPM_BUILD_ROOT%{_iconsdir}/pcmanx.png

# menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat > $RPM_BUILD_ROOT%{_menudir}/%{name} << _EOF_
?package(%{name}): \
 icon="pcmanx.png" \
 title="PCManX" \
 longtitle="Friendly BBS Client" \
 needs="x11" \
 section="Internet/Other" \
 command="%{_bindir}/pcmanx" \
 xdg="true"
_EOF_

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=PCManX
Comment=Friendly BBS Client
Exec=%_bindir/pcmanx
Icon=pcmanx.png
Terminal=false
Type=Application
Categories=X-MandrivaLinux-Internet-Other;Network;
EOF


%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/pcmanx
%{_libdir}/libpcmanx_core.*
%{_iconsdir}/pcmanx.png
%{_datadir}/pcmanx/*
%{_datadir}/pixmaps/pcmanx.png
%{_datadir}/applications/*
%{_datadir}/locale/zh_TW/LC_MESSAGES/pcmanx.mo
%{_datadir}/locale/zh_CN/LC_MESSAGES/pcmanx.mo
%{_menudir}/%{name}

%clean
rm -rf %{buildroot}


