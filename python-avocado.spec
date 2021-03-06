#
# spec file for package python-avocado
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%{!?ifpython2: %define ifpython2    \
%if "%{python_flavor}" == "python2" \
%{nil}                              \
}

%{!?python_subpackages: %define python_subpackages \
%{nil}                                             \
}

%{!?python_files: %define python_files \
%{nil}                                 \
}


# No longer build for python2
#define skip_python2  1
%{?!python_module:%define python_module() python-%{**} python3-%{**}}
%define         pkgname avocado
Name:           python-avocado
Version:        52.1
Release:        lp152.6.2.01
Summary:        Avocado Test Framework
License:        GPL-2.0-only
Group:          Development/Tools/Other
URL:            https://avocado-framework.github.io/
Source:         https://github.com/avocado-framework/avocado/archive/%{version}.tar.gz#/%{pkgname}-%{version}.tar.gz
#Patch1:         PR-3076.patch
BuildRequires:  %{python_module Sphinx}
BuildRequires:  %{python_module aexpect}
BuildRequires:  %{python_module devel}
BuildRequires:  %{python_module docutils}
BuildRequires:  %{python_module lxml}
BuildRequires:  %{python_module psutil}
BuildRequires:  %{python_module pyaml}
BuildRequires:  %{python_module pystache}
BuildRequires:  %{python_module requests} >= 1.2.3
BuildRequires:  %{python_module resultsdb_api}
BuildRequires:  %{python_module setuptools} >= 18.0.0
BuildRequires:  %{python_module six} >= 1.11.0
BuildRequires:  %{python_module stevedore} >= 0.14
BuildRequires:  fdupes
BuildRequires:  kmod
BuildRequires:  libvirt-devel
BuildRequires:  procps
BuildRequires:  python-rpm-macros
Requires:       %{pkgname}-common
Requires:       gdb
Requires:       procps
Requires:       python-Fabric
Requires:       python-requests >= 1.2.3
Requires:       python-setuptools
Requires:       python-six >= 1.11.0
Requires:       python-stevedore >= 0.14
Requires(post): update-alternatives
Requires(postun): update-alternatives
Provides:       %{pkgname} = %{version}
Obsoletes:      %{pkgname} < %{version}
BuildArch:      noarch
%if 0%{?suse_version} >= 1500
%if 0%{?sle_version} < 150200
BuildRequires:  %{python_module libvirt-python}
%else
BuildRequires:  python3-libvirt-python
%endif
%else
BuildRequires:  python-libvirt-python
%endif
%ifpython2
Requires:       python2-pylzma
Requires:       python2-subprocess32 >= 3.2.6
%endif
%python_subpackages

%description
Avocado is a set of tools and libraries (what people call these days a
framework) to perform automated testing.

%package  -n    %{pkgname}-common
Summary:        Avocado Test Framework
Group:          Development/Languages/Python
Conflicts:      avocado < %{version}

%description   -n  %{pkgname}-common
Avocado is a set of tools and libraries (what people call these days a
framework) to perform automated testing.

This package contains common infrastructure files.

%if 0%{?have_python2} && ! 0%{?skip_python2}
%package -n python2-%{pkgname}-plugins-output-html
Summary:        Avocado HTML report plugin
Group:          Development/Languages/Python
Requires:       python2-%{pkgname} = %{version}
Requires:       python2-pystache

%description -n python2-%{pkgname}-plugins-output-html
This plugin adds the ability for Avocado to generate an HTML report in every
job result directory. It also gives the user the ability to write a report to
an arbitrary filesystem location.
%endif

%package -n python3-%{pkgname}-plugins-output-html
Summary:        Avocado HTML report plugin
Group:          Development/Languages/Python
Requires:       python3-%{pkgname} = %{version}
Requires:       python3-pystache

%description -n python3-%{pkgname}-plugins-output-html
This plugin adds the ability for Avocado to generate an HTML report in every
job result directory. It also gives the user the ability to write a report to
an arbitrary filesystem location.

%if 0%{?have_python2} && ! 0%{?skip_python2}
%package -n python2-%{pkgname}-plugins-runner-remote
Summary:        Avocado Runner for Remote Execution
Group:          Development/Languages/Python
Requires:       python2-%{pkgname} = %{version}
Requires:       python2-Fabric

