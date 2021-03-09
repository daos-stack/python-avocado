%global srcname avocado
%global pkgname avocado

# Conditional for release vs. snapshot builds. Set to 1 for release build.
%if ! 0%{?rel_build:1}
    %global rel_build 1
%endif

# Settings used for build from snapshots.
%if 0%{?rel_build}
    %global gitref          %{version}
    %global gittar          %{srcname}-%{version}.tar.gz
%else
    %if ! 0%{?commit:1}
        %global commit      489fee786c7b69cf0fa12f75be0595cb8bae5887
    %endif
    %if ! 0%{?commit_date:1}
        %global commit_date 20190917
    %endif
    %global shortcommit     %(c=%{commit};echo ${c:0:8})
    %global gitrel          .%{commit_date}git%{shortcommit}
    %global gitref          %{commit}
    %global gittar          %{srcname}-%{shortcommit}.tar.gz
%endif

# Selftests are provided but may need to be skipped because many of
# the functional tests are time and resource sensitive and can
# cause race conditions and random build failures. They are
# enabled by default.
# However, selftests need to be disabled when libvirt is not available.
%global with_tests 1
%if 0%{?rhel} && 0%{?rhel} <= 7
    # libvirt is not available for all RHEL builder architectures
    %global with_tests 0
%endif

%if 0%{?fedora} > 30 || 0%{?rhel} > 7
    %bcond_with    python2
%else
    %bcond_without python2
%endif
%if 0%{?fedora} || 0%{?rhel} > 6
    %bcond_without python3
%else
    %bcond_with    python3
%endif

# Avocado is currently incompatible with the Fabric API in Fedora 31 and later
# https://github.com/avocado-framework/avocado/issues/3125
%if 0%{?fedora} >= 31
%global with_fabric 0
%else
%global with_fabric 1
%endif

# Python 3 version of Fabric package is new starting with Fedora 29
%if %{with python3} && 0%{?fedora} >= 29
%global with_python3_fabric 1
%else
%global with_python3_fabric 0
%endif

# Python2 binary packages are being removed
# See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
# python2-resultsdb_api package has been removed in F30
%if %{with python2} && ( (0%{?fedora} && 0%{?fedora} <= 29) || (0%{?rhel} && 0%{?rhel} <= 7) )
%global with_python2_resultsdb 1
%else
%global with_python2_resultsdb 0
%endif

Name: python-%{pkgname}
Version: 69.2
Release: 1.01%{?gitrel}%{?dist}
Summary: Framework with tools and libraries for Automated Testing
Group: Development/Tools
# Found licenses:
# avocado/utils/external/gdbmi_parser.py: MIT
# avocado/utils/external/spark.py: MIT
# Other files: GPLv2 and GPLv2+
License: GPLv2 and MIT
URL: http://avocado-framework.github.io/
Source0: https://github.com/avocado-framework/%{srcname}/archive/%{gitref}.tar.gz#/%{gittar}
Patch0: avocado-69.1-selftest.patch
BuildArch: noarch

BuildRequires: procps-ng
BuildRequires: kmod

%if %{with python2}
BuildRequires: python2-aexpect
BuildRequires: python2-devel
BuildRequires: python2-docutils
BuildRequires: python2-mock
BuildRequires: python2-psutil
BuildRequires: python2-requests
BuildRequires: python2-setuptools
BuildRequires: python2-six
%if 0%{?fedora} && 0%{?fedora} <= 30
# python2-sphinx is no longer available or needed as of F31
BuildRequires: python2-sphinx
%endif
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
BuildRequires: python2-jinja2
%else
BuildRequires: python-jinja2
%endif
%if %{with_fabric}
%if 0%{?fedora} >= 29
BuildRequires: python2-fabric3
%else
BuildRequires: fabric
%endif
%endif
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires: python2-enum34
BuildRequires: python2-lxml
BuildRequires: python2-stevedore
%else
BuildRequires: python-enum34
BuildRequires: python-lxml
BuildRequires: python-stevedore
%endif
%if 0%{?fedora} && 0%{?fedora} <= 29
# Python2 binary packages are being removed
# See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
BuildRequires: python2-pycdlib
%endif
%if %{with_python2_resultsdb}
BuildRequires: python2-resultsdb_api
%endif
%endif

%if 0%{?rhel} == 7
%global pypref 36
%else
%global pypref 3
%endif
%if %{with python3}
%if 0%{?rhel} == 0
BuildRequires: python3-aexpect
BuildRequires: python3-pycdlib
BuildRequires: python3-resultsdb_api
BuildRequires: python3-stevedore
%endif
BuildRequires: python%{pypref}-devel
BuildRequires: python%{pypref}-docutils
BuildRequires: python%{pypref}-jinja2
BuildRequires: python%{pypref}-lxml
BuildRequires: python%{pypref}-mock
BuildRequires: python%{pypref}-psutil
BuildRequires: python%{pypref}-requests
BuildRequires: python%{pypref}-setuptools
BuildRequires: python%{pypref}-six
BuildRequires: python%{pypref}-sphinx
%if %{with_fabric}
%if %{with_python3_fabric}
BuildRequires: python3-fabric3
%endif
%endif
%endif

%if 0%{?with_tests}
BuildRequires: genisoimage
BuildRequires: libcdio
BuildRequires: perl-Test-Harness
BuildRequires: psmisc
%if 0%{?fedora} >= 30 || 0%{?rhel} > 7
BuildRequires: glibc-all-langpacks
%endif
%if %{with python2}
%if 0%{?fedora} >= 27 || 0%{?rhel} > 7
BuildRequires: python2-libvirt
BuildRequires: python2-netifaces
BuildRequires: python2-yaml
%else
BuildRequires: libvirt-python
BuildRequires: python-netifaces
BuildRequires: python-yaml
%endif
%endif
%if %{with python3}
BuildRequires: python3-netifaces
BuildRequires: python3-yaml
%if 0%{?fedora} >= 27 || 0%{?rhel} > 7
BuildRequires: python3-libvirt
%else
BuildRequires: libvirt-python3
%endif
%endif
%endif

