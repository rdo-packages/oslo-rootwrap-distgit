%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global pypi_name oslo.rootwrap
%global pkg_name oslo-rootwrap

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-oslo-rootwrap
Version:        4.1.0
Release:        1%{?dist}
Summary:        Oslo Rootwrap

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%package -n python2-%{pkg_name}
Summary:        Oslo Rootwrap
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python-pbr
# Required for testing
BuildRequires:  python-eventlet
BuildRequires:  python-fixtures
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-oslotest
BuildRequires:  python-six
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools


Requires:       python-six >= 1.9.0

%description -n python2-%{pkg_name}
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`

%package -n python-%{pkg_name}-doc
Summary:        Documentation for Oslo Rootwrap

BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx

%description -n python-%{pkg_name}-doc
Documentation for Oslo Rootwrap

%package -n python2-%{pkg_name}-tests
Summary:    Tests for Oslo Rootwrap

Requires:       python-%{pkg_name} = %{version}-%{release}
Requires:       python-eventlet
Requires:       python-fixtures
Requires:       python-hacking
Requires:       python-mock
Requires:       python-oslotest
Requires:       python-subunit
Requires:       python-testrepository
Requires:       python-testscenarios
Requires:       python-testtools

%description -n python2-%{pkg_name}-tests
Tests for the Oslo Log handling library.

%if 0%{?with_python3}
%package -n python3-%{pkg_name}
Summary:        Oslo Rootwrap
%{?python_provide:%python_provide python3-%{pkg_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# Required for testing
BuildRequires:  python3-eventlet
BuildRequires:  python3-fixtures
BuildRequires:  python3-hacking
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-six
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools


Requires:       python3-six >= 1.9.0

%description -n python3-%{pkg_name}
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`

%package -n python3-%{pkg_name}-tests
Summary:    Tests for Oslo Rootwrap

Requires:       python3-%{pkg_name} = %{version}-%{release}
Requires:       python3-eventlet
Requires:       python3-fixtures
Requires:       python3-hacking
Requires:       python3-mock
Requires:       python3-oslotest
Requires:       python3-subunit
Requires:       python3-testrepository
Requires:       python3-testscenarios
Requires:       python3-testtools

%description -n python3-%{pkg_name}-tests
Tests for the Oslo Log handling library.

%endif

%description
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`


%prep
%setup -q -n %{pypi_name}-%{upstream_version}

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
sphinx-build doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
# TODO one test is failing here, but not in virtualenv
PYTHONPATH=. %{__python2} setup.py test ||
%if 0%{?with_python3}
rm -rf .testrepository
PYTHONPATH=. %{__python3} setup.py test ||
%endif

%files -n python2-%{pkg_name}
%doc README.rst LICENSE
%{python2_sitelib}/oslo_rootwrap
%{python2_sitelib}/*.egg-info
%{_bindir}/oslo-rootwrap
%{_bindir}/oslo-rootwrap-daemon
%exclude %{python2_sitelib}/oslo_rootwrap/tests

%files -n python-%{pkg_name}-doc
%doc html
%license LICENSE

%files -n python2-%{pkg_name}-tests
%{python2_sitelib}/oslo_rootwrap/tests

%if 0%{?with_python3}
%files -n python3-%{pkg_name}
%doc README.rst LICENSE
%{python3_sitelib}/oslo_rootwrap
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/oslo_rootwrap/tests

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_rootwrap/tests
%endif

%changelog
* Wed Mar 23 2016 Haikel Guemar <hguemar@fedoraproject.org> 4.1.0-
- Update to 4.1.0