%description -n python2-%{pkgname}-plugins-runner-remote
This plugin allows Avocado to run jobs on a remote machine, by means of an SSH
connection. Avocado must have been previously installed on the remote machine.
%endif

%package -n python3-%{pkgname}-plugins-runner-remote
Summary:        Avocado Runner for Remote Execution
Group:          Development/Languages/Python
Requires:       python3-%{pkgname} = %{version}
Requires:       python3-Fabric

%description -n python3-%{pkgname}-plugins-runner-remote
This plugin allows Avocado to run jobs on a remote machine, by means of an SSH
connection. Avocado must have been previously installed on the remote machine.

%if 0%{?sle_version} >= 150200
%else
%if 0%{?have_python2} && ! 0%{?skip_python2}
%package -n python2-%{pkgname}-plugins-runner-vm
Summary:        Avocado Runner for libvirt VM Execution
Group:          Development/Languages/Python
Requires:       python2-%{pkgname} = %{version}
Requires:       python2-%{pkgname}-plugins-runner-remote = %{version}
Requires:       python2-libvirt-python

%description -n python2-%{pkgname}-plugins-runner-vm
This plugin allows Avocado to run jobs within a libvirt-based virtual machine,
by means of interaction with a libvirt daemon and an SSH connection to the VM
itself. Avocado must have been previously installed on the VM.
%endif
%endif

%package -n python3-%{pkgname}-plugins-runner-vm
Summary:        Avocado Runner for libvirt VM Execution
Group:          Development/Languages/Python
Requires:       python3-%{pkgname} = %{version}
Requires:       python3-%{pkgname}-plugins-runner-remote = %{version}
Requires:       python3-libvirt-python

%description -n python3-%{pkgname}-plugins-runner-vm
This plugin allows Avocado to run jobs within a libvirt-based virtual machine,
by means of interaction with a libvirt daemon and an SSH connection to the VM
itself. Avocado must have been previously installed on the VM.

%if 0%{?have_python2} && ! 0%{?skip_python2}
%package -n python2-%{pkgname}-plugins-runner-docker
Summary:        Avocado Runner for Execution on Docker Containers
Group:          Development/Languages/Python
Requires:       python2-%{pkgname} = %{version}
Requires:       python2-%{pkgname}-plugins-runner-remote = %{version}
Requires:       python2-aexpect

%description -n python2-%{pkgname}-plugins-runner-docker
This plugin allows Avocado to run jobs within a Docker container, by
interacting with a Docker daemon and attaching to the container itself. Avocado
must have been previously installed in the container.
%endif

%package -n python3-%{pkgname}-plugins-runner-docker
Summary:        Avocado Runner for Execution on Docker Containers
Group:          Development/Languages/Python
Requires:       python3-%{pkgname} = %{version}
Requires:       python3-%{pkgname}-plugins-runner-remote = %{version}
Requires:       python3-aexpect

%description -n python3-%{pkgname}-plugins-runner-docker
This plugin allows Avocado to run jobs within a Docker container, by
interacting with a Docker daemon and attaching to the container itself. Avocado
must have been previously installed in the container.

%if 0%{?have_python2} && ! 0%{?skip_python2}
%package -n python2-%{pkgname}-plugins-resultsdb
Summary:        Avocado plugin to propagate job results to ResultsDB
Group:          Development/Languages/Python
Requires:       python2-%{pkgname} = %{version}
Requires:       python2-resultsdb_api

%description -n python2-%{pkgname}-plugins-resultsdb
This plugin allows Avocado to send job results directly to a ResultsDB
server.
%endif

%package -n python3-%{pkgname}-plugins-resultsdb
Summary:        Avocado plugin to propagate job results to ResultsDB
Group:          Development/Languages/Python
Requires:       python3-%{pkgname} = %{version}
Requires:       python3-resultsdb_api

%description -n python3-%{pkgname}-plugins-resultsdb
Allows Avocado to send job results directly to a ResultsDB
server.

%if 0%{?have_python2} && ! 0%{?skip_python2}
%package -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
Summary:        Avocado plugin to generate variants out of yaml files
Group:          Development/Languages/Python
Requires:       python2-%{pkgname} = %{version}
Requires:       python2-pyaml

%description -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
This plugin can be used to produce multiple test variants with test parameters
defined in one or more YAML files.
%endif