%description
Avocado is a set of tools and libraries (what people call
these days a framework) to perform automated testing.


%prep
%setup -q -n %{srcname}-%{gitref}
%patch0 -p1
# package plugins-runner-vm requires libvirt-python, but the RPM
# version of libvirt-python does not publish the egg info and this
# causes that dep to be attempted to be installed by pip
sed -e "s/'libvirt-python'//" -i optional_plugins/runner_vm/setup.py
%if 0%{?rhel} && 0%{?rhel} <= 7
sed -e "s/'six>=1.10.0'/'six>=1.9.0'/" -i setup.py
sed -e "s/'PyYAML>=4.2b2'/'PyYAML>=3.10'/" -i optional_plugins/varianter_yaml_to_mux/setup.py
%endif
%if 0%{?fedora} && 0%{?fedora} < 29
sed -e "s/'PyYAML>=4.2b2'/'PyYAML>=3.12'/" -i optional_plugins/varianter_yaml_to_mux/setup.py
%endif

%build
%if %{with python2}
%py2_build
%endif
%if %{with python3}
%py3_build
%endif
pushd optional_plugins/html
    %if %{with python2}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
pushd optional_plugins/runner_remote
%if %{with_fabric}
    %if %{with python2}
    %py2_build
    %endif
    %if %{with_python3_fabric}
    %py3_build
    %endif
%endif
popd
pushd optional_plugins/runner_vm
%if %{with_fabric}
    %if %{with python2}
    %py2_build
    %endif
    %if %{with_python3_fabric}
    %py3_build
    %endif
%endif
popd
pushd optional_plugins/runner_docker
%if %{with_fabric}
    %if %{with python2}
    %py2_build
    %endif
    %if %{with_python3_fabric}
    %py3_build
    %endif
%endif
popd
pushd optional_plugins/resultsdb
    %if %{with_python2_resultsdb}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
pushd optional_plugins/varianter_yaml_to_mux
    %if %{with python2}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
pushd optional_plugins/loader_yaml
    %if %{with python2}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
pushd optional_plugins/golang
    %if %{with python2}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
pushd optional_plugins/varianter_pict
    %if %{with python2}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
pushd optional_plugins/varianter_cit
    %if %{with python2}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
pushd optional_plugins/result_upload
    %if %{with python2}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
pushd optional_plugins/glib
    %if %{with python2}
    %py2_build
    %endif
    %if %{with python3}
    %py3_build
    %endif
popd
%{__make} man

%install
%if %{with python2}
%py2_install
%{__mv} %{buildroot}%{_bindir}/avocado %{buildroot}%{_bindir}/avocado-%{python2_version}
%{__ln_s} avocado-%{python2_version} %{buildroot}%{_bindir}/avocado-2
%{__mv} %{buildroot}%{_bindir}/avocado-rest-client %{buildroot}%{_bindir}/avocado-rest-client-%{python2_version}
%{__ln_s} avocado-rest-client-%{python2_version} %{buildroot}%{_bindir}/avocado-rest-client-2
# configuration is held at /etc/avocado only and part of the
# python-avocado-common package
%{__rm} -rf %{buildroot}%{python2_sitelib}/avocado/etc
# ditto for libexec files
%{__rm} -rf %{buildroot}%{python2_sitelib}/avocado/libexec
%endif
%if %{with python3}
%py3_install
%{__mv} %{buildroot}%{_bindir}/avocado %{buildroot}%{_bindir}/avocado-%{python3_version}
%{__ln_s} avocado-%{python3_version} %{buildroot}%{_bindir}/avocado-3
%{__mv} %{buildroot}%{_bindir}/avocado-rest-client %{buildroot}%{_bindir}/avocado-rest-client-%{python3_version}
%{__ln_s} avocado-rest-client-%{python3_version} %{buildroot}%{_bindir}/avocado-rest-client-3
# configuration is held at /etc/avocado only and part of the
# python-avocado-common package
%{__rm} -rf %{buildroot}%{python3_sitelib}/avocado/etc
# ditto for libexec files
%{__rm} -rf %{buildroot}%{python3_sitelib}/avocado/libexec
%endif
%if %{with python3}
# Unversioned executables should now be the Python 3 version if shipping with Python 3
#   https://docs.fedoraproject.org/en-US/packaging-guidelines/Python_Appendix/
%{__ln_s} avocado-%{python3_version} %{buildroot}%{_bindir}/avocado
%{__ln_s} avocado-rest-client-%{python3_version} %{buildroot}%{_bindir}/avocado-rest-client
%else
%{__ln_s} avocado-%{python2_version} %{buildroot}%{_bindir}/avocado
%{__ln_s} avocado-rest-client-%{python2_version} %{buildroot}%{_bindir}/avocado-rest-client
%endif
pushd optional_plugins/html
    %if %{with python2}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
pushd optional_plugins/runner_remote
%if %{with_fabric}
    %if %{with python2}
    %py2_install
    %endif
    %if %{with_python3_fabric}
    %py3_install
    %endif
%endif
popd
pushd optional_plugins/runner_vm
%if %{with_fabric}
    %if %{with python2}
    %py2_install
    %endif
    %if %{with_python3_fabric}
    %py3_install
    %endif
%endif
popd
pushd optional_plugins/runner_docker
%if %{with_fabric}
    %if %{with python2}
    %py2_install
    %endif
    %if %{with_python3_fabric}
    %py3_install
    %endif
%endif
popd
pushd optional_plugins/resultsdb
    %if %{with_python2_resultsdb}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
pushd optional_plugins/varianter_yaml_to_mux
    %if %{with python2}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
pushd optional_plugins/loader_yaml
    %if %{with python2}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
