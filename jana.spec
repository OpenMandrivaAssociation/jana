%define version 0.0.0
%define rel 6
%define snapshot git20090406
%define release %mkrel 0.%{snapshot}.%{rel}

%define sversion %{version}%{snapshot}

%define major           0
%define libname         %mklibname %{name} %{major}
%define develname       %mklibname %{name} -d

Name: jana
Summary: An interface library for time-related PIM
Group: System/Libraries
Version: %{version}
License: GPLv2
URL: http://git.gnome.org/cgit/jana
Release: %{release}
Source0: %{name}-%{snapshot}.tar.gz
Patch0: jana-20091028-fix-jana-task-get-priority.patch
Patch1: jana-20091028-add-po-to-subdirs.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: intltool
BuildRequires: gtk2-devel
BuildRequires: gnome-common
BuildRequires: gtk-doc
BuildRequires: libdbus-1-devel
BuildRequires: libgladeui-devel
BuildRequires: libedataserver-devel
BuildRequires: evolution-data-server-devel

%description
An interface library for time-related personal information management related
data.

%package -n %{libname}
Summary: Jana development documentation
Group: System/Libraries

%description -n %{libname}
An interface library for time-related personal information management related
data.

%package doc
Summary: Jana development documentation
Group: System/Libraries

%description doc
Documentation for the Jana libraries

%package -n %{libname}-gtk
Summary: Jana GTK
Group: System/Libraries

%description -n %{libname}-gtk
Jana's GTK support

%package -n %{libname}-ecal
Summary: Jana ECAL
Group: System/Libraries

%description -n %{libname}-ecal
Jana's ECAL support


%package -n %{develname}
Summary: Jana development environment
Group: Development/C

Requires: %{libname} = %{version}-%{release}
Requires: %{libname}-gtk = %{version}-%{release}
Requires: %{libname}-ecal = %{version}-%{release}
Provides: %{name}-devel

%description -n %{develname}
Header files and libraries for building applications with Jana

%prep
%setup -q -n %{name}-%{snapshot}
%patch0 -p1
%patch1 -p1

%build
NOCONFIGURE=cassoulet ./autogen.sh
%configure2_5x --enable-gtk-doc --enable-glade
%make

%install
rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}-%{version}
for f in `ls %{buildroot}/%{_datadir}/doc/`; do
  if [ -f %{buildroot}/%{_datadir}/doc/$f ]; then
    mv %{buildroot}/%{_datadir}/doc/$f %{buildroot}/%{_datadir}/doc/%{name}-%{version}
  fi
done

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so.*

%files -n %{libname}-gtk
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-gtk.so.*

%files -n %{libname}-ecal
%defattr(-,root,root,-)
%{_libdir}/lib%{name}-ecal.so.*

%files doc
%defattr(-,root,root,-)
%doc COPYING AUTHORS ChangeLog MAINTAINERS README
%{_datadir}/doc
%{_datadir}/gtk-doc/*

%files -n %{develname}
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.la
%{_datadir}/jana/landwater.vmf
%{_datadir}/glade3/catalogs/*
