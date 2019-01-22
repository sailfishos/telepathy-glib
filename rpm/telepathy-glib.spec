Name:       telepathy-glib
Summary:    GLib bindings for Telepathy
Version:    0.21.2
Release:    1
Group:      System/Libraries
License:    LGPLv2+
URL:        http://telepathy.freedesktop.org/wiki/
Source0:    http://telepathy.freedesktop.org/releases/telepathy-glib/%{name}-%{version}.tar.gz
Source1:    mktests.sh
Patch0:     nemo-test-packaging.patch
Patch1:     disable-gtkdoc.patch
Patch2:     memory-leak.patch
Patch3:     group_prop_crash.patch
Patch4:     build-on-busybox.patch
Requires:   glib2 >= 2.32.0
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.90
BuildRequires:  pkgconfig(dbus-1) >= 0.95
BuildRequires:  pkgconfig(glib-2.0) >= 2.32.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.32.0
BuildRequires:  pkgconfig(gio-2.0) >= 2.32.0
BuildRequires:  libxslt
BuildRequires:  python

%description
Telepathy-GLib is a GObject-based C binding for Telepathy,
a unified framework for all forms of real time conversations,
including instant messaging, IRC, voice calls and video calls.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Library, headers, and other files for developing applications
that use Telepathy-GLib.


%package tests
Summary:    Tests package for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-examples

%description tests
The %{name}-tests package contains tests and
tests.xml for automated testing.


%package examples
Summary:    Example programs for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description examples
The %{name}-examples package contains example 
programs. Some are needed for the tests.


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.


%prep
%setup -q -n %{name}-%{version}/telepathy-glib

# nemo-test-packaging.patch
%patch0 -p1
# disable-gtkdoc.patch
%patch1 -p1
# memory-leak.patch
%patch2 -p1
# group_prop_crash.patch
%patch3 -p1
# build-on-busybox.patch
%patch4 -p1

%__cp $RPM_SOURCE_DIR/mktests.sh tests/
touch tests/INSIGNIFICANT
%__chmod 0755 tests/mktests.sh
%__chmod 0644 tests/INSIGNIFICANT

%build
%autogen --disable-static \
  --enable-silent-rules \
  --disable-gtk-doc \
  --enable-installed-tests

make %{?_smp_mflags}

tests/mktests.sh > tests/tests.xml

%install
rm -rf %{buildroot}
%make_install

install -m 0644 tests/tests.xml $RPM_BUILD_ROOT/opt/tests/telepathy-glib/tests.xml
install -m 0644 tests/INSIGNIFICANT $RPM_BUILD_ROOT/opt/tests/telepathy-glib/INSIGNIFICANT
install -m 0644 tests/README $RPM_BUILD_ROOT/opt/tests/telepathy-glib/README
mkdir -p $RPM_BUILD_ROOT%{_datadir}/telepathy/managers
mkdir -p $RPM_BUILD_ROOT%{_datadir}/telepathy/clients
mkdir -p $RPM_BUILD_ROOT%{_includedir}/telepathy-1.0

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
install -m0644 AUTHORS $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libtelepathy-glib*.so.*

%files devel
%defattr(-,root,root,-)
%dir %{_datadir}/telepathy
%dir %{_datadir}/telepathy/managers
%dir %{_datadir}/telepathy/clients
%dir %{_includedir}/telepathy-1.0
%{_libdir}/libtelepathy-glib.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/telepathy-1.0/%{name}/

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}

%files examples
%defattr(-,root,root,-)
%{_bindir}/telepathy-example*
%{_libexecdir}/telepathy-example*
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.ConnectionManager.example*
%{_datadir}/telepathy/managers/example*

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}
