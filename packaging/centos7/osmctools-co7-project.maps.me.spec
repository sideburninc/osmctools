%define project %(echo $PROJECT)
%define name %{project}
%define version %(echo $VERSION)
%define project_repo %(echo $REPO_URL)/%{project}.git
%define release %(echo $RELEASE)
%define project_root %{_builddir}/%{name}-%{version}

Name:      %{name}
Summary:   This package contains osm tools: osmupdate, osmfilter, osmconvert.
Version:   %{version}
Release:   %{release}
License:   Propritetary
Url:       http://github.com/mapsme/%{project}
Buildroot: %{_tmppath}/%{name}-%{version}-%(%{__id_u} -n)
Source:    %{name}-%{version}.tar.gz
BuildRequires: devtoolset-7-gcc-c++
BuildRequires: git
BuildRequires: zlib-devel

%description
%{name} are osm tools.

%prep
rm -rf %{project_root} 2> /dev/null
rm -rf %{project_root}.repo 2> /dev/null
git clone -b %{version} --depth 1 --recurse-submodules %{project_repo} %{project_root}.repo
# Pack source to save it in src rpm.
mkdir -p %{project_root}
mv %{project_root}.repo/* %{project_root}
rm -rm %{project_root}.repo
rm -rf %{project_root}/.git
%{__tar} czf %{S:0} %{name}-%{version}
%setup -T -D

%build
mkdir -p %{project_root}/build
cd %{project_root}/build
source /opt/rh/devtoolset-7/enable
cmake3 ..
make %{?_smp_mflags}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
cp -Rp %{_builddir}/%{name}-%{version}/build/osmupdate %{buildroot}/%{_bindir}
cp -Rp %{_builddir}/%{name}-%{version}/build/osmfilter %{buildroot}/%{_bindir}
cp -Rp %{_builddir}/%{name}-%{version}/build/osmconvert %{buildroot}/%{_bindir}

%files
%defattr(-,root,root,-)
%{_bindir}/*

%changelog
* Thu Jul 22 2020 Maksim Andrianov <m.andrianov@corp.mail.ru>
- Initial build
