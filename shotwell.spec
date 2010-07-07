Name:           shotwell
Version:        0.5.90
Release:        2%{?dist}
Summary:        A photo organizer for the GNOME desktop

Group:          Applications/Multimedia
# LGPLv2+ for the code
# CC-BY-SA for some of the icons
License:        LGPLv2+ and CC-BY-SA
URL:            http://www.yorba.org/shotwell/
Source0:        http://www.yorba.org/download/shotwell/0.5/unstable/shotwell-%{version}.tar.bz2
BuildRequires:  gtk2-devel
BuildRequires:  GConf2-devel
BuildRequires:  sqlite-devel
BuildRequires:  vala-devel >= 0.7.10
BuildRequires:  libgee-devel
BuildRequires:  libgudev-devel
BuildRequires:  libxml2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  unique-devel
BuildRequires:  libexif-devel
BuildRequires:  gexiv2-devel
BuildRequires:  libraw-devel
BuildRequires:  libgphoto2-devel
BuildRequires:  webkitgtk-devel
BuildRequires:  libsoup-devel
BuildRequires:  libusb-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext

%description
Shotwell is a new open source photo organizer designed for the GNOME desktop
environment. It allows you to import photos from your camera, view and edit
them, and share them with others.

%prep
%setup -q

%build
./configure --prefix=/usr --disable-schemas-install
sed -i -e 's/\\n/\n/g' configure.mk
sed -i -e 's/^CFLAGS=.*$/CFLAGS=%{optflags}/' Makefile
make %{?_smp_mflags}


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export XDG_DISABLE_MAKEFILE_UPDATES=1
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/shotwell.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/shotwell-viewer.desktop

%find_lang %{name}

%post
update-desktop-database &>/dev/null || :
%gconf_schema_upgrade shotwell
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%pre
%gconf_schema_prepare shotwell

%preun
%gconf_schema_remove shotwell

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING MAINTAINERS NEWS THANKS AUTHORS
%{_sysconfdir}/gconf/schemas/shotwell.schemas
%{_bindir}/shotwell
%{_datadir}/shotwell
%{_datadir}/applications/shotwell.desktop
%{_datadir}/applications/shotwell-viewer.desktop
%{_datadir}/icons/hicolor/scalable/apps/shotwell.svg


%changelog
* Wed Jul  7 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.90-2
- Rebuild against newer webkitgtk

* Wed May 26 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.90-1
- Update to 0.5.90
- Scriptlet updates

* Wed May 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.2-1
- Update to 0.5.2
- Translation updates for Czech, Finnish, Greek, Ukrainian and Russian

* Fri Mar 12 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.0-1
- Update to 0.5.0
- Many new features, see http://www.yorba.org/shotwell/

* Mon Jan 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.3-1
- Update to 0.4.3

* Tue Jan  5 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.2-1
- Update to 0.4.2

* Wed Dec 23 2009 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Fri Dec 18 2009 Matthias Clasen <mclasen@redhat.com> - 0.4.0-0.1.20091218svn
- 0.4 snapshot

* Thu Nov 12 2009 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Tue Nov  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.3.0-1
- Version 0.3.0

* Thu Aug 20 2009 Michel Salim <salimma@fedoraproject.org> - 0.2.0-3
- Rebuild against new libgee

* Sun Aug 12 2009  Matthias Clasen <mclasen@redhat.com> - 0.2.0-2.fc12
- Bring icon cache handling in sync with current guidelines

* Sun Aug  9 2009  Matthias Clasen <mclasen@redhat.com> - 0.2.0-1.fc12
- Initial packaging
