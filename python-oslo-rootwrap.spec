%global pypi_name oslo.rootwrap
%global milestone a2

Name:           python-oslo-rootwrap
Version:        1.3.0.0
Release:        0.1.%{milestone}%{?dist}
Summary:        Oslo Rootwrap

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}%{milestone}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr


%description
The Oslo Rootwrap allows fine filtering of shell commands to run as `root`
from OpenStack services.

Unlike other Oslo deliverables, it should **not** be used as a Python library,
but called as a separate process through the `oslo-rootwrap` command:

`sudo oslo-rootwrap ROOTWRAP_CONFIG COMMAND_LINE`

%prep
%setup -q -n %{pypi_name}-%{version}%{milestone}

sed -i 's/%{version}%{milestone}/%{version}/' PKG-INFO

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info



%build
%{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot}

#%check
#%{__python} setup.py test

%files
%doc README.rst LICENSE
%dir %{python_sitelib}/oslo
%{python_sitelib}/oslo/rootwrap
%{python_sitelib}/oslo.rootwrap-%{version}*

%changelog
* Fri Sep 12 2014 Alan Pevec <apevec@redhat.com> - 1.3.0.0-0.1.a2
- Update to 1.3.0.0a2 milestone

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Matthias Runge <mrunge@redhat.com> - 1.0.0-1
- Initial package.
