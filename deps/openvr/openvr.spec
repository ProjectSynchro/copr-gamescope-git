# Samples aren't supported on i686
%ifarch i686
%bcond_with samples
%else
%bcond_without samples
%endif

%global common_description %{expand:
OpenVR is an API and runtime that allows access to VR hardware from multiple
vendors without requiring that applications have specific knowledge of the
hardware they are targeting.}

Name:           openvr
Version:        2.5.1
Release:        %autorelease
Summary:        OpenVR SDK

License:        BSD-3-Clause
URL:            https://github.com/ValveSoftware/openvr
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
# Use GNUInstallDirs to determine lib install path
Patch:          %{url}/pull/1511.patch
# Add ability to build with system installed jsoncpp
Patch:          %{url}/pull/1716.patch
# Add option to neuter the steamvr check
Patch:          openvr-skip-steamvr-check.patch
# Add ability to build with system installed SDL2 and Vulkan
Patch:          openvr-use-system-sdl2-vulkan.patch
# Define soversion for the OpenVR API library
Patch:          openvr-api-soversion.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  jsoncpp-devel

%if %{with samples}
BuildRequires:  chrpath
BuildRequires:  glslang
BuildRequires:  glslc
BuildRequires:  sed

BuildRequires:  glew-devel
BuildRequires:  libGL-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  SDL2-devel
BuildRequires:  vulkan-loader-devel
%endif

%description    %{common_description}

%package        api
Summary:        OpenVR API libraries

%description    api %{common_description}

This package provides the shared libraries for the OpenVR Application API.

%package        devel
Summary:        Development headers for %{name}
Requires:       jsoncpp-devel
Requires:       %{name}-api%{?_isa} = %{version}-%{release}

%description    devel %{common_description}

This package provides the development headers for OpenVR.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc %{common_description}

This package provides additional documentation for OpenVR.

%if %{with samples}
%package        samples
Summary:        OpenVR Samples

%description    samples %{common_description}

This package provides various sample programs and drivers using OpenVR.
%endif

%prep
%autosetup -p1

# Delete prebuilt binaries and libraries
rm -r bin lib samples/bin/{android*,linux*,win*}

# Delete prebuilt shaders
rm samples/bin/shaders/*.spv

# Delete bundled library sources
rm -r thirdparty samples/thirdparty

%if %{with samples}
# Fix paths in samples
sed -i 's:../hellovr_actions.json:%{_datadir}/%{name}/hellovr_actions.json:' \
  samples/hellovr_opengl/hellovr_opengl_main.cpp
sed -i 's:../shaders/:%{_libdir}/%{name}/shaders/:' \
  samples/hellovr_vulkan/hellovr_vulkan_main.cpp
sed -i 's:../cube_texture.png:%{_datadir}/%{name}/cube_texture.png:' \
  samples/hellovr_opengl/hellovr_opengl_main.cpp \
  samples/hellovr_vulkan/hellovr_vulkan_main.cpp

# Disable broken simplehmd driver
# https://bugzilla.redhat.com/show_bug.cgi?id=2275022
sed -i '/simplehmd/d' samples/drivers/drivers/CMakeLists.txt
%endif

%build
# Build library
%cmake \
  -DBUILD_SHARED=ON \
  -DUSE_SYSTEM_JSONCPP=ON
%cmake_build

%if %{with samples}
# Build shaders
# see samples/bin/shaders/build_vulkan_shaders.bat
for f in samples/bin/shaders/*.hlsl; do
  base="$(dirname "$f")/$(basename "$f" .hlsl)"

  glslangValidator \
    -S vert \
    -e VSMain \
    -o "${base}_vs.spv" \
    -V \
    --hlsl-iomap \
    --auto-map-bindings \
    --shift-cbuffer-binding 0 \
    --shift-texture-binding 1 \
    --shift-sampler-binding 2 \
    -D "$f"

  glslangValidator \
    -S frag \
    -e PSMain \
    -o "${base}_ps.spv" \
    -V \
    --hlsl-iomap \
    --auto-map-bindings \
    --shift-cbuffer-binding 0 \
    --shift-texture-binding 1 \
    --shift-sampler-binding 2 \
    -D "$f"
done

# Build samples
pushd samples
%cmake \
  -DSKIP_STEAMVR_CHECK=ON \
  -DUSE_SYSTEM_SDL2=ON \
  -DUSE_SYSTEM_VULKAN=ON
%cmake_build

# Build sample drivers
pushd drivers
%cmake
%cmake_build
%endif

%install
%cmake_install

%if %{with samples}
# Samples have to be installed manually
install -Dpm0755 -t %{buildroot}%{_bindir} samples/bin/linux%{__isa_bits}/*
install -Dpm0644 -t %{buildroot}%{_datadir}/%{name} \
  samples/bin/*.json \
  samples/bin/cube_texture.png
install -Dpm0644 -t %{buildroot}%{_libdir}/%{name}/shaders \
  samples/bin/shaders/*.spv

# Sample drivers have to be installed manually
install -Dpm0755 -t %{buildroot}%{_libdir}/%{name}/drivers \
  samples/drivers/%{_vpath_builddir}/drivers/*/libdriver_*.so

# Fix runpath in samples and sample drivers
chrpath -d %{buildroot}%{_bindir}/* %{buildroot}%{_libdir}/%{name}/drivers/*.so
%endif

%files api
%license LICENSE
%doc README.md
%{_libdir}/libopenvr_api.so.2{,.*}

%files devel
%{_includedir}/%{name}
%{_datadir}/pkgconfig/%{name}.pc
%{_libdir}/libopenvr_api.so

%files doc
%license LICENSE
%doc docs controller_callouts

%if %{with samples}
%files samples
%license LICENSE
%{_bindir}/hellovr_opengl
%{_bindir}/hellovr_vulkan
%{_bindir}/helloworldoverlay
%{_bindir}/tracked_camera_openvr_sample
%{_datadir}/%{name}/
%{_libdir}/%{name}/
%endif

%changelog
%autochangelog
