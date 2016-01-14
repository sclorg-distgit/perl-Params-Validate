%{?scl:%scl_package perl-Params-Validate}
%{!?scl:%global pkg_name %{name}}

# Supported rpmbuild options:
#
# --with network/--without network
#    include/exclude networked tests, which work in mock, but don't work in koji
#    Default: --without (Exclude tests, which don't work in koji)
%bcond_with	network

# --with release-tests/--without release-tests
#    Default: --with (--without when bootstrapping)
%if 0%{?perl_bootstrap} || 0%{?scl:1}
%bcond_with	release_tests
%else
%bcond_without	release_tests
%endif

Summary: 	Params-Validate Perl module
Name: 		%{?scl_prefix}perl-Params-Validate
Version: 	1.08
Release: 	7%{?dist}
License: 	Artistic 2.0
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Params-Validate/
Source0: 	http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/Params-Validate-%{version}.tar.gz

# Hacks to make spell checking tests work with hunspell
Patch0:         Params-Validate-1.08.diff

%{?scl:%global perl_version %(scl enable %{scl} 'eval "`%{__perl} -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`%{__perl} -V:version`"; echo $version)}
Requires:  	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})

BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(Module::Implementation) >= 0.04
BuildRequires:  %{?scl_prefix}perl(Module::Build) >= 0.37

# Run-time:
BuildRequires:  %{?scl_prefix}perl(Attribute::Handlers) >= 0.79
BuildRequires:  %{?scl_prefix}perl(Exporter)
BuildRequires:  %{?scl_prefix}perl(Scalar::Util) >= 1.10
BuildRequires:  %{?scl_prefix}perl(XSLoader)

# Required by the tests
BuildRequires:  %{?scl_prefix}perl(base)
BuildRequires:  %{?scl_prefix}perl(Devel::Peek)
BuildRequires:  %{?scl_prefix}perl(File::Spec)
BuildRequires:  %{?scl_prefix}perl(File::Temp)
BuildRequires:  %{?scl_prefix}perl(lib)
BuildRequires:  %{?scl_prefix}perl(Test::Fatal)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.88
BuildRequires:  %{?scl_prefix}perl(Test::Taint) >= 0.02
BuildRequires:  %{?scl_prefix}perl(Tie::Array)
BuildRequires:  %{?scl_prefix}perl(Tie::Hash)
BuildRequires:  %{?scl_prefix}perl(Readonly)
BuildRequires:  %{?scl_prefix}perl(Readonly::XS)

%if %{with release_tests}
# For release testing tests
BuildRequires:	%{?scl_prefix}perl(Test::CPAN::Changes)
BuildRequires:	%{?scl_prefix}perl(Test::EOL)
BuildRequires:	%{?scl_prefix}perl(Test::NoTabs)
BuildRequires:	%{?scl_prefix}perl(Test::Pod) >= 1.41
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage) >= 1.04
BuildRequires:  %{?scl_prefix}perl(Test::Pod::LinkCheck)
BuildRequires:  %{?scl_prefix}perl(Test::Pod::No404s)
BuildRequires:  %{?scl_prefix}perl(LWP::Protocol::https)
BuildRequires:	%{?scl_prefix}perl(Test::Spelling)
BuildRequires:  %{?scl_prefix}hunspell-en
%endif

%{?perl_default_filter}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_from_provides /\.so()/d
%filter_setup
%endif

%description
The Params::Validate module allows you to validate method or function
call parameters to an arbitrary level of specificity. At the simplest
level, it is capable of validating the required parameters were given
and that no unspecified additional parameters were passed in. It is
also capable of determining that a parameter is of a specific type,
that it is an object of a certain class hierarchy, that it possesses
certain methods, or applying validation callbacks to arguments.

%prep
%setup -q -n Params-Validate-%{version}
%patch0 -p1
sed -i -e "s,set_spell_cmd(.*),set_spell_cmd(\'hunspell -l\')," t/release-pod-spell.t

