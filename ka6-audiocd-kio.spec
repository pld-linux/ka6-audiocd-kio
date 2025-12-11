#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		audiocd-kio
Summary:	Audio CD kio
Name:		ka6-%{kaname}
Version:	25.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	a5cb8d3683f7db5cdbdf38bea304b701
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cdparanoia-III-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-libkcddb-devel >= %{kdeappsver}
BuildRequires:	ka6-libkcompactdisc-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kioslave for accessing audio CDs.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%ghost %{_libdir}/libaudiocdplugins.so.5
%{_libdir}/libaudiocdplugins.so.*.*
%{_libdir}/qt6/plugins/kf6/kio/audiocd.so
%{_libdir}/qt6/plugins/libaudiocd_encoder_flac.so
%{_libdir}/qt6/plugins/libaudiocd_encoder_lame.so
%{_libdir}/qt6/plugins/libaudiocd_encoder_opus.so
%{_libdir}/qt6/plugins/libaudiocd_encoder_vorbis.so
%{_libdir}/qt6/plugins/libaudiocd_encoder_wav.so
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings_qwidgets/kcm_audiocd.so
%{_desktopdir}/kcm_audiocd.desktop
%{_datadir}/config.kcfg/audiocd_flac_encoder.kcfg
%{_datadir}/config.kcfg/audiocd_lame_encoder.kcfg
%{_datadir}/config.kcfg/audiocd_opus_encoder.kcfg
%{_datadir}/config.kcfg/audiocd_vorbis_encoder.kcfg
%{_datadir}/konqsidebartng/virtual_folders/services/audiocd.desktop
%{_datadir}/metainfo/org.kde.kio_audiocd.metainfo.xml
%{_datadir}/qlogging-categories6/kio_audiocd.categories
%{_datadir}/qlogging-categories6/kio_audiocd.renamecategories
%{_datadir}/solid/actions/solid_audiocd.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/audiocdplugins
%{_libdir}/libaudiocdplugins.so
