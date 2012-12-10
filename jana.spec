# Tarfile created using git
# git clone git://git.gnome.org/jana
# git archive --format=tar --prefix=jana-0.4.5/ %{git_version} | bzip2 > jana-0.4.5-20100520.tar.bz2

%define gitdate 20100520
%define git_version acd72f2
%define tarfile %{name}-%{version}-%{gitdate}.tar.bz2
%define snapshot %{gitdate}git%{git_version}

%define major           0
%define libname         %mklibname %{name} %{major}
%define develname       %mklibname %{name} -d

Name:          jana
Version:       0.4.5
Release:       0.27.%{snapshot}
Summary:       An interface library for time-related PIM

Group:         System/Libraries
License:       LGPLv2
URL:           http://git.gnome.org/cgit/jana/
Source0:       %{tarfile}
Patch1:        jana.patch
Patch2:        jana-0.4.5-eds.patch

BuildRequires: evolution-data-server-devel
BuildRequires: gtk+3-devel
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires: pkgconfig(libedataserverui-3.0)
BuildRequires: gtk-doc
BuildRequires: intltool

# Require these because we're using a git snapshot
BuildRequires: libtool
BuildRequires: gnome-common

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
%package devel
Summary: Development package for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
 
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
%setup -q
%patch1 -p1 -b .gtk3
%patch2 -p1 -b .eds

%build
# Don't run configure from autogen.sh
sed -i 's|echo|exit 0|g' autogen.sh
./autogen.sh

%configure2_5x --disable-static --enable-gtk-doc 
%make

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'
mkdir -p %{buildroot}/%{_datadir}/doc/%{name}-%{version}
for f in `ls %{buildroot}/%{_datadir}/doc/`; do
  if [ -f %{buildroot}/%{_datadir}/doc/$f ]; then
    mv %{buildroot}/%{_datadir}/doc/$f %{buildroot}/%{_datadir}/doc/%{name}-%{version}
  fi
done


#Remove libtool archives.
rm -rf %{buildroot}/%{_libdir}/*.la

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

%files -n %{libname}-gtk
%{_libdir}/lib%{name}-gtk.so.*

%files -n %{libname}-ecal
%{_libdir}/lib%{name}-ecal.so.*

%files doc
%doc COPYING AUTHORS ChangeLog MAINTAINERS README
%{_datadir}/doc/%{name}-%{version}
%{_datadir}/gtk-doc/*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/jana/landwater.vmf
