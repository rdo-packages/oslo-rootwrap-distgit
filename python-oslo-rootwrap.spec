%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
%global pypi_name oslo.rootwrap
%global pkg_name oslo-rootwrap

Name:           python-oslo-rootwrap
Version:        XXX
Release:        XXX
Summary:        Oslo Rootwrap

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%package -n python3-%{pkg_name}
Summary:        Oslo Rootwrap
%{?python_provide:%python_provide python3-%{pkg_name}}
Obsoletes: python2-%{pkg_name} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  git-core
# Required for testing
BuildRequires:  iproute
BuildRequires:  python3-eventlet
BuildRequires:  python3-fixtures
BuildRequires:  python3-hacking
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-six
BuildRequires:  python3-stestr
BuildRequires:  python3-subunit
BuildRequires:  python3-testtools
BuildRequires:  python3-testscenarios



%description -n python3-%{pkg_name}
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:        Documentation for Oslo Rootwrap

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme

%description -n python-%{pkg_name}-doc
Documentation for Oslo Rootwrap
%endif

%package -n python3-%{pkg_name}-tests
Summary:    Tests for Oslo Rootwrap

Requires:       python3-%{pkg_name} = %{version}-%{release}
Requires:       python3-eventlet
Requires:       python3-fixtures
Requires:       python3-hacking
Requires:       python3-mock
Requires:       python3-oslotest
Requires:       python3-subunit
Requires:       python3-stestr
Requires:       python3-testtools
Requires:       python3-testscenarios

%description -n python3-%{pkg_name}-tests
Tests for the Oslo Log handling library.

%description
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%build
%{py3_build}

%if 0%{?with_doc}
# generate html docs
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{py3_install}

%check
#export PYTHON_DISALLOW_AMBIGUOUS_VERSION=0
export PYTHONPATH=.
export OS_TEST_PATH="./oslo_rootwrap/tests"
PYTHON=python3 stestr-3 --test-path $OS_TEST_PATH run

%files -n python3-%{pkg_name}
%doc README.rst LICENSE
%{python3_sitelib}/oslo_rootwrap
%{python3_sitelib}/*.egg-info
%{_bindir}/oslo-rootwrap
%{_bindir}/oslo-rootwrap-daemon
%exclude %{python3_sitelib}/oslo_rootwrap/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_rootwrap/tests

%changelog
