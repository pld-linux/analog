# TODO:
# - /home/services/httpd ? Is it right place?
Summary:	WWW server logfile analysis program
Summary(pl):	Analizator logów serwera WWW
Name:		analog
Version:	6.0
Release:	2
License:	GPL v2
Group:		Networking/Utilities
#Source0Download:	http://www.analog.cx/download.html
Source0:	http://www.analog.cx/%{name}-%{version}.tar.gz
# Source0-md5:	743d03a16eb8c8488205ae63cdb671cd
Patch0:		%{name}-config.patch
Requires:	webserver
URL:		http://www.analog.cx/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		httpdir	/home/services/httpd

%description
WWW server logfile analysis program with lots of features.

%description -l pl
Analizator logów serwera WWW z wieloma opcjami.

%package form
Summary:	Form interface to analog
Summary(pl):	Interfejs w postaci formularza do analoga
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description form
Form interface to the analog httpd log analysis program. You should
regenerate the form file to customize it for your server by running
'analog -form +O%{httpdir}/html/anlgform.html'
after you have modified /etc/analog.cfg.

%description form -l pl
Interfejs w postaci formularza do programu analog. Powiniene¶
wygenerowaæ nowy plik formularza po ustawieniu odpowiednich opcji w
/etc/analog.cfg poprzez wykonanie polecenia:
'analog -form +O%{httpdir}/html/anlgform.html'

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
install -d $RPM_BUILD_ROOT%{httpdir}/{icons,cgi-bin,html/usage} \
	$RPM_BUILD_ROOT{%{_var}/lib/%{name},%{_datadir}/%{name}/lang} \
	$RPM_BUILD_ROOT{%{_bindir},%{_sysconfdir},%{_mandir}/man1}

install analog $RPM_BUILD_ROOT%{_bindir}
install analog.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.cfg
install lang/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install analog.cfg $RPM_BUILD_ROOT%{_sysconfdir}
install images/* $RPM_BUILD_ROOT%{httpdir}/icons
install anlgform.html $RPM_BUILD_ROOT%{httpdir}/html/usage
install anlgform.pl $RPM_BUILD_ROOT%{httpdir}/cgi-bin
install analog.man $RPM_BUILD_ROOT%{_mandir}/man1/analog.1

touch $RPM_BUILD_ROOT%{httpdir}/html/usage/analog.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* lang/* examples how-to
%attr(755,root,root) %dir %{_datadir}/analog/lang
%attr(755,root,root) %dir %{_datadir}/analog
%attr(775,root,http) %dir /var/lib/analog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/analog.cfg
%attr(755,root,root) %{_bindir}/analog
%{_datadir}/analog/lang/*.*
%{httpdir}/icons/*.gif
%{httpdir}/icons/*.png
%attr(755,root,root) %dir %{httpdir}/html/usage
%verify(not md5 mtime size) %{httpdir}/html/usage/analog.html
%{_mandir}/man1/*.1*

%files form
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{httpdir}/html/usage/anlgform.html
%attr(755,root,root) %{httpdir}/cgi-bin/anlgform.pl
