%define version 0.3.6
%define release %mkrel 1

Summary:   	User-friendly telnet client designed for BBS browsing
Name:      	pcmanx-gtk2
Version:   	%{version}
Release:   	%{release}
License: 	GPL
Group:    	Networking/Other
Source0:	http://pcmanx.csie.net/release/%{name}-%{version}.tar.bz2
Url:       	http://pcmanx.csie.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:	gtk2-devel desktop-file-utils
BuildRequires:	X11-devel
BuildRequires:	intltool
Provides:	pcmanx = %{version}-%{release}
Obsoletes:	pcmanx-pure-gtk2

%description
An easy-to-use telnet client mainly targets BBS users.
PCMan X is a newly developed GPL'd version of PCMan, a full-featured famous BBS
client formerly designed for MS Windows only.
It aimed to be an easy-to-use yet full-featured telnet client facilitating BBS
browsing with the ability to process double-byte characters.

%prep

%setup -q

%build
%configure2_5x --disable-static
make

%install
make install-strip DESTDIR=$RPM_BUILD_ROOT

# icon
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
install -m 644 $RPM_BUILD_ROOT%{_datadir}/pixmaps/pcmanx.png $RPM_BUILD_ROOT%{_iconsdir}/pcmanx.png

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications/ \
	$RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang pcmanx

%post
%update_menus

%postun
%clean_menus

%files -f pcmanx.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/pcmanx
%{_libdir}/libpcmanx_core.*
%{_iconsdir}/pcmanx.png
%{_datadir}/pcmanx/*
%{_datadir}/pixmaps/pcmanx.png
%{_datadir}/applications/*.desktop

%clean
rm -rf %{buildroot}
