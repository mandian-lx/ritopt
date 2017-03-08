%{?_javapackages_macros:%_javapackages_macros}

Summary:	An options parser for the Java programming language
Name:		ritopt
Version:	0.2.1
Release:	1
License:	GPL
Group:		Development/Java
URL:		http://ritopt.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-all.tar.gz
Patch0:		%{name}-0.2.1-autoconf.patch
BuildArch:	noarch

BuildRequires:	jpackage-utils
BuildRequires:	java-devel
BuildRequires:	ant
BuildRequires:	texlive

%description
Ritopt is an options parser for the Java programming language

%files
%{_javadir}/*.jar
%doc tut/tutorial.pdf 
%doc README
%doc NEWS
%doc AUTHORS
%doc ChangeLog

#----------------------------------------------------------------------------

%package	javadoc
Summary:	Javadoc for %{name}
Requires:	jpackage-utils

%description javadoc
API documentation for %{name}.

%files javadoc
%{_javadocdir}/%{name}

#----------------------------------------------------------------------------

%prep
%setup -q 
%patch0 -p1 -b .orig

# set package name and version
sed -i -e '{ s|@PACKAGE@|%{name}|g
		s|@VERSION@|%{version}|g
	   }' configure.in

# convert eol to unix
find . -type f -exec sed -i -e 's|\r||g' {} \;

%build
autoreconf -ifv
%configure
%make

# build tutorial (twice so it can build ToC)
pushd tut
pdflatex tutorial.tex
pdflatex tutorial.tex
popd

# fix jar-not-indexed warning
pushd java/
%jar -i %{name}.jar
popd

%install
%make_install

# javadoc
install -dm 0755 %{buildroot}%{_javadocdir}/
cp -r java/doc %{buildroot}%{_javadocdir}/%{name}
rm -f %{buildroot}%{_javadocdir}/ritopt_javadoc

