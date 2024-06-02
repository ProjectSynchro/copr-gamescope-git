%global commit c5a5ba00b655caa1c10656dfe3ae09e281ec0544
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20240602T161406Z
%global tag 3.14.18
%global libliftoff_minver 0.5.0
%global reshade_commit 4245743a8c41abbe3dc73980c1810fe449359bf1
%global reshade_shortcommit %(c=%{reshade_commit}; echo ${c:0:7})

Name:           gamescope
Version:        %{tag}^%{git_date}.g%{shortcommit}
Release:        %autorelease
Summary:        Micro-compositor for video games on Wayland

License:        BSD
URL:            https://github.com/ValveSoftware/gamescope
Source0:        %{url}/archive/%{commit}.tar.gz
# Create stb.pc to satisfy dependency('stb')
Source1:        stb.pc
Source2:        https://github.com/Joshua-Ashton/reshade/archive/%{reshade_commit}/reshade-%{reshade_shortcommit}.tar.gz

Patch01:        0001-cstdint.patch

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  libeis-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXcursor-devel
BuildRequires:  pkgconfig(libdecor-0)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.17
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libavif) >= 1.0.0
BuildRequires:  (pkgconfig(wlroots) >= 0.18.0 with pkgconfig(wlroots) < 0.19)
BuildRequires:  (pkgconfig(libliftoff) >= 0.5.0 with pkgconfig(libliftoff) < 0.6)
BuildRequires:  (pkgconfig(openvr) >= 2 with pkgconfig(openvr) < 3)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  spirv-headers-devel
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
BuildRequires:  vkroots-devel
BuildRequires:  /usr/bin/glslangValidator

# libliftoff hasn't bumped soname, but API/ABI has changed for 0.2.0 release
Requires:       libliftoff%{?_isa} >= %{libliftoff_minver}
Requires:       xorg-x11-server-Xwayland
Recommends:     mesa-dri-drivers
Recommends:     mesa-vulkan-drivers

%description
%{name} is the micro-compositor optimized for running video games on Wayland.

%prep
%autosetup -p1 -a2 -N -n %{name}-%{commit}
# Install stub pkgconfig file
mkdir -p pkgconfig
cp %{SOURCE1} pkgconfig/stb.pc

# Replace spirv-headers include with the system directory
sed -i 's^../thirdparty/SPIRV-Headers/include/spirv/^/usr/include/spirv/^' src/meson.build

# Push in reshade from sources instead of submodule
rm -rf src/reshade && mv reshade-%{reshade_commit} src/reshade

%autopatch -p1

%build
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:pkgconfig

MESON_OPTIONS=(
   -Dpipewire=enabled 
   -Denable_openvr_support=true 
   -Dforce_fallback_for=[]
)

%meson "${MESON_OPTIONS[@]}"
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%caps(cap_sys_nice=eip) %{_bindir}/gamescope
%{_bindir}/gamescopestream
%{_libdir}/libVkLayer_FROG_gamescope_wsi_*.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.*.json


%changelog
%autochangelog
