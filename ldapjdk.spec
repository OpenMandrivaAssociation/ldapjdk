%define spname		ldapsp
%define tar_name	ldapsdk_java
%define tar_version	20020819
%define section		free
%define gcj_support	1

Name:		ldapjdk
Version:	4.17
Release:	%mkrel 1.6
Epoch:		0
Summary: 	The Mozilla LDAP Java SDK
License:	MPL
Group:		Development/Java
URL:		http://www.mozilla.org/directory/javasdk.html
# This tarball is made by taking the upstream one from
# ftp://ftp.mozilla.org/pub/directory/java-sdk/ and
# deleting mozilla/directory/java-sdk/ldap{jdk,sp}/lib
# as they contain non-distributable jars.
Source0:	%{tar_name}_%{tar_version}_clean.tar.bz2

Requires:	oro
Requires:	jndi
Requires:	jpackage-utils >= 0:1.5
Requires:	jaas
Requires:	jsse
Requires:  	java-sasl
BuildRequires:	oro
BuildRequires:	java-devel
BuildRequires:	jndi
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	jaas
BuildRequires:	jsse
BuildRequires:	jss
BuildRequires:  java-sasl
Provides:	jndi-ldap = 0:1.3.0
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
#Distribution:	JPackage
#Vendor:		JPackage Project

%description
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Obsoletes:      openjmx-javadoc

%description javadoc
Javadoc for %{name}

%prep
%setup -q -c

%build
# cleanup CVS dirs
rm -fr $(find . -name CVS -type d)
# make sure there are no proprietary jars here
[ `find . -name "*.jar" -type f | wc -l` = 0 ] || exit 1
mv mozilla/directory/* .
rm -fr mozilla

cd java-sdk
export JAVA_HOME="%{java_home}"
export CLASSPATH=$(build-classpath oro jndi jaas jss jsse sasl)
export MOZ_SRC=`pwd`
export JAVA_VERSION=1.4
srcpath=ietfldap:ldapfilter:ldapbeans:ldapjdk:ldapsp:tools

# Main jar
%__make -f ldap.mk clean
%__make -f ldap.mk
%__make -f ldap.mk basepackage
%__make -f ldap.mk JAVADOC="%{javadoc} -sourcepath $srcpath" doc

# ldap jdndi service provides
%__make -f ldapsp.mk clean
%__make -f ldapsp.mk
%__make -f ldapsp.mk basepackage
%__make -f ldapsp.mk JAVADOC="%{javadoc} -sourcepath $srcpath" doc

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 java-sdk/dist/packages/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 java-sdk/dist/packages/%{spname}.jar $RPM_BUILD_ROOT%{_javadir}/%{spname}-%{version}.jar

pushd $RPM_BUILD_ROOT%{_javadir}
	for jar in *-%{version}.jar ; do
		ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
	done
popd

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}-1.3.0

pushd $RPM_BUILD_ROOT%{_javadir}-1.3.0
	ln -fs ../java/*%{spname}.jar jndi-ldap.jar
popd

install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -r java-sdk/dist/doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc buildjsdk.txt java-sdk/*.htm
%{_javadir}/%{name}*.jar
%{_javadir}/%{spname}*.jar
%{_javadir}-1.3.0/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*


