Summary:	WWW server logfile analysis program
Summary(pl):	Analizator log�w serwera www
Name:		analog
Version:	5.32
Release:	1
License:	distributable
Group:		Networking/Utilities
#Source0Download:	http://www.analog.cx/download.html
Source0:	http://www.analog.cx/%{name}-%{version}.tar.gz
# Source0-md5:	077a2d43c8f5c2bddf37129ca63ec1f8
Patch0:		%{name}-config.patch
Patch1:		%{name}-png.patch
Requires:	webserver
URL:		http://www.analog.cx/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WWW server logfile analysis program with lots of features.

%description -l pl
Analizator log�w serwera www z wieloma opcjami.

%package form
Summary:	Form interface to analog
Summary(pl):	Interfejs w postaci formularza do analoga
Group:		Networking/Utilities
Requires:	%{name} = %{version}

%description form
Form interface to the analog httpd log analysis program. You should
regenerate the form file to customize it for your server by running
'analog -form +O/home/httpd/html/anlgform.html' after you have
modified /etc/analog.cfg.

%description form -l pl
Interfejs w postaci formularza do programu analog. Powiniene�
wygenerowa� nowy plik formularza po ustawieniu odpowiednich opcji w
/etc/analog.cfg poprzez wykonanie polecenia: 'analog -form
+O/home/httpd/html/anlgform.html'

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
%{__make} %{name} \
	CFLAGS="%{rpmcflags}" \
	CEXTRAFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/home/httpd/{icons,cgi-bin,html/usage} \
	$RPM_BUILD_ROOT{%{_var}/lib/%{name},%{_datadir}/%{name}/lang} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir}}

install analog $RPM_BUILD_ROOT%{_bindir}
install analog.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg
install lang/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install analog.cfg $RPM_BUILD_ROOT%{_sysconfdir}
install images/* $RPM_BUILD_ROOT/home/httpd/icons
install anlgform.html $RPM_BUILD_ROOT/home/httpd/html/usage
install anlgform.pl $RPM_BUILD_ROOT/home/httpd/cgi-bin

touch $RPM_BUILD_ROOT/home/httpd/html/usage/analog.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* lang/*
%attr(755,root,root) %dir %{_datadir}/analog/lang
%attr(755,root,root) %dir %{_datadir}/analog
%attr(775,root,http) %dir /var/lib/analog
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/analog.cfg
%attr(755,root,root) %{_bindir}/analog
%{_datadir}/analog/lang/*.*
/home/httpd/icons/*.gif
%attr(755,root,root) %dir /home/httpd/html/usage
%verify(not size mtime md5) /home/httpd/html/usage/analog.html

%files form
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) /home/httpd/html/usage/anlgform.html
%attr(755,root,root) /home/httpd/cgi-bin/anlgform.pl
