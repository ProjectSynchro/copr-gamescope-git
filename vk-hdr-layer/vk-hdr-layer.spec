%global commit f5f13b7ae44135a4d79a60bd4cd4efe7e1534ba6
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           vk-hdr-layer
Version:        1.0.0
Release:        %autorelease
Summary:        Vulkan layer utilizing a small color management / HDR protocol for experimentation
License:        MIT
URL:            https://github.com/Zamundaaa/VK_hdr_layer
Source0:        %{url}/archive/%{commit}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(vkroots)

%description
Vulkan layer utilizing a small color management / HDR protocol for experimentation

%prep
%autosetup -n VK_hdr_layer-%{commit}

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_datadir}/vulkan/implicit_layer.d/*
%{_libdir}/*.so
