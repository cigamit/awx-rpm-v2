%global python3_pkgversion ¤PYTHON3PKGVERSION¤

%define  debug_package %{nil}
%define _prefix /opt/awx-rpm
%define _mandir %{_prefix}/share/man
%global __os_install_post %{nil}

%define service_user awx
%define service_group awx
%define service_homedir /var/lib/tower
%define service_logdir /var/log/tower
%define service_configdir /etc/tower

Summary: Ansible AWX-RPM
Name: awx-rpm
Version: ¤VERSION¤
Release: 1%{dist}
#Source0: awx-¤VERSION¤.tar.gz
Source1: settings.py-%{version}
Source2: awx-receiver.service-%{version}
Source3: awx-dispatcher.service-%{version}
Source4: awx-wsrelay.service-%{version}
Source5: awx-ws-heartbeat.service-%{version}
Source6: awx-daphne.service-%{version}
Source7: awx-web.service-%{version}
Source20: awx-receptor.service-%{version}
Source21: awx-receptor-hop.service-%{version}
Source22: awx-receptor-worker.service-%{version}
Source23: awx.target-%{version}
Source30: receptor.conf-%{version}
Source31: receptor-hop.conf-%{version}
Source32: receptor-worker.conf-%{version}
Source40: awx-rpm-logo.svg-%{version}
Source8: awx-rpm-nginx.conf-%{version}
#Patch0: awx-patch.patch-%{version}
#Patch1: awx-rpm-extract-strings.patch-%{version}
#Patch2: awx-rpm-branding.patch-%{version}
License: GPLv3
Group: AWX
URL: https://awx.wiki
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}.buildroot
Vendor: AWX
Prefix: %{_prefix}
AutoReqProv: false

Requires: python%{python3_pkgversion} awx-core awx-ui awx-rpm-manage
¤REQUIRES¤

%{?systemd_requires}

%description
%{summary}

%prep

%build

%install

mkdir -p $RPM_BUILD_ROOT/var/lib/awx/rsyslog
mkdir -p $RPM_BUILD_ROOT/var/lib/awx/projects
mkdir -p $RPM_BUILD_ROOT/var/lib/awx/job_status
mkdir -p %{buildroot}/etc/tower

cp %{_sourcedir}/settings.py-%{version} %{buildroot}%{service_configdir}/settings.py
mkdir -p %{buildroot}%{_prefix}/public
mkdir -p %{buildroot}/usr/lib/systemd/system
# awx-channels-worker awx
#for service in awx-wsrelay awx-ws-heartbeat awx-daphne awx-dispatcher awx-receiver awx-receptor awx-receptor-hop awx-receptor-worker; do
for service in awx-web awx-wsrelay awx-ws-heartbeat awx-daphne awx-dispatcher awx-receiver awx-receptor awx-receptor-hop awx-receptor-worker; do
    cp %{_sourcedir}/${service}.service-%{version} %{buildroot}/usr/lib/systemd/system/${service}.service
done

cp %{_sourcedir}/awx.target-%{version} %{buildroot}/usr/lib/systemd/system/awx.target

mkdir -p %{buildroot}/etc/receptor

for receptor in receptor receptor-hop receptor-worker; do
	cp %{_sourcedir}/$receptor.conf-%{version} %{buildroot}/etc/receptor/$receptor.conf
done

mkdir -p %{buildroot}/etc/nginx/conf.d
cp %{_sourcedir}/awx-rpm-nginx.conf-%{version} %{buildroot}/etc/nginx/conf.d/awx-rpm.conf

# Create Virtualenv folder
mkdir -p %{buildroot}%{service_homedir}/venv

mkdir -p $RPM_BUILD_ROOT/etc/nginx/conf.d/

%pre
/usr/bin/getent group %{service_group} >/dev/null || /usr/sbin/groupadd --system %{service_group}
/usr/bin/getent passwd %{service_user} >/dev/null || /usr/sbin/useradd --no-create-home --system -g %{service_group} --home-dir %{service_homedir} -s /bin/bash %{service_user}
/usr/sbin/usermod -s /bin/bash %{service_user}
/usr/bin/gpasswd -a awx redis

%post
if [ ! -f /etc/nginx/nginx.crt ];then
sscg -q --cert-file /etc/nginx/nginx.crt --cert-key-file /etc/nginx/nginx.key --ca-file /etc/nginx/ca.crt --lifetime 3650 --hostname $HOSTNAME --email root@$HOSTNAME
fi

%preun

%postun

%clean

%files
%defattr(0644, awx, awx, 0755)
#%attr(0755, root, root) /usr/bin/awx-manage
%attr(0755, root, root) /usr/lib/systemd/system/*.service
#%attr(0755, root, root) /usr/lib/python%{python3_pkgversion}/site-packages/awx*
#%attr(0755, awx, awx) %{_prefix}
#%dir %attr(0750, %{service_user}, %{service_group}) %{service_homedir}
#%dir %attr(0750, %{service_user}, %{service_group}) %{service_homedir}/venv
#%{service_homedir}/.tower_version
#%dir %attr(0770, %{service_user}, %{service_group}) %{service_logdir}
%config(noreplace) %{service_configdir}/settings.py
%config /etc/nginx/conf.d/awx-rpm.conf
/usr/lib/systemd/system/awx.target
/etc/receptor
#/usr/bin/ansible-tower-service
#/usr/bin/ansible-tower-setup
#/usr/bin/awx-python
#/usr/bin/failure-event-handler
#/usr/share/awx
#/usr/share/sosreport/sos/plugins/tower.py
#/var/lib/awx/favicon.ico
#/var/lib/awx/wsgi.py
/var/lib/awx/rsyslog
/var/lib/awx/projects
/var/lib/awx/job_status

%changelog
* ¤DATE¤ Martin Juhl <m@rtinjuhl.dk> ¤VERSION¤
- New version build: ¤VERSION¤
¤CHANGELOG¤
