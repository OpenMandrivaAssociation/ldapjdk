%define spname                ldapsp
%define tar_name        ldapsdk_java
%define tar_version        20020819
%define section                free
%define gcj_support        1

Name:           ldapjdk
Version:        4.18
Release:        %mkrel 0.0.7
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
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

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
%{_javadocdir}/%{name}
%{_javadocdir}/%{name}-%{version}




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:4.18-0.0.5mdv2011.0
+ Revision: 666065
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:4.18-0.0.4mdv2011.0
+ Revision: 606397
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:4.18-0.0.3mdv2010.1
+ Revision: 523161
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:4.18-0.0.2mdv2010.0
+ Revision: 425504
- rebuild

* Mon Nov 24 2008 David Walluck <walluck@mandriva.org> 0:4.18-0.0.1mdv2009.1
+ Revision: 306132
- 4.18

* Wed Dec 26 2007 David Walluck <walluck@mandriva.org> 0:4.17-1.6.0mdv2008.1
+ Revision: 138165
- fix build

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)
    - remove unnecessary Requires(post) on java-gcj-compat


* Tue Dec 12 2006 David Walluck <walluck@mandriva.org> 4.17-1.4mdv2007.0
+ Revision: 95185
- bump release
- Import ldapjdk

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:4.17-1.3mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Fri Jan 13 2006 David Walluck <walluck@mandriva.org> 0:4.17-1.2mdk
- BuildRequires: java-devel

* Sun Sep 11 2005 David Walluck <walluck@mandriva.org> 0:4.17-1.1mdk
- release

* Thu Jan 27 2005 Gary Benson <gbenson@redhat.com> 0:4.17-1jpp_2fc
- Remove non-distributable files from the source tarball.

* Fri Jan 21 2005 Gary Benson <gbenson@redhat.com> 0:4.17-1jpp_1fc
- Build into Fedora.

* Tue Nov 16 2004 Fernando Nasser <fnasser@redhat.com> 0:4.17-1jpp_1rh
- Merge with upstream for upgrade

* Fri Aug 27 2004 Fernando Nasser <fnasser@redhat.com> 0:4.17-1jpp
- Upgrade to 4.17
- Rebuilt with Ant 1.6.2

* Fri Mar 05 2004 Frank Ch. Eigler <fche@redhat.com> 0:4.1-5jpp_1rh
- RH vacuuming
- added ldapjdk-javaxssl.patch to stop using com.sun.*