%package -n python3-%{pkgname}-plugins-varianter-yaml-to-mux
Summary:        Avocado plugin to generate variants out of yaml files
Group:          Development/Languages/Python
Requires:       python3-%{pkgname} = %{version}
Requires:       python3-pyaml

%description -n python3-%{pkgname}-plugins-varianter-yaml-to-mux
This plugin can be used to produce multiple test variants with test parameters
defined in one or more YAML files.

%package -n %{pkgname}-examples
Summary:        Avocado Test Framework Example Tests
Group:          Development/Tools/Other
Requires:       %{pkgname} = %{version}

%description -n %{pkgname}-examples
The set of example tests present in the upstream tree of the Avocado framework.
Some of them are used as functional tests of the framework, others serve as
examples of how to write tests on your own.

%prep
%autosetup -p1 -n %{pkgname}-%{version}

%build
%python_build
make %{?_smp_mflags} man

pushd optional_plugins/html
%python_build
popd
pushd optional_plugins/runner_remote
%python_build
popd
pushd optional_plugins/runner_vm
%if 0%{?sle_version} >= 150200
/usr/bin/python3 setup.py  build \
    --executable="/usr/bin/python3 -s" 
%else
%python_build
%endif
popd
pushd optional_plugins/runner_docker
%python_build
popd
pushd optional_plugins/resultsdb
%python_build
popd
pushd optional_plugins/varianter_yaml_to_mux
%python_build
popd

%install
%python_install

pushd optional_plugins/html
%python_install
popd
pushd optional_plugins/runner_remote
%python_install
popd
pushd optional_plugins/runner_vm
%if 0%{?sle_version} >= 150200
/usr/bin/python3 setup.py  install \
    -O1 --skip-build --force --root %{buildroot} --prefix /usr 
%else
%python_install
%endif
popd
pushd optional_plugins/runner_docker
%python_install
popd
pushd optional_plugins/resultsdb
%python_install
popd
pushd optional_plugins/varianter_yaml_to_mux
%python_install
popd

%python_clone -a %{buildroot}%{_bindir}/avocado
%python_clone -a %{buildroot}%{_bindir}/avocado-rest-client

# Reduce duplicates
%python_expand %fdupes %{buildroot}%{$python_sitelib}

# Install manpages
install -Dpm 0644 man/avocado.1 \
  %{buildroot}%{_mandir}/man1/avocado.1
install -Dpm 0644 man/avocado-rest-client.1 \
  %{buildroot}%{_mandir}/man1/avocado-rest-client.1

# Prepare common directories
install -d -m 0755 %{buildroot}%{_localstatedir}/lib/avocado/data
install -d -m 0755 %{buildroot}%{_docdir}/avocado

# Install examples
cp -r examples/gdb-prerun-scripts %{buildroot}%{_docdir}/avocado
cp -r examples/plugins %{buildroot}%{_docdir}/avocado
cp -r examples/tests %{buildroot}%{_docdir}/avocado
mv  %{buildroot}%{_datadir}/avocado/wrappers %{buildroot}%{_docdir}/avocado
cp -r examples/yaml_to_mux %{buildroot}%{_docdir}/avocado

# Do not ship tests
%python_expand rm -rf %{buildroot}%{_datarootdir}/avocado/tests

# Do not ship libexecdir in wrong place
%python_expand rm -rf %{buildroot}%{$python_sitelib}/%{pkgname}/libexec

# Do not ship etc in wrong place
%python_expand rm -rf %{buildroot}%{$python_sitelib}/%{pkgname}%{_sysconfdir}

