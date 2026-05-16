# TODO:
# - /home/services/httpd ? Is it right place?
# - support for webapps
Summary:	WWW server logfile analysis program
Summary(pl.UTF-8):	Analizator logów serwera WWW
Name:		analog
Version:	6.0.18
Release:	1
License:	GPL v2
Group:		Networking/Utilities
#Source0Download:	https://github.com/c-amie/analog-ce/releases
Source0:	https://github.com/c-amie/analog-ce/archive/refs/tags/%{version}.tar.gz
# Source0-md5:	334cfdc27f61797df12f1c40f4b2ce62
Patch0:		%{name}-config.patch
Patch1:		%{name}-system-pcre2.patch
BuildRequires:	pcre2-8-devel
BuildRequires:	pkgconfig
Requires:	webserver
URL:		https://github.com/c-amie/analog-ce
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
%setup -q -n %{name}-ce-%{version}
%patch -P0 -p1
%patch -P1 -p1

%build
%{__make} -C src \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags} $(pkg-config --cflags libpcre2-8)" \
	DEFS="-DHAVE_PCRE" \
	LIBS="$(pkg-config --libs libpcre2-8) -lm"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}/{icons,cgi-bin,html/usage,lang} \
	$RPM_BUILD_ROOT{%{_var}/lib/%{name},%{_bindir},%{_sysconfdir}} \
	$RPM_BUILD_ROOT%{_mandir}/man1

install analog $RPM_BUILD_ROOT%{_bindir}
install analog.cfg-sample $RPM_BUILD_ROOT/etc/%{name}.cfg
install lang/* $RPM_BUILD_ROOT%{_appdir}/lang
install analog.cfg-sample $RPM_BUILD_ROOT%{_sysconfdir}/analog.cfg
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
%attr(755,root,root) %dir %{_appdir}
%attr(775,root,http) %dir %{_var}/lib/%{name}
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) /etc/%{name}.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/analog.cfg
%attr(755,root,root) %{_bindir}/analog
%dir %{_appdir}/lang
%{_appdir}/lang/*.*
%dir %{_appdir}/icons
%{_appdir}/icons/*.css
%{_appdir}/icons/*.gif
%{_appdir}/icons/*.png
%dir %{_appdir}/html
%attr(755,root,root) %dir %{_appdir}/html/usage
%verify(not md5 mtime size) %{_appdir}/html/usage/analog.html
%{_mandir}/man1/*.1*

%files form
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_appdir}/html/usage/anlgform.html
%dir %{_appdir}/cgi-bin
%attr(755,root,root) %{_appdir}/cgi-bin/anlgform.pl
