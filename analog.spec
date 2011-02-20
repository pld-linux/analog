# TODO:
# - /home/services/httpd ? Is it right place?
# - support for webapps
Summary:	WWW server logfile analysis program
Summary(pl.UTF-8):	Analizator logów serwera WWW
Name:		analog
Version:	6.0
Release:	4
License:	GPL v2
Group:		Networking/Utilities
#Source0Download:	http://www.analog.cx/download.html
Source0:	http://www.analog.cx/%{name}-%{version}.tar.gz
# Source0-md5:	743d03a16eb8c8488205ae63cdb671cd
Patch0:		%{name}-config.patch
Requires:	webserver
URL:		http://www.analog.cx/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _appdir         %{_datadir}/%{name}
%define         _webapps        /etc/webapps
%define         _webapp         %{name}
%define         _sysconfdir     %{_webapps}/%{_webapp}

%description
WWW server logfile analysis program with lots of features.

%description -l pl.UTF-8
Analizator logów serwera WWW z wieloma opcjami.

%package form
Summary:	Form interface to analog
Summary(pl.UTF-8):	Interfejs w postaci formularza do analoga
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description form
Form interface to the analog httpd log analysis program. You should
regenerate the form file to customize it for your server by running
'analog -form +O%{_appdir}/html/anlgform.html'
after you have modified /etc/analog.cfg.

%description form -l pl.UTF-8
Interfejs w postaci formularza do programu analog. Powinieneś
wygenerować nowy plik formularza po ustawieniu odpowiednich opcji w
/etc/analog.cfg poprzez wykonanie polecenia:
'analog -form +O%{_appdir}/html/anlgform.html'

%prep
%setup  -q
%patch0 -p1

%build
%{__make} %{name} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	CEXTRAFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}/{icons,cgi-bin,html/usage,lang} \
	$RPM_BUILD_ROOT{%{_var}/lib/%{name},%{_bindir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_mandir}/man1

install analog $RPM_BUILD_ROOT%{_bindir}
install analog.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg
install lang/* $RPM_BUILD_ROOT%{_appdir}/lang
install analog.cfg $RPM_BUILD_ROOT%{_sysconfdir}
install images/* $RPM_BUILD_ROOT%{_appdir}/icons
install anlgform.html $RPM_BUILD_ROOT%{_appdir}/html/usage
install anlgform.pl $RPM_BUILD_ROOT%{_appdir}/cgi-bin
install analog.man $RPM_BUILD_ROOT%{_mandir}/man1/analog.1

touch $RPM_BUILD_ROOT%{_appdir}/html/usage/analog.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* lang/* examples how-to
%attr(755,root,root) %dir %{_appdir}/lang
%attr(755,root,root) %dir %{_appdir}
%attr(775,root,http) %dir %{_var}/lib/%{name}
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.cfg
%attr(755,root,root) %{_bindir}/analog
%dir %{_appdir}/lang
%{_appdir}/lang/*.*
%dir %{_appdir}/icons
%{_appdir}/icons/*.gif
%{_appdir}/icons/*.png
%attr(755,root,root) %dir %{_appdir}/html/usage
%verify(not md5 mtime size) %{_appdir}/html/usage/analog.html
%{_mandir}/man1/*.1*

%files form
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_appdir}/html/usage/anlgform.html
%dir %{_appdir}/cgi-bin
%attr(755,root,root) %{_appdir}/cgi-bin/anlgform.pl
