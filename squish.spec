#
# Conditional build:
%bcond_without	openmp		# OpenMP support
%bcond_with	altivec		# use Altivec (PPC only)
%bcond_with	sse		# use SSE (x86 only)
%bcond_with	sse2		# use SSE2 (x86 only)
%bcond_without	static_libs	# static library
#
%ifarch pentium3 pentium4 %{x8664}
%define	with_sse	1
%endif
%ifarch pentium4 %{x8664}
%define	with_sse2	1
%endif
%{?with_sse:%define use_sse 1}
%{?with_sse2:%define use_sse 2}

Summary:	libsquish - DXT compression library
Summary(pl.UTF-8):	libsquish - biblioteka kompresji DXT
Name:		squish
Version:	1.15
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libsquish/libsquish-%{version}.tgz
# Source0-md5:	c02645800131e55b519ff8dbe7284f93
Patch0:		%{name}-cmake.patch
URL:		http://sourceforge.net/projects/libsquish/
BuildRequires:	cmake >= 2.8.3
%{?with_openmp:BuildRequires:	gcc-c++ >= 6:4.2}
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The squish library (libsquish) is an open source DXT compression
library written in C++ with the following features:
 - supports the DXT1, DXT3 and DXT5 formats,
 - optimised for both SSE and Altivec SIMD instruction sets,
 - builds on multiple platforms (x86 and PPC tested),
 - very simple interface.

%description -l pl.UTF-8
Biblioteka squish (libsquish) to mająca otwarte źródła biblioteka
kompresji DXT napisana w C++ o następujących cechach:
 - obsługuje formaty DXT1, DXT3 i DXT5,
 - jest zoptymalizowana dla instrukcji SIMD: SSE i Altivec,
 - buduje się na wielu platformach (testowane x86 i PPC),
 - ma bardzo prosty interfejs.

%package devel
Summary:	Header files for squish library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki squish
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for squish library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki squish.

%package static
Summary:	Static squish library
Summary(pl.UTF-8):	Statyczna biblioteka squish
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static squish library.

%description static -l pl.UTF-8
Statyczna biblioteka squish.

%prep
%setup -q -c
%patch0 -p1

%build
# disable sse setting on cmake level, control none/sse/sse2 settings through flags
CXXFLAGS="%{rpmcxxflags} %{?with_altivec:-maltivec} %{?with_sse2:-msse2}%{!?with_sse2:%{?with_sse:-msse}}"
CPPFLAGS="%{rpmcppflags} %{?with_altivec:-DSQUISH_USE_ALTIVEC=1} %{?use_sse:-DSQUISH_USE_SSE=%{use_sse}}"

install -d build
cd build
%cmake .. \
	%{!?with_openmp:-DBUILD_SQUISH_WITH_OPENMP=OFF} \
	-DBUILD_SQUISH_WITH_SSE2=OFF
%{__make}
cd ..

%if %{with static_libs}
install -d build-static
cd build-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF \
	%{!?with_openmp:-DBUILD_SQUISH_WITH_OPENMP=OFF} \
	-DBUILD_SQUISH_WITH_SSE2=OFF
%{__make}
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C build-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog.txt LICENSE.txt README.txt
%attr(755,root,root) %{_libdir}/libsquish.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsquish.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsquish.so
%{_includedir}/squish.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libsquish.a
%endif
