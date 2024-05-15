# Build with aom
%bcond_without aom
# Build SVT-AV1
%bcond_without svt
%if (0%{?rhel} && 0%{?rhel} < 9) || 0%{?rhel} >= 10
%bcond_with rav1e
%else
%bcond_without rav1e
%endif
%if 0%{?rhel} >= 10
%bcond_with gtest
%else
%bcond_without gtest
%endif
%bcond_without check

Name:           libavif
Version:        1.0.4
Release:        %autorelease
Summary:        Library for encoding and decoding .avif files

License:        BSD-2-Clause
URL:            https://github.com/AOMediaCodec/libavif
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# Encode alpha as 4:2:0 with SVT. Fix build with SVT-AV1 2.0.0
Patch0:         https://github.com/AOMediaCodec/libavif/commit/b10d2697e9ed2fb09cb722335ff4342c353612b8.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
%{?with_check:%{?with_gtest:BuildRequires:  gtest-devel}}
BuildRequires:  nasm
%if %{with aom}
BuildRequires:  pkgconfig(aom)
%endif
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
%{?with_rav1e:BuildRequires:  pkgconfig(rav1e)}
%{?with_svt:BuildRequires:  pkgconfig(SvtAv1Enc)}
BuildRequires:  pkgconfig(zlib)

%description
This library aims to be a friendly, portable C implementation of the AV1 Image
File Format, as described here:

https://aomediacodec.github.io/av1-avif/

%package devel
Summary:        Development files for libavif
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package holds the development files for libavif.

%package tools
Summary:        Tools to encode and decode AVIF files

%description tools
This library aims to be a friendly, portable C implementation of the AV1 Image
File Format, as described here:

https://aomediacodec.github.io/av1-avif/

This package holds the commandline tools to encode and decode AVIF files.

%package     -n avif-pixbuf-loader
Summary:        AVIF image loader for GTK+ applications
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
Requires:       gdk-pixbuf2%{?_isa}

%description -n avif-pixbuf-loader
Avif-pixbuf-loader contains a plugin to load AVIF images in GTK+ applications.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    %{?with_aom:-DAVIF_CODEC_AOM=1} \
    -DAVIF_CODEC_DAV1D=1 \
    %{?with_rav1e:-DAVIF_CODEC_RAV1E=1} \
    %{?with_svt:-DAVIF_CODEC_SVT=1} \
    -DAVIF_BUILD_APPS=1 \
    -DAVIF_BUILD_GDK_PIXBUF=1 \
    %{?with_check:-DAVIF_BUILD_TESTS=1 -DAVIF_ENABLE_GTEST=%{with gtest}}
%cmake_build

%install
%cmake_install

%if %{with check}
%check
%ctest
%endif

%files
%license LICENSE
# Do not glob the soname
%{_libdir}/libavif.so.16*
%{_datadir}/thumbnailers/avif.thumbnailer

%files devel
%{_libdir}/libavif.so
%{_includedir}/avif/
%{_libdir}/cmake/libavif/
%{_libdir}/pkgconfig/libavif.pc

%files tools
%doc CHANGELOG.md README.md
%{_bindir}/avifdec
%{_bindir}/avifenc

%files -n avif-pixbuf-loader
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-avif.so

%changelog
%autochangelog
