%global package_speccommit 525b160e0537cadf8032b68622d1f6962d518feb
%global usver 5.10.214
%global xsver 3
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 5.10.214
%define vendor_name Intel
%define vendor_label intel
%define driver_name igc

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Version: 5.10.214
Release: %{?xsrel}.1%{?dist}
License: GPL
Source0: intel-igc.tar.gz
Patch0: 0001-Change-makefile-for-building-igc.patch
Patch1: 0002-Some-backports-from-higher-kernel-version.patch
Patch2: 0003-gettimex64-is-not-supported-until-kernel-v5.0.patch
Patch3: 0004-supported_coalesce_params-is-not-supported-until-ker.patch
Patch4: 0005-TAPRIO-was-not-supported-until-kernel-v5.18.patch

# XCP-ng specific patches
Patch1000: 1000-showversion.patch
Patch1001: 1001-i226.patch

BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

# This RPM obsoletes XCP-ng specific RPM igc-module
Obsoletes: igc-module < 5.10.200-2

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%{?_cov_results_package}

%changelog
* Thu Jun 20 2024 Thierry Escande <thierry.escande@vates.tech> - 5.10.214-3.1
- Obsoletes igc-module RPM
- Import XCP-ng specific patches from obsolete igc-module RPM

* Mon May 06 2024 Stephen Cheng <stephen.cheng@cloud.com> - Version: 5.10.214-3
- CP-48894: Modify checksum
- The checksum was wrongly grenerated in the previous commit due to xenpkg upgrade

* Mon May 06 2024 Stephen Cheng <stephen.cheng@cloud.com> - Version: 5.10.214-2
- CP-48894: Add checksum

* Thu Apr 11 2024 Stephen Cheng <stephen.cheng@cloud.com> - Version: 5.10.214-1
- CP-48894: Build igc driver based on source code from kernel 5.10.214
