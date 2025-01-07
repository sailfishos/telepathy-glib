Name:       telepathy-glib
Summary:    GLib bindings for Telepathy
Version:    0.24.2
Release:    1
License:    LGPLv2+
URL:        http://telepathy.freedesktop.org/wiki/
Source0:    %{name}-%{version}.tar.gz
Source1:    mktests.sh
Patch1:     0001-Adjust-test-installation-path.patch
Patch2:     0002-Disable-gtk-doc.patch
Patch3:     0003-Use-q-instead-of-c-for-diff.patch
Patch4:     0004-Use-readlink-f-which-is-supported-by-busybox.patch
Requires:   glib2 >= 2.32.0
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.90
BuildRequires:  pkgconfig(dbus-1) >= 0.95
BuildRequires:  pkgconfig(glib-2.0) >= 2.32.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.32.0
BuildRequires:  pkgconfig(gio-2.0) >= 2.32.0
BuildRequires:  libxslt
BuildRequires:  python3-base

%description
Telepathy-GLib is a GObject-based C binding for Telepathy,
a unified framework for all forms of real time conversations,
including instant messaging, IRC, voice calls and video calls.


%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
Library, headers, and other files for developing applications
that use Telepathy-GLib.


%package tests
Summary:    Tests package for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-examples

%description tests
The %{name}-tests package contains tests and
tests.xml for automated testing.


%package examples
Summary:    Example programs for %{name}
Requires:   %{name} = %{version}-%{release}

%description examples
The %{name}-examples package contains example 
programs. Some are needed for the tests.


%package doc
Summary:   Documentation for %{name}
Requires:  %{name} = %{version}-%{release}

%description doc
%{summary}.


%prep
%autosetup -p1 -n %{name}-%{version}/telepathy-glib

%__cp $RPM_SOURCE_DIR/mktests.sh tests/
touch tests/INSIGNIFICANT
%__chmod 0755 tests/mktests.sh
%__chmod 0644 tests/INSIGNIFICANT

%build
%autogen --disable-static \
  --enable-silent-rules \
  --disable-gtk-doc \
  --enable-installed-tests

%make_build

tests/mktests.sh > tests/tests.xml

%install
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
%license COPYING
%{_libdir}/libtelepathy-glib*.so.*

%files devel
%dir %{_datadir}/telepathy
%dir %{_datadir}/telepathy/managers
%dir %{_datadir}/telepathy/clients
%dir %{_includedir}/telepathy-1.0
%{_libdir}/libtelepathy-glib.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/telepathy-1.0/%{name}/

%files tests
/opt/tests/%{name}

%files examples
%{_bindir}/telepathy-example*
%{_libexecdir}/telepathy-example*
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.ConnectionManager.example*
%{_datadir}/telepathy/managers/example*

%files doc
%{_docdir}/%{name}-%{version}
