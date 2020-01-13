%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%if 0%{?fedora} >= 24
%global with_python3 1
%endif
%global with_doc 1
%global pypi_name oslo.rootwrap
%global pkg_name oslo-rootwrap

Name:           python-oslo-rootwrap
Version:        5.14.2
Release:        1%{?dist}
Summary:        Oslo Rootwrap

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%package -n python2-%{pkg_name}
Summary:        Oslo Rootwrap
%{?python_provide:%python_provide python2-%{pkg_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  git
# Required for testing
BuildRequires:  iproute
BuildRequires:  python2-eventlet
BuildRequires:  python2-fixtures
BuildRequires:  python2-hacking
BuildRequires:  python2-mock
BuildRequires:  python2-oslotest
BuildRequires:  python2-six
BuildRequires:  python2-stestr
BuildRequires:  python2-subunit
BuildRequires:  python2-testtools
%if 0%{?fedora} > 0
BuildRequires:  python2-testrepository
BuildRequires:  python2-testscenarios
%else
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
%endif


Requires:       python2-six >= 1.10.0

%description -n python2-%{pkg_name}
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:        Documentation for Oslo Rootwrap

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme

%description -n python-%{pkg_name}-doc
Documentation for Oslo Rootwrap
%endif

%package -n python2-%{pkg_name}-tests
Summary:    Tests for Oslo Rootwrap

Requires:       python2-%{pkg_name} = %{version}-%{release}
Requires:       python2-eventlet
Requires:       python2-fixtures
Requires:       python2-hacking
Requires:       python2-mock
Requires:       python2-oslotest
Requires:       python2-subunit
Requires:       python2-stestr
Requires:       python2-testtools
%if 0%{?fedora} > 0
Requires:       python2-testrepository
Requires:       python2-testscenarios
%else
Requires:       python-testrepository
Requires:       python-testscenarios
%endif

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
BuildRequires:  python3-stestr
BuildRequires:  python3-subunit
BuildRequires:  python3-testrepository
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools


Requires:       python3-six >= 1.10.0

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
Requires:       python3-stestr
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
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%py2_install

%check
#export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0
export PYTHONPATH=.
export OS_TEST_PATH="./oslo_rootwrap/tests"
%if 0%{?with_python3}
stestr-3 --test-path $OS_TEST_PATH run
%endif
stestr --test-path $OS_TEST_PATH run

%files -n python2-%{pkg_name}
%doc README.rst LICENSE
%{python2_sitelib}/oslo_rootwrap
%{python2_sitelib}/*.egg-info
%{_bindir}/oslo-rootwrap
%{_bindir}/oslo-rootwrap-daemon
%exclude %{python2_sitelib}/oslo_rootwrap/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

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
* Mon Jan 13 2020 RDO <dev@lists.rdoproject.org> 5.14.2-1
- Update to 5.14.2

* Thu Aug 02 2018 RDO <dev@lists.rdoproject.org> 5.14.1-1
- Update to 5.14.1

