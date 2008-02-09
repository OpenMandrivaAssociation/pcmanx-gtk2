%define version 0.3.7
%define release %mkrel 2
%define firefox_epoch %(rpm -q --queryformat %{EPOCH} mozilla-firefox)
%define firefox_version %(rpm -q --queryformat %{VERSION} mozilla-firefox)

Summary:   	User-friendly telnet client designed for BBS browsing
Name:      	pcmanx-gtk2
Version:   	%{version}
Release:   	%{release}
License: 	GPLv2+
Group:    	Networking/Other
Source0:	http://pcmanx.csie.net/release/%{name}-%{version}.tar.bz2
Url:       	http://pcmanx.csie.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gtk2-devel desktop-file-utils
BuildRequires:	X11-devel
BuildRequires:	intltool
BuildRequires:	ImageMagick
BuildRequires:	mozilla-firefox-devel
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
Requires:	mozilla-firefox = %{firefox_epoch}:%{firefox_version}
Requires:	%name = %version

%description -n mozilla-firefox-ext-pcmanx
This package contains pcmanx-gtk2 plugin for Mozilla Firefox.

%prep
%setup -q

%build
%configure2_5x --disable-static --enable-plugin
%make

%install
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

%post
%update_menus

%postun
%clean_menus

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
%{_libdir}/firefox-%{firefox_version}/components/*
%{_libdir}/firefox-%{firefox_version}/plugins/*.so

%clean
rm -rf %{buildroot}
