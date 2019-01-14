#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define         module          liblo
%define         pypi_name       pyliblo
Summary:	pyliblo - Python bindings for the liblo OSC library
Name:		python-%{pypi_name}
Version:	0.10.0
Release:	1
License:	LGPL 2.1
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	1be68794dedaf8cc60748fe94fdb9628
URL:		http://das.nasophon.de/pyliblo/
BuildRequires:	liblo-devel >= 0.27
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python bindings for the liblo OSC library.

%package -n python3-%{pypi_name}
Summary:	pyliblo - Python bindings for the liblo OSC library
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}
Python bindings for the liblo OSC library.

%package -n %{pypi_name}-tools
Summary:	OSC tools shipped with pyliblo Python library
Group:		Applications
%if %{with python3}
Requires:	python3-%{pypi_name}
%else
Requires:	python-%{pypi_name}
%endif

%description -n %{pypi_name}-tools
OSC tools shipped with pyliblo Python library.

%package apidocs
Summary:	%{pypi_name} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{pypi_name}
Group:		Documentation

%description apidocs
API documentation for %{pypi_name}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{pypi_name}.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
cd doc
%{__make} -j1 html
rm -rf _build/html/_sources
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
rm -rf $RPM_BUILD_ROOT%{_bindir}/*
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{pypi_name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{pypi_name}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{py_sitedir}/%{module}.so
%{py_sitedir}/%{pypi_name}-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{py3_sitedir}/%{module}.*.so
%{py3_sitedir}/%{pypi_name}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{pypi_name}-%{version}
%endif

%files -n %{pypi_name}-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dump_osc
%attr(755,root,root) %{_bindir}/send_osc
%{_mandir}/man1/dump_osc.1*
%{_mandir}/man1/send_osc.1*

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/*
%endif
