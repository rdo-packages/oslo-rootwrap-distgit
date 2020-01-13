# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
%global pypi_name oslo.rootwrap
%global pkg_name oslo-rootwrap

Name:           python-oslo-rootwrap
Version:        5.15.3
Release:        1%{?dist}
Summary:        Oslo Rootwrap

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%package -n python%{pyver}-%{pkg_name}
Summary:        Oslo Rootwrap
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}
%if %{pyver} == 3
Obsoletes: python2-%{pkg_name} < %{version}-%{release}
%endif

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  git
# Required for testing
BuildRequires:  iproute
BuildRequires:  python%{pyver}-eventlet
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-testscenarios


Requires:       python%{pyver}-six >= 1.10.0

%description -n python%{pyver}-%{pkg_name}
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:        Documentation for Oslo Rootwrap

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{pkg_name}-doc
Documentation for Oslo Rootwrap
%endif

%package -n python%{pyver}-%{pkg_name}-tests
Summary:    Tests for Oslo Rootwrap

Requires:       python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires:       python%{pyver}-eventlet
Requires:       python%{pyver}-fixtures
Requires:       python%{pyver}-hacking
Requires:       python%{pyver}-mock
Requires:       python%{pyver}-oslotest
Requires:       python%{pyver}-subunit
Requires:       python%{pyver}-stestr
Requires:       python%{pyver}-testtools
Requires:       python%{pyver}-testscenarios

%description -n python%{pyver}-%{pkg_name}-tests
Tests for the Oslo Log handling library.

%description
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
#export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0
export PYTHONPATH=.
export OS_TEST_PATH="./oslo_rootwrap/tests"
stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{pkg_name}
%doc README.rst LICENSE
%{pyver_sitelib}/oslo_rootwrap
%{pyver_sitelib}/*.egg-info
%{_bindir}/oslo-rootwrap
%{_bindir}/oslo-rootwrap-daemon
%exclude %{pyver_sitelib}/oslo_rootwrap/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_rootwrap/tests

%changelog
* Mon Jan 13 2020 RDO <dev@lists.rdoproject.org> 5.15.3-1
- Update to 5.15.3

* Tue Mar 12 2019 RDO <dev@lists.rdoproject.org> 5.15.2-1
- Update to 5.15.2

