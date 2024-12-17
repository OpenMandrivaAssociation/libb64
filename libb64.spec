%define major 0
%define libname %mklibname b64
%define devname %mklibname b64 -d

Summary:	A fast encoding/decoding data into and from a base64-encoded format
Name:		libb64
Version:	1.2.1
Release:	2
License:	Public Domain
URL:		https://libb64.sourceforge.net/
Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{version}.zip
# (debian)
Patch0:		bufsiz-as-buffer-size.diff
Patch1:		initialize-coder-state.diff
Patch2:		integer-overflows.diff
Patch3:		no-hardcoded-lib-path.diff
Patch4:		override-cflags.diff
Patch5:		static-chars-per-line.diff
Patch6:		off-by-one.diff
Patch7:		disable-werror.diff
#
Patch8:		libb64-1.2-shared.patch

%description
Base64 uses a subset of displayable ASCII characters, and is therefore a useful
encoding for storing binary data in a text file, such as XML, or sending binary
data over text-only email.

libb64 is a library of ANSI C routines for fast encoding/decoding data into and
from a base64-encoded format. C++ wrappers are included, as well as the source
code for standalone encoding and decoding executables.

%files
%license LICENSE
%doc README
%{_bindir}/%{name}-base64

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	A fast encoding/decoding data into and from a base64-encoded format
Group:		System/Libraries

%description -n %{libname}
Base64 uses a subset of displayable ASCII characters, and is therefore a useful
encoding for storing binary data in a text file, such as XML, or sending binary
data over text-only email.

libb64 is a library of ANSI C routines for fast encoding/decoding data into and
from a base64-encoded format. C++ wrappers are included, as well as the source
code for standalone encoding and decoding executables.

%files -n %{libname}
%license LICENSE
%{_libdir}/%{name}.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	A fast encoding/decoding data into and from a base64-encoded format
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel

%description -n %{devname}
Headers and development files for %{name}.

%files -n %{devname}
%license LICENSE
%doc README TODO
%{_includedir}/b64
%{_libdir}/%{name}.so

#---------------------------------------------------------------------------

%prep
%autosetup -p1

# Remove unneeded flags
#sed -i '/-O3/ d' src/Makefile
#sed -i '/pedantic/ d' src/Makefile


%build
#export CFLAGS="%{optflags} -fPIC"
export LDFLAGS="%ldflags -shared -Wl,-soname,%{name}.so.%{major}"

%set_build_flags
%make_build all_src all_base64

%install
#make-install

# binary, rename to prevent conflict with coreutils binary
install -Dpm 0755 base64/base64 %{buildroot}/%{_bindir}/%{name}-base64

# shared lib
install -Dpm 0755 src/%{name}.so %{buildroot}%{_libdir}/%{name}.so.%{major}
pushd %{buildroot}%{_libdir}/
ln -fs %{name}.so.%{major} %{name}.so
popd

# headers
install -Dpm 0644 -t %{buildroot}/%{_includedir}/b64/ include/b64/*

%check
%set_build_flags
%make_build -C examples test
