%global debug_package %{nil}
%global commit 5106d8a0df95de66cc58dc1ea37e69c99afc9540
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20240429

Name:           vkroots
Version:        0^%{git_date}git%{shortcommit}
Release:        %autorelease
Summary:        A stupid simple method of making Vulkan layers, at home
License:        LGPL-2.1-or-later AND (Apache-2.0 or MIT)
URL:            https://github.com/Joshua-Ashton/vkroots
Source:         %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  vulkan-headers


%description
vkroots is a framework for writing Vulkan layers that
takes all the complexity/hastle away from you. It's so simple.


%package devel
Summary:        A stupid simple method of making Vulkan layers, at home

%description devel
vkroots is a framework for writing Vulkan layers that
takes all the complexity/hastle away from you. It's so simple.

%prep
%autosetup -p1 -n %{name}-%{commit}


%build
%meson
%meson_build


%install
%meson_install


%files devel
%license LICENSE
%doc README.md
%{_includedir}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc


%changelog
%autochangelog
