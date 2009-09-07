%define version 0.3.9
%define release %mkrel 1

Summary:   	User-friendly telnet client designed for BBS browsing
Name:      	pcmanx-gtk2
Version:   	%{version}
Release:   	%{release}
License: 	GPLv2+
Group:    	Networking/Other
Source0:	http://pcmanx-gtk2.googlecode.com/svn/website/release/%{name}-%{version}.tar.bz2
Url:       	http://code.google.com/p/pcmanx-gtk2/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gtk2-devel desktop-file-utils
BuildRequires:	X11-devel
BuildRequires:	intltool gettext-devel
BuildRequires:	imagemagick
Provides:	pcmanx = %{version}-%{release}
Obsoletes:	pcmanx-pure-gtk2

%description
An easy-to-use telnet client mainly targets BBS users.
PCMan X is a newly developed GPL'd version of PCMan, a full-featured famous BBS
client formerly designed for MS Windows only.
It aimed to be an easy-to-use yet full-featured telnet client facilitating BBS
browsing with the ability to process double-byte characters.

%prep
%setup -q -n %name-%version

%build
%configure2_5x --disable-static --disable-plugin
%make

%install
rm -fr %buildroot
%makeinstall_std

# icon
mkdir -p $RPM_BUILD_ROOT{%{_iconsdir},%{_liconsdir},%{_miconsdir}}
install -m 644 data/pcmanx.png $RPM_BUILD_ROOT%{_liconsdir}/pcmanx.png
convert -resize 32x32 data/pcmanx.png $RPM_BUILD_ROOT%{_iconsdir}/pcmanx.png
convert -resize 16x16 data/pcmanx.png $RPM_BUILD_ROOT%{_miconsdir}/pcmanx.png

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="RemoteAccess" \
	--remove-key='Encoding' \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
	$RPM_BUILD_ROOT%{_datadir}/applications/*

# fwang: remove devel files
rm -f %buildroot%_libdir/{*.la,*.so}

%find_lang pcmanx

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files -f pcmanx.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/pcmanx
%{_libdir}/libpcmanx_core.so.*
%{_iconsdir}/pcmanx.png
%{_liconsdir}/pcmanx.png
%{_miconsdir}/pcmanx.png
%{_datadir}/pcmanx
%{_datadir}/pixmaps/pcmanx.png
%{_datadir}/applications/*.desktop

%clean
rm -rf %{buildroot}