pushd optional_plugins/golang
    %if %{with python2}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
pushd optional_plugins/varianter_pict
    %if %{with python2}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
pushd optional_plugins/varianter_cit
    %if %{with python2}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
pushd optional_plugins/result_upload
    %if %{with python2}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
pushd optional_plugins/glib
    %if %{with python2}
    %py2_install
    %endif
    %if %{with python3}
    %py3_install
    %endif
popd
# cleanup plugin test cruft
%if %{with python2}
%{__rm} -rf %{buildroot}%{python2_sitelib}/tests
%endif
%if %{with python3}
%{__rm} -rf %{buildroot}%{python3_sitelib}/tests
%endif
%{__mkdir} -p %{buildroot}%{_sysconfdir}/avocado
%{__cp} avocado/etc/avocado/avocado.conf %{buildroot}%{_sysconfdir}/avocado/avocado.conf
%{__cp} -r avocado/etc/avocado/conf.d %{buildroot}%{_sysconfdir}/avocado/conf.d
%{__cp} -r avocado/etc/avocado/scripts %{buildroot}%{_sysconfdir}/avocado/scripts
%{__cp} -r avocado/etc/avocado/sysinfo %{buildroot}%{_sysconfdir}/avocado/sysinfo
%{__mkdir} -p %{buildroot}%{_libexecdir}/avocado
%{__cp} avocado/libexec/avocado-bash-utils %{buildroot}%{_libexecdir}/avocado/avocado-bash-utils
%{__cp} avocado/libexec/avocado_debug %{buildroot}%{_libexecdir}/avocado/avocado_debug
%{__cp} avocado/libexec/avocado_error %{buildroot}%{_libexecdir}/avocado/avocado_error
%{__cp} avocado/libexec/avocado_info %{buildroot}%{_libexecdir}/avocado/avocado_info
%{__cp} avocado/libexec/avocado_warn %{buildroot}%{_libexecdir}/avocado/avocado_warn
%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__install} -m 0644 man/avocado.1 %{buildroot}%{_mandir}/man1/avocado.1
%{__install} -m 0644 man/avocado-rest-client.1 %{buildroot}%{_mandir}/man1/avocado-rest-client.1
%{__install} -d -m 0755 %{buildroot}%{_sharedstatedir}/avocado/data
# place examples in documentation directory
%{__install} -d -m 0755 %{buildroot}%{_docdir}/avocado
%{__cp} -r examples/gdb-prerun-scripts %{buildroot}%{_docdir}/avocado/gdb-prerun-scripts
%{__cp} -r examples/plugins %{buildroot}%{_docdir}/avocado/plugins
%{__cp} -r examples/tests %{buildroot}%{_docdir}/avocado/tests
%{__cp} -r examples/varianter_cit %{buildroot}%{_docdir}/avocado/varianter_cit
%{__cp} -r examples/varianter_pict %{buildroot}%{_docdir}/avocado/varianter_pict
%{__cp} -r examples/wrappers %{buildroot}%{_docdir}/avocado/wrappers
%{__cp} -r examples/yaml_to_mux %{buildroot}%{_docdir}/avocado/yaml_to_mux
%{__cp} -r examples/yaml_to_mux_loader %{buildroot}%{_docdir}/avocado/yaml_to_mux_loader
find %{buildroot}%{_docdir}/avocado -type f -name '*.py' -exec %{__chmod} -c -x {} ';'


%check
%if 0%{?with_tests}
    %if %{with python2}
    %{__python2} setup.py develop --user
    pushd optional_plugins/html
        %{__python2} setup.py develop --user
    popd
    %if %{with_fabric}
    pushd optional_plugins/runner_remote
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/runner_vm
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/runner_docker
        %{__python2} setup.py develop --user
    popd
    %endif
    %if %{with_python2_resultsdb}
    pushd optional_plugins/resultsdb
        %{__python2} setup.py develop --user
    popd
    %endif
    pushd optional_plugins/varianter_yaml_to_mux
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/loader_yaml
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/golang
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/varianter_pict
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/varianter_cit
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/result_upload
        %{__python2} setup.py develop --user
    popd
    pushd optional_plugins/glib
        %{__python2} setup.py develop --user
    popd
    # LANG: to make the results predictable, we pin the language
    # that is used during test execution.
    # AVOCADO_CHECK_LEVEL: package build environments have the least
    # amount of resources we have observed so far. Let's avoid tests that
    # require too much resources or are time sensitive
    # UNITTEST_AVOCADO_CMD: the "avocado" command to be run during
    # unittests needs to be a Python specific one on Fedora >= 28. Let's
    # use the one that was setup in the source tree by the "setup.py
    # develop --user" step and is guaranteed to be version specific.
    USER_BASE=`%{__python2} -m site --user-base`
    LANG=en_US.UTF-8 AVOCADO_CHECK_LEVEL=0 UNITTEST_AVOCADO_CMD=$USER_BASE/bin/avocado %{__python2} selftests/run
    %endif

    %if %{with python3}
    %{__python3} setup.py develop --user
    pushd optional_plugins/html
        %{__python3} setup.py develop --user
    popd
    %if %{with_fabric}
    %if %{with_python3_fabric}
    pushd optional_plugins/runner_remote
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/runner_vm
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/runner_docker
        %{__python3} setup.py develop --user
    popd
    %endif
    %endif
    pushd optional_plugins/resultsdb
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/varianter_yaml_to_mux
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/loader_yaml
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/golang
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/varianter_pict
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/varianter_cit
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/result_upload
        %{__python3} setup.py develop --user
    popd
    pushd optional_plugins/glib
        %{__python3} setup.py develop --user
    popd
    USER_BASE=`%{__python3} -m site --user-base`
    LANG=en_US.UTF-8 AVOCADO_CHECK_LEVEL=0 UNITTEST_AVOCADO_CMD=$USER_BASE/bin/avocado %{__python3} selftests/run
    %endif
