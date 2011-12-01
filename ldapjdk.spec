%define spname                ldapsp
%define tar_name        ldapsdk_java
%define tar_version        20020819
%define section                free
%define gcj_support        1

Name:           ldapjdk
Version:        4.18
Release:        %mkrel 0.0.5
Epoch:          0
Summary:        Mozilla LDAP Java SDK
License:        MPL
Group:          Development/Java
URL:            http://www.mozilla.org/directory/javasdk.html
# cvs -d:pserver:anonymous@cvs-mirror.mozilla.org:/cvsroot export -r LDAPJavaSDK_418 DirectorySDKSourceJava
# tar cjf ldapjdk-4.18.tar.bz2 mozilla
Source0:        ldapjdk-4.18.tar.bz2
Requires:       oro
Requires:       jndi
Requires:       jpackage-utils >= 0:1.5
Requires:       jaas
Requires:       jsse
Requires:       java-sasl
BuildRequires:  oro
BuildRequires:  java-devel
BuildRequires:  jndi
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  jaas
BuildRequires:  jsse
BuildRequires:  jss
BuildRequires:  java-sasl
Provides:       jndi-ldap = 0:1.3.0
Provides:       ldapsdk = %{epoch}:%{version}-%{release}
Obsoletes:      ldapsdk < %{epoch}:%{version}-%{release}
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Mozilla LDAP SDKs enable you to write applications which access,
manage, and update the information stored in an LDAP directory.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Obsoletes:      openjmx-javadoc < %{epoch}:%{version}-%{release}

%description javadoc
Javadoc for %{name}

%prep
%setup -q -c

%build
find . -type f -name "*.jar" | xargs -t rm
mv mozilla/directory/* .
rm -rf mozilla

cd java-sdk
export JAVA_HOME="%{java_home}"
export CLASSPATH=$(build-classpath oro jndi jaas jss jsse sasl)
export MOZ_SRC=`pwd`
export JAVA_VERSION=1.5
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
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_javadir}
install -m 644 java-sdk/dist/packages/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
install -m 644 java-sdk/dist/packages/%{spname}.jar %{buildroot}%{_javadir}/%{spname}-%{version}.jar

pushd %{buildroot}%{_javadir}
        for jar in *-%{version}.jar ; do
                ln -fs ${jar} $(echo $jar | sed "s|-%{version}.jar|.jar|g")
        done
popd

install -d -m 755 %{buildroot}%{_javadir}-1.3.0

pushd %{buildroot}%{_javadir}-1.3.0
        ln -fs ../java/*%{spname}.jar jndi-ldap.jar
popd

install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -r java-sdk/dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

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
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}