%build
%{?scl:scl enable %{scl} '}
%{__perl} Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
%{?scl:'}
%{?scl:scl enable %{scl} "}
./Build
%{?scl:"}


%install
%{?scl:scl enable %{scl} "}
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{?scl:"}
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} $RPM_BUILD_ROOT/*

%check
%{?scl:scl enable %{scl} "}
%{?with_release_tests:RELEASE_TESTING=1} %{!?with_network:SKIP_POD_NO404S=1} ./Build test
%{?scl:"}


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README TODO
%{perl_vendorarch}/Params
%{perl_vendorarch}/auto/Params
%{perl_vendorarch}/Attribute
%{_mandir}/man3/*

%changelog
* Thu Nov 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-7
- Rebuilt for SCL

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1.08-6
- Perl 5.18 re-rebuild of bootstrapped packages

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 1.08-4
- Perl 5.18 rebuild

* Thu Jul 18 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-3
- Adjust license tag (RHBZ #977787).

* Thu Jul 18 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-2
- Add %%bcond --without release-tests.
- Skip release tests when bootstrapping (RHBZ #982253).

* Tue Jun 11 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.08-1
- Upstream update.
- Update patch.
- Update BRs.
- Add %%bcond --with network.
- Fix up %%changelog dates.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.07-1
- Upstream update.

* Tue Aug 14 2012 Petr Pisar <ppisar@redhat.com> - 1.06-5
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.06-3
- Perl 5.16 rebuild

* Thu May 31 2012 Petr Pisar <ppisar@redhat.com> - 1.06-2
- Round Module::Build version to 2 digits

* Mon Mar 19 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.06-1
- Upstream update.

* Thu Feb 09 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.05-1
- Upstream update.

* Mon Feb 06 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.01-1
- Upstream update.
- Drop Params-Validate-1.00-no-pod-coverage.patch.
- Spec file cleanup.

* Sun Jan 22 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.00-5
- Add %%{perl_default_filter}.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.00-3
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.00-2
- Perl mass rebuild

* Thu Jun 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.00-1
- Upstream update.
- Deactivate t/release-pod-coverage.t 
  (Add Params-Validate-1.00-no-pod-coverage.patch).

* Thu Jun 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.99-3
- Fix up bogus Tue Jun 28 2011 changelog entry.
- Fix License (Artistic2.0).
- Add BR: perl(Test::CPAN:Changes).

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.99-2
- Perl mass rebuild
- remove unneeded Pod::Man 

* Tue May 31 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.99-1
- Upstream update.
- Rebase patch (Params-Validate-0.99.diff).

* Sat Apr 30 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.98-1
- Upstream update.
- Spec cleanup.
- Rework BR's.
- Reflect upstream having abandoned AUTHOR_TESTING.
- Make spell-checking tests working/work-around aspell/hunspell/perl(Test::Spelling)
  issues (add Params-Validate-0.98.diff).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.95-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.95-2
- Mass rebuild with perl-5.12.0

* Wed Mar 03 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.95-1
- Upstream update.

* Tue Dec 15 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.94-1
- Upstream update.
- Reflect upstream having reworked author tests to using AUTHOR_TESTING=1.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.92-2
- rebuild against perl 5.10.1

* Mon Nov 23 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.92-1
- Upstream update.
- Switch to Build.PL.
- Disable IS_MAINTAINER test.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jun 10 2008 Ralf Corsépius <rc040203@freenet.de> - 0.91-1
- Upstream update.
- Conditionally activate IS_MAINTAINER tests.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.89-4
- Rebuild for perl 5.10 (again)

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 0.89-3
- Rebuild for gcc43.

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.89-2
- rebuild for new perl

* Tue Nov 13 2007 Ralf Corsépius <rc040203@freenet.de> - 0.89-1
- Upstream update.

* Thu Sep 06 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-3
- Update license tag.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-2
- Mass rebuild.

* Mon Mar 12 2007 Ralf Corsépius <rc040203@freenet.de> - 0.88-1
- BR: perl(ExtUtils::MakeMaker).
- Upstream update.

* Sat Jan 20 2007 Ralf Corsépius <rc040203@freenet.de> - 0.87-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.86-2
- Mass rebuild.

* Sun Aug 13 2006 Ralf Corsépius <rc040203@freenet.de> - 0.86-1
- Upstream update.

* Wed Jun 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.85-1
- Upstream update.

* Mon Jun 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.84-1
- Upstream update.

* Sun May 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.82-1
- Upstream update.

* Tue Apr 04 2006 Ralf Corsépius <rc040203@freenet.de> - 0.81-1
- Upstream update.

* Mon Feb 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.80-2
- Rebuild.

* Wed Feb 01 2006 Ralf Corsépius <rc040203@freenet.de> - 0.80-1
- Upstream update.

* Sat Jan 14 2006 Ralf Corsépius <rc040203@freenet.de> - 0.79-1
- Upstream update.
- BR perl(Readonly), perl(Readonly::XS).

* Sun Aug 14 2005 Ralf Corsepius <ralf@links2linux.de> - 0.78-2
- Spec file cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.78-1
- FE submission.
