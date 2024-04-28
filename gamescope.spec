%global commit a1578b6fc0a653632987291e83ea847d098221ef
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20240415
%global tag 3.14.7
%global libliftoff_minver 0.4.1
%global reshade_commit 4245743a8c41abbe3dc73980c1810fe449359bf1
%global reshade_shortcommit %(c=%{reshade_commit}; echo ${c:0:7})
%global vkroots_commit 5c217cd43ca1ceecaa6acfc93a81cdc615929155
%global vkroots_shortcommit %(c=%{vkroots_commit}; echo ${c:0:7})
%global wlroots_commit a5c9826e6d7d8b504b07d1c02425e6f62b020791
%global wlroots_shortcommit %(c=%{wlroots_commit}; echo ${c:0:7})

Name:           gamescope
Version:        %{tag}^%{git_date}git%{shortcommit}
Release:        %autorelease
Summary:        Micro-compositor for video games on Wayland

License:        BSD
URL:            https://github.com/ValveSoftware/gamescope
Source0:        %{url}/archive/%{commit}.tar.gz
# Create stb.pc to satisfy dependency('stb')
Source1:        stb.pc
Source2:        https://github.com/Joshua-Ashton/reshade/archive/%{reshade_commit}/reshade-%{reshade_shortcommit}.tar.gz
Source3:        https://github.com/Joshua-Ashton/vkroots/archive/%{vkroots_commit}/vkroots-%{vkroots_shortcommit}.tar.gz
Source4:        https://github.com/Joshua-Ashton/wlroots/archive/%{wlroots_commit}/wlroots-%{wlroots_shortcommit}.tar.gz

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
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.17
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libavif)
#BuildRequires:  (pkgconfig(wlroots) >= 0.18.0 with pkgconfig(wlroots) < 0.19)
BuildRequires:  (pkgconfig(libliftoff) >= 0.4.1 with pkgconfig(libliftoff) < 0.5)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(libdecor-0)
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
#BuildRequires:  vkroots-devel
BuildRequires:  /usr/bin/glslangValidator

#vkroots deps
BuildRequires:  vulkan-headers

#wlroots deps
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm) >= 17.1.0
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(libinput) >= 1.21.0
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(pixman-1) >= 0.42.0
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xwayland)

# libliftoff hasn't bumped soname, but API/ABI has changed for 0.2.0 release
Requires:       libliftoff%{?_isa} >= %{libliftoff_minver}
Requires:       xorg-x11-server-Xwayland
Recommends:     mesa-dri-drivers
Recommends:     mesa-vulkan-drivers

%description
%{name} is the micro-compositor optimized for running video games on Wayland.

%prep
%setup -a2 -a3 -a4 -q -n %{name}-%{commit}
# Install stub pkgconfig file
mkdir -p pkgconfig
cp %{SOURCE1} pkgconfig/stb.pc

# Replace spirv-headers include with the system directory
sed -i 's^../thirdparty/SPIRV-Headers/include/spirv/^/usr/include/spirv/^' src/meson.build

# Push in reshade from sources instead of submodule
rm -rf src/reshade && mv reshade-%{reshade_commit} src/reshade

# Use vkroots/wlroots from sources instead of submodule
rm -rf subprojects/vkroots && mv vkroots-%{vkroots_commit} subprojects/vkroots
rm -rf subprojects/wlroots && mv wlroots-%{wlroots_commit} subprojects/wlroots

%autopatch -p1

%build
export PKG_CONFIG_PATH=pkgconfig
%meson -Dpipewire=enabled -Denable_openvr_support=false -Dforce_fallback_for=[]
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_bindir}/gamescope
%{_libdir}/libVkLayer_FROG_gamescope_wsi_*.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.*.json

%ghost
/usr/include/vkroots.h
/usr/include/wlr/*
/usr/lib64/libwlroots.a
/usr/lib64/pkgconfig/vkroots.pc
/usr/lib64/pkgconfig/wlroots.pc

%changelog
%autochangelog