%endif


%if %{with python2}
%package -n python2-%{pkgname}
Summary: %{summary}
License: GPLv2 and MIT
%{?python_provide:%python_provide python2-%{pkgname}}
Requires: python-%{pkgname}-common == %{version}-%{release}
Requires: gdb
Requires: gdb-gdbserver
Requires: procps-ng
Requires: python2
Requires: python2-requests
Requires: python2-setuptools
Requires: python2-six
%if 0%{?fedora} || 0%{?rhel} > 7
Requires: python2-enum34
Requires: python2-stevedore
%else
Requires: python-enum34
Requires: python-stevedore
%endif
%if 0%{?fedora} && 0%{?fedora} <= 29
# Python2 binary packages are being removed
# See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
Requires: python2-pycdlib
%endif
%if 0%{?fedora} && 0%{?fedora} <= 30
# More Python2 binary packages removed
Requires: pyliblzma
%endif

%description -n python2-%{pkgname}
Avocado is a set of tools and libraries (what people call
these days a framework) to perform automated testing.

%files -n python2-%{pkgname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/avocado/
%{python2_sitelib}/avocado_framework-%{version}-py%{python2_version}.egg-info
%{_bindir}/avocado-%{python2_version}
%{_bindir}/avocado-2
%{_bindir}/avocado-rest-client-%{python2_version}
%{_bindir}/avocado-rest-client-2
%if %{without python3}
%{_bindir}/avocado
%{_bindir}/avocado-rest-client
%endif
%endif

%if %{with python3}
%package -n python3-%{pkgname}
Summary: %{summary}
License: GPLv2 and MIT
%{?python_provide:%python_provide python3-%{pkgname}}
Requires: python-%{pkgname}-common == %{version}-%{release}
Requires: gdb
Requires: gdb-gdbserver
Requires: procps-ng
Requires: python3
Requires: python3-requests
Requires: python3-setuptools
Requires: python%{pypref}-six
%if 0%{?fedora} || 0%{?rhel} > 7
Requires: python3-stevedore
Requires: python3-pycdlib
%endif

%description -n python3-%{pkgname}
Avocado is a set of tools and libraries (what people call
these days a framework) to perform automated testing.

%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/avocado/
%{python3_sitelib}/avocado_framework-%{version}-py%{python3_version}.egg-info
%{_bindir}/avocado-%{python3_version}
%{_bindir}/avocado-3
%{_bindir}/avocado
%{_bindir}/avocado-rest-client-%{python3_version}
%{_bindir}/avocado-rest-client-3
%{_bindir}/avocado-rest-client
%endif


%package -n python-%{pkgname}-common
Summary: Avocado common files

%description -n python-%{pkgname}-common
Common files (such as configuration) for the Avocado Testing Framework.

%files -n python-%{pkgname}-common
%{_mandir}/man1/avocado.1.gz
%{_mandir}/man1/avocado-rest-client.1.gz
%dir %{_docdir}/avocado
%dir %{_sharedstatedir}/avocado
%dir %{_sysconfdir}/avocado
%dir %{_sysconfdir}/avocado/conf.d
%dir %{_sysconfdir}/avocado/sysinfo
%dir %{_sysconfdir}/avocado/scripts
%dir %{_sysconfdir}/avocado/scripts/job
%dir %{_sysconfdir}/avocado/scripts/job/pre.d
%dir %{_sysconfdir}/avocado/scripts/job/post.d
%config(noreplace) %{_sysconfdir}/avocado/avocado.conf
%config(noreplace) %{_sysconfdir}/avocado/conf.d/gdb.conf
%config(noreplace) %{_sysconfdir}/avocado/conf.d/jobscripts.conf
%config(noreplace) %{_sysconfdir}/avocado/sysinfo/commands
%config(noreplace) %{_sysconfdir}/avocado/sysinfo/files
%config(noreplace) %{_sysconfdir}/avocado/sysinfo/profilers
%{_sysconfdir}/avocado/conf.d/README
%{_sysconfdir}/avocado/scripts/job/pre.d/README
%{_sysconfdir}/avocado/scripts/job/post.d/README


%if %{with python2}
%package -n python2-%{pkgname}-plugins-output-html
Summary: Avocado HTML report plugin
%{?python_provide:%python_provide python2-%{pkgname}-plugins-output-html}
Requires: python2-%{pkgname} == %{version}-%{release}
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
Requires: python2-jinja2
%else
Requires: python-jinja2
%endif

%description -n python2-%{pkgname}-plugins-output-html
Adds to avocado the ability to generate an HTML report at every job results
directory. It also gives the user the ability to write a report on an
arbitrary filesystem location.

%files -n python2-%{pkgname}-plugins-output-html
%{python2_sitelib}/avocado_result_html/
%{python2_sitelib}/avocado_framework_plugin_result_html-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-output-html
Summary: Avocado HTML report plugin
%{?python_provide:%python_provide python3-%{pkgname}-plugins-output-html}
Requires: python3-%{pkgname} == %{version}-%{release}
Requires: python%{pypref}-jinja2

%description -n python3-%{pkgname}-plugins-output-html
Adds to avocado the ability to generate an HTML report at every job results
directory. It also gives the user the ability to write a report on an
arbitrary filesystem location.

%files -n python3-%{pkgname}-plugins-output-html
%{python3_sitelib}/avocado_result_html/
%{python3_sitelib}/avocado_framework_plugin_result_html-%{version}-py%{python3_version}.egg-info
%endif


%if %{with_fabric}
%if %{with python2}
%package -n python2-%{pkgname}-plugins-runner-remote
Summary: Avocado Runner for Remote Execution
%{?python_provide:%python_provide python2-%{pkgname}-plugins-runner-remote}
Requires: python2-%{pkgname} == %{version}-%{release}
%if 0%{?fedora} >= 29
Requires: python2-fabric3
%else
Requires: fabric
%endif

%description -n python2-%{pkgname}-plugins-runner-remote
Allows Avocado to run jobs on a remote machine, by means of an SSH
connection. Avocado must be previously installed on the remote machine.

%files -n python2-%{pkgname}-plugins-runner-remote
%{python2_sitelib}/avocado_runner_remote/
%{python2_sitelib}/avocado_framework_plugin_runner_remote-%{version}-py%{python2_version}.egg-info
%endif

%if %{with_python3_fabric}
%package -n python3-%{pkgname}-plugins-runner-remote
Summary: Avocado Runner for Remote Execution
%{?python_provide:%python_provide python3-%{pkgname}-plugins-runner-remote}
Requires: python3-%{pkgname} == %{version}-%{release}
Requires: python3-fabric3

%description -n python3-%{pkgname}-plugins-runner-remote
Allows Avocado to run jobs on a remote machine, by means of an SSH
connection. Avocado must be previously installed on the remote machine.

%files -n python3-%{pkgname}-plugins-runner-remote
%{python3_sitelib}/avocado_runner_remote/
%{python3_sitelib}/avocado_framework_plugin_runner_remote-%{version}-py%{python3_version}.egg-info
%endif
%endif


%if %{with_fabric}
%if %{with python2}
%package -n python2-%{pkgname}-plugins-runner-vm
Summary: Avocado Runner for libvirt VM Execution
%{?python_provide:%python_provide python2-%{pkgname}-plugins-runner-vm}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: python2-%{pkgname}-plugins-runner-remote == %{version}-%{release}
%if 0%{?fedora} >= 27 || 0%{?rhel} > 7
Requires: python2-libvirt
%else
Requires: libvirt-python
%endif

%description -n python2-%{pkgname}-plugins-runner-vm
Allows Avocado to run jobs on a libvirt based VM, by means of
interaction with a libvirt daemon and an SSH connection to the VM
itself. Avocado must be previously installed on the VM.

%files -n python2-%{pkgname}-plugins-runner-vm
%{python2_sitelib}/avocado_runner_vm/
%{python2_sitelib}/avocado_framework_plugin_runner_vm-%{version}-py%{python2_version}.egg-info
%endif

%if %{with_python3_fabric}
%package -n python3-%{pkgname}-plugins-runner-vm
Summary: Avocado Runner for libvirt VM Execution
%{?python_provide:%python_provide python3-%{pkgname}-plugins-runner-vm}
Requires: python3-%{pkgname} == %{version}-%{release}
Requires: python3-%{pkgname}-plugins-runner-remote == %{version}-%{release}
Requires: python3-libvirt

%description -n python3-%{pkgname}-plugins-runner-vm
Allows Avocado to run jobs on a libvirt based VM, by means of
interaction with a libvirt daemon and an SSH connection to the VM
itself. Avocado must be previously installed on the VM.

%files -n python3-%{pkgname}-plugins-runner-vm
%{python3_sitelib}/avocado_runner_vm/
%{python3_sitelib}/avocado_framework_plugin_runner_vm-%{version}-py%{python3_version}.egg-info
%endif
%endif


%if %{with_fabric}
%if %{with python2}
%package -n python2-%{pkgname}-plugins-runner-docker
Summary: Avocado Runner for Execution on Docker Containers
%{?python_provide:%python_provide python2-%{pkgname}-plugins-runner-docker}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: python2-%{pkgname}-plugins-runner-remote == %{version}-%{release}
Requires: python2-aexpect

%description -n python2-%{pkgname}-plugins-runner-docker
Allows Avocado to run jobs on a Docker container by interacting with a
Docker daemon and attaching to the container itself. Avocado must
be previously installed on the container.

%files -n python2-%{pkgname}-plugins-runner-docker
%{python2_sitelib}/avocado_runner_docker/
%{python2_sitelib}/avocado_framework_plugin_runner_docker-%{version}-py%{python2_version}.egg-info
%endif

%if %{with_python3_fabric}
%package -n python3-%{pkgname}-plugins-runner-docker
Summary: Avocado Runner for Execution on Docker Containers
%{?python_provide:%python_provide python3-%{pkgname}-plugins-runner-docker}
Requires: python3-%{pkgname} == %{version}-%{release}
Requires: python3-%{pkgname}-plugins-runner-remote == %{version}-%{release}
Requires: python3-aexpect

%description -n python3-%{pkgname}-plugins-runner-docker
Allows Avocado to run jobs on a Docker container by interacting with a
Docker daemon and attaching to the container itself. Avocado must
be previously installed on the container.

%files -n python3-%{pkgname}-plugins-runner-docker
%{python3_sitelib}/avocado_runner_docker/
%{python3_sitelib}/avocado_framework_plugin_runner_docker-%{version}-py%{python3_version}.egg-info
%endif
%endif


%if %{with_python2_resultsdb}
%package -n python2-%{pkgname}-plugins-resultsdb
Summary: Avocado plugin to propagate job results to ResultsDB
%{?python_provide:%python_provide python2-%{pkgname}-plugins-resultsdb}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: python2-resultsdb_api

%description -n python2-%{pkgname}-plugins-resultsdb
Allows Avocado to send job results directly to a ResultsDB
server.

%files -n python2-%{pkgname}-plugins-resultsdb
%{python2_sitelib}/avocado_resultsdb/
%{python2_sitelib}/avocado_framework_plugin_resultsdb-%{version}-py%{python2_version}.egg-info
%config(noreplace) %{_sysconfdir}/avocado/conf.d/resultsdb.conf
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-resultsdb
Summary: Avocado plugin to propagate job results to ResultsDB
%{?python_provide:%python_provide python3-%{pkgname}-plugins-resultsdb}
Requires: python3-%{pkgname} == %{version}-%{release}
Requires: python3-resultsdb_api

%description -n python3-%{pkgname}-plugins-resultsdb
Allows Avocado to send job results directly to a ResultsDB
server.

%files -n python3-%{pkgname}-plugins-resultsdb
%{python3_sitelib}/avocado_resultsdb/
%{python3_sitelib}/avocado_framework_plugin_resultsdb-%{version}-py%{python3_version}.egg-info
%config(noreplace) %{_sysconfdir}/avocado/conf.d/resultsdb.conf
%endif


%if %{with python2}
%package -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
Summary: Avocado plugin to generate variants out of yaml files
%{?python_provide:%python_provide python2-%{pkgname}-plugins-varianter-yaml-to-mux}
Requires: python2-%{pkgname} == %{version}-%{release}
%if 0%{?fedora} >= 27 || 0%{?rhel} > 7
Requires: python2-yaml
%else
Requires: python-yaml
%endif

%description -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
Can be used to produce multiple test variants with test parameters
defined in a yaml file(s).

%files -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
%{python2_sitelib}/avocado_varianter_yaml_to_mux/
%{python2_sitelib}/avocado_framework_plugin_varianter_yaml_to_mux-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-varianter-yaml-to-mux
Summary: Avocado plugin to generate variants out of yaml files
%{?python_provide:%python_provide python3-%{pkgname}-plugins-varianter-yaml-to-mux}
Requires: python3-%{pkgname} == %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: python%{pypref}-PyYAML
%else
Requires: python3-yaml
%endif

%description -n python3-%{pkgname}-plugins-varianter-yaml-to-mux
Can be used to produce multiple test variants with test parameters
defined in a yaml file(s).

%files -n python3-%{pkgname}-plugins-varianter-yaml-to-mux
%{python3_sitelib}/avocado_varianter_yaml_to_mux/
%{python3_sitelib}/avocado_framework_plugin_varianter_yaml_to_mux-%{version}-py%{python3_version}.egg-info
%endif


%if %{with python2}
%package -n python2-%{pkgname}-plugins-loader-yaml
Summary: Avocado plugin that loads tests from YAML files
%{?python_provide:%python_provide python2-%{pkgname}-plugins-loader-yaml}
Requires: python2-%{pkgname}-plugins-varianter-yaml-to-mux == %{version}-%{release}

%description -n python2-%{pkgname}-plugins-loader-yaml
Can be used to produce a test suite from definitions in a YAML file,
similar to the one used in the yaml_to_mux varianter plugin.

%files -n python2-%{pkgname}-plugins-loader-yaml
%{python2_sitelib}/avocado_loader_yaml/
%{python2_sitelib}/avocado_framework_plugin_loader_yaml-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-loader-yaml
Summary: Avocado plugin that loads tests from YAML files
%{?python_provide:%python_provide python3-%{pkgname}-plugins-loader-yaml}
Requires: python3-%{pkgname}-plugins-varianter-yaml-to-mux == %{version}-%{release}

%description -n python3-%{pkgname}-plugins-loader-yaml
Can be used to produce a test suite from definitions in a YAML file,
similar to the one used in the yaml_to_mux varianter plugin.

%files -n python3-%{pkgname}-plugins-loader-yaml
%{python3_sitelib}/avocado_loader_yaml/
%{python3_sitelib}/avocado_framework_plugin_loader_yaml-%{version}-py%{python3_version}.egg-info
%endif


%if %{with python2}
%package -n python2-%{pkgname}-plugins-golang
Summary: Avocado plugin for execution of golang tests
%{?python_provide:%python_provide python2-%{pkgname}-plugins-golang}
Requires: python2-%{pkgname} == %{version}-%{release}
Requires: golang

%description -n python2-%{pkgname}-plugins-golang
Allows Avocado to list golang tests, and if golang is installed,
also run them.

%files -n python2-%{pkgname}-plugins-golang
%{python2_sitelib}/avocado_golang/
%{python2_sitelib}/avocado_framework_plugin_golang-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-golang
Summary: Avocado plugin for execution of golang tests
%{?python_provide:%python_provide python3-%{pkgname}-plugins-golang}
Requires: python3-%{pkgname} == %{version}-%{release}
Requires: golang

%description -n python3-%{pkgname}-plugins-golang
Allows Avocado to list golang tests, and if golang is installed,
also run them.

%files -n python3-%{pkgname}-plugins-golang
%{python3_sitelib}/avocado_golang/
%{python3_sitelib}/avocado_framework_plugin_golang-%{version}-py%{python3_version}.egg-info
%endif


%if %{with python2}
%package -n python2-%{pkgname}-plugins-varianter-pict
Summary: Varianter with combinatorial capabilities by PICT
%{?python_provide:%python_provide python2-%{pkgname}-plugins-varianter-pict}
Requires: python2-%{pkgname} == %{version}-%{release}

%description -n python2-%{pkgname}-plugins-varianter-pict
This plugin uses a third-party tool to provide variants created by
Pair-Wise algorithms, also known as Combinatorial Independent Testing.

%files -n python2-%{pkgname}-plugins-varianter-pict
%{python2_sitelib}/avocado_varianter_pict/
%{python2_sitelib}/avocado_framework_plugin_varianter_pict-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-varianter-pict
Summary: Varianter with combinatorial capabilities by PICT
%{?python_provide:%python_provide python3-%{pkgname}-plugins-varianter-pict}
Requires: python3-%{pkgname} == %{version}-%{release}

%description -n python3-%{pkgname}-plugins-varianter-pict
This plugin uses a third-party tool to provide variants created by
Pair-Wise algorithms, also known as Combinatorial Independent Testing.

%files -n python3-%{pkgname}-plugins-varianter-pict
%{python3_sitelib}/avocado_varianter_pict/
%{python3_sitelib}/avocado_framework_plugin_varianter_pict-%{version}-py%{python3_version}.egg-info
%endif


%if %{with python2}
%package -n python2-%{pkgname}-plugins-varianter-cit
Summary: Varianter with Combinatorial Independent Testing capabilities
%{?python_provide:%python_provide python2-%{pkgname}-plugins-varianter-cit}
Requires: python2-%{pkgname} == %{version}-%{release}

%description -n python2-%{pkgname}-plugins-varianter-cit
A varianter plugin that generates variants using Combinatorial
Independent Testing (AKA Pair-Wise) algorithm developed in
collaboration with CVUT Prague.

%files -n python2-%{pkgname}-plugins-varianter-cit
%{python2_sitelib}/avocado_varianter_cit/
%{python2_sitelib}/avocado_framework_plugin_varianter_cit-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-varianter-cit
Summary: Varianter with Combinatorial Independent Testing capabilities
%{?python_provide:%python_provide python3-%{pkgname}-plugins-varianter-cit}
Requires: python3-%{pkgname} == %{version}-%{release}

%description -n python3-%{pkgname}-plugins-varianter-cit
A varianter plugin that generates variants using Combinatorial
Independent Testing (AKA Pair-Wise) algorithm developed in
collaboration with CVUT Prague.

%files -n python3-%{pkgname}-plugins-varianter-cit
%{python3_sitelib}/avocado_varianter_cit/
%{python3_sitelib}/avocado_framework_plugin_varianter_cit-%{version}-py%{python3_version}.egg-info
%endif


%if %{with python2}
%package -n python2-%{pkgname}-plugins-result-upload
Summary: Avocado plugin propagate job results to a remote host
%{?python_provide:%python_provide python2-%{pkgname}-plugins-result-upload}
Requires: python2-%{pkgname} == %{version}-%{release}

%description -n python2-%{pkgname}-plugins-result-upload
This optional plugin is intended to upload the Avocado Job results to
a dedicated sever.

%files -n python2-%{pkgname}-plugins-result-upload
%{python2_sitelib}/avocado_result_upload/
%{python2_sitelib}/avocado_framework_plugin_result_upload-%{version}-py%{python2_version}.egg-info
%config(noreplace) %{_sysconfdir}/avocado/conf.d/result_upload.conf
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-result-upload
Summary: Avocado plugin propagate job results to a remote host
%{?python_provide:%python_provide python3-%{pkgname}-plugins-result-upload}
Requires: python3-%{pkgname} == %{version}-%{release}

%description -n python3-%{pkgname}-plugins-result-upload
This optional plugin is intended to upload the Avocado Job results to
a dedicated sever.

%files -n python3-%{pkgname}-plugins-result-upload
%{python3_sitelib}/avocado_result_upload/
%{python3_sitelib}/avocado_framework_plugin_result_upload-%{version}-py%{python3_version}.egg-info
%config(noreplace) %{_sysconfdir}/avocado/conf.d/result_upload.conf
%endif


%if %{with python2}
%package -n python2-%{pkgname}-plugins-glib
Summary: Avocado plugin for execution of GLib Test Framework tests
%{?python_provide:%python_provide python2-%{pkgname}-plugins-glib}
Requires: python2-%{pkgname} == %{version}-%{release}

%description -n python2-%{pkgname}-plugins-glib
This optional plugin is intended to list and run tests written in the
GLib Test Framework.

%files -n python2-%{pkgname}-plugins-glib
%{python2_sitelib}/avocado_glib/
%{python2_sitelib}/avocado_framework_plugin_glib-%{version}-py%{python2_version}.egg-info
%endif

%if %{with python3}
%package -n python3-%{pkgname}-plugins-glib
Summary: Avocado plugin for execution of GLib Test Framework tests
%{?python_provide:%python_provide python3-%{pkgname}-plugins-glib}
Requires: python3-%{pkgname} == %{version}-%{release}

%description -n python3-%{pkgname}-plugins-glib
This optional plugin is intended to list and run tests written in the
GLib Test Framework.

%files -n python3-%{pkgname}-plugins-glib
%{python3_sitelib}/avocado_glib/
%{python3_sitelib}/avocado_framework_plugin_glib-%{version}-py%{python3_version}.egg-info
%endif


%package -n python-%{pkgname}-examples
Summary: Avocado Test Framework Example Tests
License: GPLv2
# documentation does not require main package, but needs to be in lock-step if present
%if %{with python2}
Conflicts: python2-%{pkgname} < %{version}-%{release}, python2-%{pkgname} > %{version}-%{release}
%endif
%if %{with python3}
Conflicts: python3-%{pkgname} < %{version}-%{release}, python3-%{pkgname} > %{version}-%{release}
%endif

%description -n python-%{pkgname}-examples
The set of example tests present in the upstream tree of the Avocado framework.
Some of them are used as functional tests of the framework, others serve as
examples of how to write tests on your own.

%files -n python-%{pkgname}-examples
%dir %{_docdir}/avocado
%{_docdir}/avocado/gdb-prerun-scripts
%{_docdir}/avocado/plugins
%{_docdir}/avocado/tests
%{_docdir}/avocado/varianter_cit
%{_docdir}/avocado/varianter_pict
%{_docdir}/avocado/wrappers
%{_docdir}/avocado/yaml_to_mux
%{_docdir}/avocado/yaml_to_mux_loader


%package -n python-%{pkgname}-bash
Summary: Avocado Test Framework Bash Utilities
Requires: python-%{pkgname}-common == %{version}-%{release}

%description -n python-%{pkgname}-bash
A small set of utilities to interact with Avocado from the Bourne
Again Shell code (and possibly other similar shells).

%files -n python-%{pkgname}-bash
%dir %{_libexecdir}/avocado
%{_libexecdir}/avocado/avocado-bash-utils
%{_libexecdir}/avocado/avocado_debug
%{_libexecdir}/avocado/avocado_error
%{_libexecdir}/avocado/avocado_info
%{_libexecdir}/avocado/avocado_warn


%changelog
* Tue Feb 23 2021 Brian J. Murrell <brian.murrell@intel.com> - 69.2-1.01
- Build with python3 on EL7

* Fri Oct 04 2019 Merlin Mathesius <mmathesi@redhat.com> - 69.2-1
- Sync with upstream release 69.2 (LTS series).

* Wed Sep 11 2019 Merlin Mathesius <mmathesi@redhat.com> - 69.1-3
- Update patch to always skip unreliable selftest.

* Mon Sep 09 2019 Merlin Mathesius <mmathesi@redhat.com> - 69.1-2
- Patch to skip selftest currently incompatible with Python 3.8.

* Tue Jun 18 2019 Merlin Mathesius <mmathesi@redhat.com> - 69.1-1
- Sync with upstream release 69.1 (LTS series).

* Wed May 22 2019 Merlin Mathesius <mmathesi@redhat.com> - 69.0-4
- pyliblzma is Python 2-only and no longer available as of F31.
- Unversioned executables should now be Python 3.

* Mon May 20 2019 Merlin Mathesius <mmathesi@redhat.com> - 69.0-3
- Drop Python 2 support from F31 and RHEL8 onward.
- Disable components dependent upon Fiber in Fedora 31 and later,
  since avocado is currently incompatible with the new Fiber API.

* Tue Mar 19 2019 Merlin Mathesius <mmathesi@redhat.com> - 69.0-2
- python2-sphinx is no longer available or needed as of F31

* Wed Feb 27 2019 Merlin Mathesius <mmathesi@redhat.com> - 69.0-1
- Sync with upstream release 69.0.

* Fri Feb 22 2019 Merlin Mathesius <mmathesi@redhat.com> - 68.0-1
- Sync with upstream release 68.0.

* Thu Jan 31 2019 Merlin Mathesius <mmathesi@redhat.com> - 67.0-1
- Sync with upstream release 67.0.
- genisoimage, libcdio, and psmisc added as build deps so iso9660 tests run.
- Replace pystache requirement with jinja2.
- glibc-all-langpacks added as build dep for F30+ so vmimage tests run.
- python2-resultsdb_api package has been removed in F30 so
  python2-avocado-plugins-resultsdb was also disabled.

* Wed Nov 21 2018 Merlin Mathesius <mmathesi@redhat.com> - 66.0-1
- Sync with upstream release 66.0.
- python2-pycdlib package has been removed in F30 as part of
  https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 04 2018 Merlin Mathesius <mmathesi@redhat.com> - 65.0-1
- Sync with upstream release 65.0.

* Tue Aug 28 2018 Merlin Mathesius <mmathesi@redhat.com> - 64.0-1
- Sync with upstream release 64.0.

* Thu Jul 26 2018 Merlin Mathesius <mmathesi@redhat.com> - 63.0-2
- Added missing python[2]-enum34 requirement.

* Mon Jul 23 2018 Merlin Mathesius <mmathesi@redhat.com> - 63.0-1
- Sync with upstream release 63.0. (BZ#1602175)
  Include upstream patches needed to build for Rawhide.

* Wed Jun 13 2018 Merlin Mathesius <mmathesi@redhat.com> - 62.0-1
- Sync with upstream release 62.0. (BZ#1590572)
- Correct libvirt dependency for EPEL7/RHEL7

* Thu May 17 2018 Merlin Mathesius <mmathesi@redhat.com> - 61.0-1
- Sync with upstream release 61.0.
- Packaging updates for Python 3.
- Reorganize SPEC file.

* Mon Apr  9 2018 Cleber Rosa <cleber@redhat.com> - 52.1-2
- Added Fedora CI tests

* Tue Apr 03 2018 Merlin Mathesius <mmathesi@redhat.com> - 52.1-1
- Sync with upstream release 52.1 (LTS series).
- Correct deprecated use of unversioned python.

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 52.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 52.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 09 2017 Merlin Mathesius <mmathesi@redhat.com> - 52.0-3
- Fix FTBFS error by disabling selfcheck producing false failures
- Update SPEC to use pkgname instead of srcname macro where appropriate

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 52.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Merlin Mathesius <mmathesi@redhat.com> - 52.0-1
- Sync with upstream release 52.0. (BZ#1465409)

* Wed Jun 14 2017 Merlin Mathesius <mmathesi@redhat.com> - 51.0-1
- Sync with upstream release 51.0. (BZ#1460837)
- Disable selftests when libvirt may not be available.

* Wed May 17 2017 Merlin Mathesius <mmathesi@redhat.com> - 50.0-1
- Sync with upstream release 50.0. (BZ#1431413)
- Be explicit about selftest level run on check.

* Tue Apr 25 2017 Merlin Mathesius <mmathesi@redhat.com> - 49.0-1
- Sync with upstream release 49.0. (BZ#1431413)

* Tue Apr 18 2017 Merlin Mathesius <mmathesi@redhat.com> - 48.0-1
- Sync with upstream release 48.0. (BZ#1431413)
- Allow rel_build macro to be defined outside of the SPEC file.

* Mon Mar 27 2017 Merlin Mathesius <mmathesi@redhat.com> - 47.0-1
- Sync with upstream release 47.0.
- Enable self-tests during build.
- Add example test to be run by Taskotron.

* Mon Feb 27 2017 Merlin Mathesius <mmathesi@redhat.com> - 46.0-2
- Incorporate upstream SPEC file changes to split plugins into subpackages.
- Remove obsolete CC-BY-SA license, which went away with the halflings font.

* Tue Feb 14 2017 Merlin Mathesius <mmathesi@redhat.com> - 46.0-1
- Sync with upstream release 46.0.
- Remove halflings license since font was removed from upstream.
- SPEC updates to easily switch between release and snapshot builds.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 43.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 10 2017 Merlin Mathesius <mmathesi@redhat.com> - 43.0-7
- SPEC updates to build and install for EPEL.

* Mon Nov 21 2016 Merlin Mathesius <mmathesi@redhat.com> - 43.0-6
- Initial packaging for Fedora.
