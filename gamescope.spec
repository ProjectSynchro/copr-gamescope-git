%global commit f29f66d3d46d1bc3e8e0cd2f8facc5ba55e9152b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20250704
%global tag 3.16.14
%global libliftoff_minver 0.4.1

Name:           gamescope
Version:        %{tag}
Release:        1.%{git_date}git%{shortcommit}%{?dist}
Summary:        Micro-compositor for video games on Wayland

License:        BSD
URL:            https://github.com/ValveSoftware/gamescope
# Create stb.pc to satisfy dependency('stb')
Source0:        stb.pc

Patch1:         001-fix-linking-pr1812.patch
Patch2:         002-silence-meson-error.patch

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libeis-devel
BuildRequires:  pixman-devel
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(pixman-1) >= 0.42.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(libdrm) >= 2.4.113
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server) >= 1.21
BuildRequires:  pkgconfig(wayland-protocols) >= 1.41
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(luajit)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libavif) >= 1.0.0
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  spirv-headers-devel

## Bundled wlroots dependencies
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm) >= 17.1.0
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libinput) >= 1.21.0
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xkbcommon)



# Enforce the the minimum EVR to contain fixes for all of:
# CVE-2021-28021 CVE-2021-42715 CVE-2021-42716 CVE-2022-28041 CVE-2023-43898
# CVE-2023-45661 CVE-2023-45662 CVE-2023-45663 CVE-2023-45664 CVE-2023-45666
# CVE-2023-45667
BuildRequires:  stb_image-devel >= 2.28^20231011gitbeebb24-12
# Header-only library: -static is for tracking per guidelines
BuildRequires:  stb_image-static
BuildRequires:  stb_image_resize-devel
BuildRequires:  stb_image_resize-static
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_write-static
BuildRequires:  /usr/bin/glslangValidator
BuildRequires:  libdecor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  xorg-x11-server-Xwayland-devel
BuildRequires:  git

Requires:       xorg-x11-server-Xwayland
Requires:       gamescope-libs = %{version}-%{release}

%ifarch x86_64
Requires:       gamescope-libs(x86-32) = %{version}-%{release}
%endif

Recommends:     mesa-dri-drivers
Recommends:     mesa-vulkan-drivers

%description
%{name} is the micro-compositor optimized for running video games on Wayland.

%package libs
Summary:	libs for %{name}
%description libs
%summary

%prep
git clone --single-branch --branch master https://github.com/ValveSoftware/gamescope
cd gamescope
git checkout %{commit}
git submodule update --init --recursive

# Apply patches
%autopatch -p1

# Apply additional manual changes after patches
mkdir -p pkgconfig
cp %{SOURCE0} pkgconfig/stb.pc

# Replace spirv-headers include with the system directory
sed -i 's^../thirdparty/SPIRV-Headers/include/spirv/^/usr/include/spirv/^' src/meson.build

%build
cd gamescope
export PKG_CONFIG_PATH=pkgconfig

MESON_OPTIONS=(
   -Dbenchmark=enabled
   -Ddrm_backend=enabled
   -Denable_gamescope=true
   -Denable_gamescope_wsi_layer=true
   -Dpipewire=enabled
   -Dinput_emulation=enabled
   -Drt_cap=enabled
   -Davif_screenshots=enabled
   -Dsdl2_backend=enabled
   -Denable_openvr_support=false
   -Dforce_fallback_for=vkroots,wlroots,libliftoff
)

%meson "${MESON_OPTIONS[@]}"
%meson_build

%install
cd gamescope
%meson_install --skip-subprojects

%files
%license gamescope/LICENSE
%doc gamescope/README.md
%{_bindir}/gamescope
%{_bindir}/gamescopectl
%{_bindir}/gamescopereaper
%{_bindir}/gamescopestream
%{_datadir}/gamescope/
%files libs
%{_libdir}/*.so
%{_datadir}/vulkan/implicit_layer.d/

%changelog
%autochangelog
