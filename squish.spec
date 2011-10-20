#
# Conditional build:
%bcond_with	altivec		# use Altivec (PPC only)
%bcond_with	sse		# use SSE (x86 only)
%bcond_with	sse2		# use SSE2 (x86 only)
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
Version:	1.11
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: http://code.google.com/p/libsquish/downloads/list
Source0:	http://libsquish.googlecode.com/files/%{name}-%{version}.zip
# Source0-md5:	150ba1117d2c1678de12650357787994
Patch0:		%{name}-shared.patch
Patch1:		%{name}-gcc4.patch
URL:		http://code.google.com/p/libsquish/
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
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
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} %{?with_altivec:-maltivec} %{?use_sse:-msse}" \
	CPPFLAGS="%{rpmcppflags} %{?with_altivec:-DSQUISH_USE_ALTIVEC=1} %{?use_sse:-DSQUISH_USE_SSE=%{use_sse}}" \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	includedir=%{_includedir} \
	libdir=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README texture_compression_s3tc.txt
%attr(755,root,root) %{_libdir}/libsquish.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsquish.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsquish.so
%{_libdir}/libsquish.la
%{_includedir}/squish.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libsquish.a
