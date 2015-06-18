%global pypi_name oslo.rootwrap

Name:           python-oslo-rootwrap
Version:        1.6.0
Release:        2%{?dist}
Summary:        Oslo Rootwrap

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://pypi.python.org/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
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
%setup -q -n %{pypi_name}-%{version}


%build
%{__python2} setup.py build


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

#%check
#%{__python} setup.py test

%files
%license LICENSE
%doc README.rst
%{python2_sitelib}/oslo
%{python2_sitelib}/oslo_rootwrap
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/*-nspkg.pth

%changelog
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Alan Pevec <apevec@redhat.com> - 1.6.0-1
- new version

* Sun Sep 21 2014 Alan Pevec <apevec@redhat.com> - 1.3.0.0-1
- Final release 1.3.0

* Fri Sep 12 2014 Alan Pevec <apevec@redhat.com> - 1.3.0.0-0.1.a2
- Update to 1.3.0.0a2 milestone

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Matthias Runge <mrunge@redhat.com> - 1.0.0-1
- Initial package.