# remove .rst files
rm -f %{buildroot}%{_datadir}/doc/avocado/*.rst

%post
%{python_install_alternative avocado avocado-rest-client}

%postun
%{python_uninstall_alternative avocado avocado-rest-client}

%files %{python_files}
%license LICENSE
%python_alternative %{_bindir}/avocado
%python_alternative %{_bindir}/avocado-rest-client
%dir %{python_sitelib}/%{pkgname}
%pycache_only %{python_sitelib}/%{pkgname}/__pycache__
%{python_sitelib}/%{pkgname}/__init__.py*
%{python_sitelib}/%{pkgname}/__main__.py*
%{python_sitelib}/%{pkgname}/core
%{python_sitelib}/%{pkgname}/plugins
%{python_sitelib}/%{pkgname}/utils
%{python_sitelib}/%{pkgname}_framework-%{version}*

%files -n %{pkgname}-common
%license LICENSE
%dir %{_sysconfdir}/avocado
%dir %{_sysconfdir}/avocado/conf.d
%dir %{_sysconfdir}/avocado/sysinfo
%dir %{_sysconfdir}/avocado/scripts
%dir %{_sysconfdir}/avocado/scripts/job
%dir %{_sysconfdir}/avocado/scripts/job/pre.d
%dir %{_sysconfdir}/avocado/scripts/job/post.d
%dir %{_localstatedir}/lib/avocado
%dir %{_libexecdir}/avocado
%{_libexecdir}/avocado/avocado-bash-utils
%{_libexecdir}/avocado/avocado_debug
%{_libexecdir}/avocado/avocado_error
%{_libexecdir}/avocado/avocado_info
%{_libexecdir}/avocado/avocado_warn
%config(noreplace)%{_sysconfdir}/avocado/avocado.conf
%config(noreplace)%{_sysconfdir}/avocado/conf.d/README
%config(noreplace)%{_sysconfdir}/avocado/conf.d/gdb.conf
%config(noreplace)%{_sysconfdir}/avocado/sysinfo/commands
%config(noreplace)%{_sysconfdir}/avocado/sysinfo/files
%config(noreplace)%{_sysconfdir}/avocado/sysinfo/profilers
%config(noreplace)%{_sysconfdir}/avocado/scripts/job/pre.d/README
%config(noreplace)%{_sysconfdir}/avocado/scripts/job/post.d/README
%{_mandir}/man1/avocado-rest-client.1%{?ext_man}
%{_mandir}/man1/avocado.1%{?ext_man}

%if 0%{?have_python2} && ! 0%{?skip_python2}
%files -n python2-%{pkgname}-plugins-output-html
%{python2_sitelib}/avocado_result_html*
%{python2_sitelib}/avocado_framework_plugin_result_html*
%endif

%files -n python3-%{pkgname}-plugins-output-html
%{python3_sitelib}/avocado_result_html*
%{python3_sitelib}/avocado_framework_plugin_result_html*

%if 0%{?have_python2} && ! 0%{?skip_python2}
%files -n python2-%{pkgname}-plugins-runner-remote
%{python2_sitelib}/avocado_runner_remote*
%{python2_sitelib}/avocado_framework_plugin_runner_remote*
%endif

%files -n python3-%{pkgname}-plugins-runner-remote
%{python3_sitelib}/avocado_runner_remote*
%{python3_sitelib}/avocado_framework_plugin_runner_remote*

%if 0%{?sle_version} >= 150200
%else
%if 0%{?have_python2} && ! 0%{?skip_python2}
%files -n python2-%{pkgname}-plugins-runner-vm
%{python2_sitelib}/avocado_runner_vm*
%{python2_sitelib}/avocado_framework_plugin_runner_vm*
%endif
%endif

%files -n python3-%{pkgname}-plugins-runner-vm
%{python3_sitelib}/avocado_runner_vm*
%{python3_sitelib}/avocado_framework_plugin_runner_vm*

%if 0%{?have_python2} && ! 0%{?skip_python2}
%files -n python2-%{pkgname}-plugins-runner-docker
%{python2_sitelib}/avocado_runner_docker*
%{python2_sitelib}/avocado_framework_plugin_runner_docker*
%endif

%files -n python3-%{pkgname}-plugins-runner-docker
%{python3_sitelib}/avocado_runner_docker*
%{python3_sitelib}/avocado_framework_plugin_runner_docker*

%if 0%{?have_python2} && ! 0%{?skip_python2}
%files -n python2-%{pkgname}-plugins-resultsdb
%{python2_sitelib}/avocado_resultsdb*
%{python2_sitelib}/avocado_framework_plugin_resultsdb*
%endif

%files -n python3-%{pkgname}-plugins-resultsdb
%{python3_sitelib}/avocado_resultsdb*
%{python3_sitelib}/avocado_framework_plugin_resultsdb*

%if 0%{?have_python2} && ! 0%{?skip_python2}
%files -n python2-%{pkgname}-plugins-varianter-yaml-to-mux
%{python2_sitelib}/avocado_varianter_yaml_to_mux*
%{python2_sitelib}/avocado_framework_plugin_varianter_yaml_to_mux*
%endif

%files -n python3-%{pkgname}-plugins-varianter-yaml-to-mux
%{python3_sitelib}/avocado_varianter_yaml_to_mux*
%{python3_sitelib}/avocado_framework_plugin_varianter_yaml_to_mux*

%files -n %{pkgname}-examples
%dir %{_docdir}/avocado
%{_docdir}/avocado/gdb-prerun-scripts
%{_docdir}/avocado/plugins
%{_docdir}/avocado/tests
%{_docdir}/avocado/wrappers
%{_docdir}/avocado/yaml_to_mux

%changelog
* Thu Sep 17 2020 Brian J. Murrell <brian.murrell@intel.com>
- Roll back to 52.1 to be in parity with EL7
- Accordingly remove plugins introduced since 52.1

* Thu Jul  9 2020 Brian J. Murrell <brian.murrell@intel.com>
- https://download.opensuse.org/repositories/devel:/languages:/python:/backports/openSUSE_Leap_15.2/src/
- Restart building for python2
- python2-pylzma -> python-pylzma
- Conditially define SLES python2 macros
* Mon May 25 2020 Jason Craig <os-dev@jacraig.com>
- Require python-Fabric instead of python-Fabric3.
  Fabric now supports Python 3 and Fabric3 has declared itself
  deprecated.
* Fri Mar 20 2020 Martin Pluskal <mpluskal@suse.com>
- Add conflict with old avocado for migration
* Thu Feb 20 2020 James Fehlig <jfehlig@suse.com>
- Stop building for python2
* Sat Sep 14 2019 John Vandenberg <jayvdb@gmail.com>
- Use have/skip_python2/3 macros to allow building only one flavour
* Fri Mar  1 2019 Jozef Pupava <jpupava@suse.com>
- Update to version 69
  * No upsteam changelog available
* Wed Jan  2 2019 Martin Pluskal <mpluskal@suse.com>
- Trim not needed dependencies
* Tue Nov 20 2018 Martin Pluskal <mpluskal@suse.com>
- Update dependencies
* Mon Nov  5 2018 Martin Pluskal <mpluskal@suse.com>
- Fix typo in dependencies
* Tue Sep 11 2018 Jan Engelhardt <jengelh@inai.de>
- Fix incomplete grammar of descriptions and comments.
- Add RPM group definitions.
* Mon Jul 30 2018 mpluskal@suse.com
- Merge with upstream/Fedora packaging
* Thu Jul  6 2017 brogers@suse.com
- Fix build failures due to unresolved reference to rst2man
* Fri Mar 31 2017 brogers@suse.com
- Update to v36.4lts (Long Term Stability)
* Tue Dec 20 2016 brogers@suse.com
- Update to v36.3lts (Long Term Stability)
* Tue Nov 22 2016 brogers@suse.com
- Update to v36.2lts (Long Term Stability)
* Wed May 25 2016 brogers@suse.com
- Update to v36.0lts (Long Term Stability)
* Thu Apr 28 2016 brogers@suse.com
- Update to v35.0 (Yes, the version numbering system changed)
* Wed Mar 23 2016 brogers@suse.com
- Update to v0.34.0
* Thu Feb 18 2016 brogers@suse.com
- Update to v0.33.0
* Fri Jan 22 2016 brogers@suse.com
- Fixed typo in BuildRequires list
* Wed Jan 20 2016 brogers@suse.com
- Update to v0.32.0
* Fri Oct  9 2015 brogers@suse.com
- Update to v0.29.0
* Tue Oct  6 2015 brogers@suse.com
- Changed a Requires package name from pyliblzma to python-pyliblzma
* Tue Oct  6 2015 brogers@suse.com
- Changed a Requires package name from gdb-gdbserver to gdbserver
* Mon Oct  5 2015 brogers@suse.com
- Initial Check-in.
  Initial preping of spec file provided with the upstream git repo
  include conforming package names, license name, and adding needed
  %%dir directives.
  A reference to the dir directory also needed to be changed in
  source code by patching.
  Another patch was needed for an issue in a documentation source
  file.
  I attempted to get the make check to work, but gave up for now,
  and just commented that out of the spec file.
