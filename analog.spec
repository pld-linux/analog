Summary:	WWW server logfile analysis program
Summary(pl):	Analizator logów serwera www
Name:		analog
Version:	4.03
Release:	1
Copyright:	distributable
Group:		Utilities
Group(pl):	Narzêdzia
Source:		ftp://ftp.nhl.nl/pub/unix/analog/%{name}%{version}.tar.gz
Patch0:		analog-config.patch
Requires:	webserver
URL:		http://www.statslab.cam.ac.uk/~sret1/analog/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WWW server logfile analysis program with lots of features.

%description -l pl
Analizator logów serwera www z wieloma opcjami.

%package form
Summary:	Form interface to analog
Summary(pl):	Interfejs w postaci formularza do analoga
Requires:	%{name} = %{version}
Group:		Utilities
Group(pl):	Narzêdzia

%description form
Form interface to the analog httpd log analysis program.  You should
regenerate the form file to customize it for your server by running
'analog -form +O/home/httpd/html/anlgform.html' after you have
modified /etc/analog.cfg.

%description -l pl form
Interfejs w postaci formularza do programu analog. Powiniene¶
wygenerowaæ nowy plik formularza po ustawieniu odpowiednich
opcji w /etc/analog.cfg poprzez wykonanie komendy:

%prep
%setup -q -n %{name}%{version}
%patch0 -p1

%build
make CEXTRAFLAGS="$RPM_OPT_FLAGS" %{name}

%install
rm -rf $RPM_BUILD_ROOT

install -d	$RPM_BUILD_ROOT/home/httpd/{icons,cgi-bin,html/usage}
install -d	$RPM_BUILD_ROOT%{_var}/state/%{name}
install -d	$RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install -d	$RPM_BUILD_ROOT%{_bindir}
install -d      $RPM_BUILD_ROOT/etc

install -s	analog		$RPM_BUILD_ROOT%{_bindir}
install		analog.cfg	$RPM_BUILD_ROOT/etc/%{name}.cfg
install		lang/*		$RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install		analog.cfg	$RPM_BUILD_ROOT/etc
install		images/*	$RPM_BUILD_ROOT/home/httpd/icons
install		anlgform.html	$RPM_BUILD_ROOT/home/httpd/html/usage
install		anlgform.pl	$RPM_BUILD_ROOT/home/httpd/cgi-bin
touch				$RPM_BUILD_ROOT/home/httpd/html/usage/analog.html

gzip -9nf docs/*.txt lang/*.html
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* lang/*.gz
%attr(755,root,root) %dir %{_datadir}/analog/lang
%attr(755,root,root) %dir %{_datadir}/analog
%attr(775,root,http) %dir /var/state/analog
%config(noreplace) %verify(not size mtime md5) /etc/analog.cfg
%attr(755,root,root) %{_bindir}/analog
%{_datadir}/analog/lang/*.*
/home/httpd/icons/*.gif
%attr(755,root,root) %dir /home/httpd/html/usage
%verify(not size mtime md5) /home/httpd/html/usage/analog.html

%files form
%defattr(644,root,root,755)
%config(noreplace) %verify(not size mtime md5) /home/httpd/html/usage/anlgform.html
%attr(755,root,root) /home/httpd/cgi-bin/anlgform.pl
