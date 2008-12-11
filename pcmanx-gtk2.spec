%define version 0.3.8
%define release %mkrel 1
%define xuldir %(pkg-config --variable=libdir libxul)

Summary:   	User-friendly telnet client designed for BBS browsing
Name:      	pcmanx-gtk2
Version:   	%{version}
Release:   	%{release}
License: 	GPLv2+
Group:    	Networking/Other
Source0:	http://pcmanx.csie.net/release/%{name}-%{version}.tar.bz2
Patch0:		pcmanx-gtk2-0.3.7-fix-underlink.patch
Patch1:		pcmanx-gtk2-0.3.8-fix-xulrunner-include.pach
Url:       	http://pcmanx.csie.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gtk2-devel desktop-file-utils
BuildRequires:	X11-devel
BuildRequires:	intltool gettext-devel
BuildRequires:	imagemagick
BuildRequires:	xulrunner-devel
Provides:	pcmanx = %{version}-%{release}
Obsoletes:	pcmanx-pure-gtk2

%description
An easy-to-use telnet client mainly targets BBS users.
PCMan X is a newly developed GPL'd version of PCMan, a full-featured famous BBS
client formerly designed for MS Windows only.
It aimed to be an easy-to-use yet full-featured telnet client facilitating BBS
browsing with the ability to process double-byte characters.

%package -n mozilla-firefox-ext-pcmanx
Group:		Networking/Other
Summary:	pcmanx-gtk2 Mozillia Firefox plugin
Requires:	mozilla-firefox >= 0:3.0.0
Requires:	%name = %version

%description -n mozilla-firefox-ext-pcmanx
This package contains pcmanx-gtk2 plugin for Mozilla Firefox.

%prep
%setup -q -n %name-%version
%patch0 -p0
%patch1 -p0 -b .xrul

%build
./autogen.sh
%configure2_5x --disable-static --enable-plugin
%make

%install
rm -fr %buildroot
make install-strip DESTDIR=$RPM_BUILD_ROOT

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

%files -n mozilla-firefox-ext-pcmanx
%defattr(-,root,root)
%{xuldir}/components/*
%{xuldir}/plugins/*.so

%clean
rm -rf %{buildroot}
