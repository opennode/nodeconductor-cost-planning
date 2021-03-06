Name: waldur-cost-planning
Summary: Waldur cost planning plugin
Group: Development/Libraries
Version: 0.6.2
Release: 1.el7
License: MIT
Url: http://waldur.com
Source0: %{name}-%{version}.tar.gz

Requires: waldur-core >= 0.151.1
Requires: waldur-openstack >= 0.38.2
Requires: waldur-digitalocean >= 0.10.2
Requires: waldur-aws >= 0.11.2
Requires: waldur-azure >= 0.3.4

Obsoletes: nodeconductor-cost-planning

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: python-setuptools

%description
Waldur cost planning plugin allows to get a price estimate without actually creating the infrastructure.

%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
* Mon May 14 2018 Jenkins <jenkins@opennodecloud.com> - 0.6.2-1.el7
- New upstream release

* Sat Jan 13 2018 Jenkins <jenkins@opennodecloud.com> - 0.6.1-1.el7
- New upstream release

* Fri Dec 22 2017 Jenkins <jenkins@opennodecloud.com> - 0.6.0-1.el7
- New upstream release

* Fri Dec 1 2017 Jenkins <jenkins@opennodecloud.com> - 0.5.6-1.el7
- New upstream release

* Wed Nov 29 2017 Jenkins <jenkins@opennodecloud.com> - 0.5.5-1.el7
- New upstream release

* Mon Nov 20 2017 Jenkins <jenkins@opennodecloud.com> - 0.5.4-1.el7
- New upstream release

* Fri Nov 17 2017 Jenkins <jenkins@opennodecloud.com> - 0.5.3-1.el7
- New upstream release

* Thu Nov 16 2017 Jenkins <jenkins@opennodecloud.com> - 0.5.2-1.el7
- New upstream release

* Sun Sep 17 2017 Jenkins <jenkins@opennodecloud.com> - 0.5.1-1.el7
- New upstream release

* Sat Sep 16 2017 Jenkins <jenkins@opennodecloud.com> - 0.5.0-1.el7
- New upstream release

* Mon Jul 3 2017 Jenkins <jenkins@opennodecloud.com> - 0.4.2-1.el7
- New upstream release
