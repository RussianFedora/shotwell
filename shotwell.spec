Name:           shotwell
Version:        0.3.2
Release:        3%{?dist}
Summary:        A photo organizer for the GNOME desktop

Group:          Applications/Multimedia
# LGPLv2+ for the code
# CC-BY-SA for some of the icons
License:        LGPLv2+ and CC-BY-SA
URL:            http://www.yorba.org/shotwell/
Source0:        http://www.yorba.org/download/shotwell/0.3/shotwell-%{version}.tar.bz2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel
BuildRequires:  GConf2-devel
BuildRequires:  sqlite-devel
BuildRequires:  vala-devel
BuildRequires:  libgee-devel
BuildRequires:  hal-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  unique-devel
BuildRequires:  libexif-devel
BuildRequires:  libgphoto2-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext

Patch0: prefixly-correct.patch

%description
Shotwell is a new open source photo organizer designed for the GNOME desktop
environment. It allows you to import photos from your camera, view and edit
them, and share them with others.

%prep
%setup -q
%patch0 -p1 -b .prefixly-correct

%build
./configure --prefix=/usr
sed -i -e 's/\\n/\n/g' configure.mk
sed -i -e 's/^CFLAGS=.*$/CFLAGS=%{optflags}/' Makefile
sed -i -e 's/-mfpmath=sse -march=nocona//' Makefile
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
export XDG_DISABLE_MAKEFILE_UPDATES=1
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/shotwell.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/shotwell-viewer.desktop

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/shotwell.schemas > /dev/null || :

%pre
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/shotwell.schemas > /dev/null || :
fi

%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/shotwell.schemas > /dev/null || :
fi

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

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
* Wed Dec  9 2009 Peter Robinson <pbrobinson@gmail.com> - 0.3.2-2
- Drop x86 specific CFLAGS optimisations

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
