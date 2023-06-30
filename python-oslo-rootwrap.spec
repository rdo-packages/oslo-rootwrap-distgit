%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global with_doc 1
%global pypi_name oslo.rootwrap
%global pkg_name oslo-rootwrap

Name:           python-oslo-rootwrap
Version:        XXX
Release:        XXX
Summary:        Oslo Rootwrap

License:        Apache-2.0
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
Obsoletes: python2-%{pkg_name} < %{version}-%{release}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
BuildRequires:  iproute


%description -n python3-%{pkg_name}
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:        Documentation for Oslo Rootwrap

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

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
export OS_TEST_PATH="./oslo_rootwrap/tests"
%tox -e %{default_toxenv}

%files -n python3-%{pkg_name}
%doc README.rst LICENSE
%{python3_sitelib}/oslo_rootwrap
%{python3_sitelib}/*.dist-info
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
