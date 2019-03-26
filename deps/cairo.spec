%define fontconfig_version 2.8.0
%define freetype_version 2.3.12
%define glib2_version 2.22.5
%define libpng_version 1.2.46
%define librsvg2_version 2.26.0-3
%define libxml2_version 2.6.32-2
%define libXrender_version 0.9.5
%define pixman_version 0.22.0

Summary:	A vector graphics library
Name:		cairo
Version:	1.16.0
Release:	1
URL:		https://www.cairographics.org
Source0:	https://www.cairographics.org/releases/%{name}-%{version}.tar.xz
Source1:	https://www.cairographics.org/releases/%{name}-%{version}.tar.xz.sha1
Source2:	https://www.cairographics.org/releases/%{name}-%{version}.tar.xz.sha1.asc
# Patch0:		%{name}-%{version}-aix.patch
License:	LGPL/MPL
Group:		System Environment/Libraries
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: bash, autoconf, automake, libtool, xz
# Implied xcb dependency? 
BuildRequires: expat-devel
BuildRequires: fontconfig-devel >= %{fontconfig_version}
BuildRequires: freetype-devel >= %{freetype_version}
# BuildRequires: gcc >= 4.2.3-2
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: libpng-devel >= %{libpng_version}
# BuildRequires: librsvg2-devel >= %{librsvg2_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
# BuildRequires: libXrender-devel >= %{libXrender_version}
BuildRequires: pixman-devel >= %{pixman_version}
BuildRequires: pkg-config
BuildRequires: zlib-devel
BuildRequires: lzo-devel

Requires: fontconfig >= %{fontconfig_version}
Requires: libfreetype6 >= %{freetype_version}
Requires: libglib-2_0-0 >= %{glib2_version}
Requires: libgobject-2_0-0 >= %{glib2_version}
# Requires: libgcc >= 4.2.3-2
Requires: libpng >= %{libpng_version}
# Requires: librsvg2 >= %{librsvg2_version}
Requires: libxml2 >= %{libxml2_version}
# Requires: libXrender >= %{libXrender_version}
Requires: pixman >= %{pixman_version}
Requires: zlib
Requires: lzo
Requires: libexpat1

%description 
Cairo is a vector graphics library designed to provide high-quality
display and print output. Currently supported output targets include
the X Window System, OpenGL (via glitz), in-memory image buffers, and
image files (PDF, PostScript, and SVG).  Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available (e.g. through the X Render
Extension or OpenGL).

%package devel
Summary: Cairo developmental libraries and header files
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config
Requires: expat-devel
Requires: fontconfig-devel >= %{fontconfig_version}
Requires: freetype-devel >= %{freetype_version}
Requires: glib2-devel >= %{glib2_version}
Requires: libpng-devel >= %{libpng_version}
Requires: libxml2-devel >= %{libxml2_version}
# Requires: libXrender-devel >= %{libXrender_version}
Requires: pixman-devel >= %{pixman_version}
Requires: zlib-devel
BuildRequires: lzo-devel

%description devel
Developmental libraries and header files required for developing or
compiling software which links to the cairo graphics library, which is
an open source vector graphics library.

%prep
%setup -q
#%patch0

%build

export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

# XXX: What's Perzl's logic here?
export CFLAGS="-DDISABLE_SOME_FLOATING_POINT -D_ALL_SOURCE -DFUNCPROTO=15 -pthread"

autoreconf -fiv

# Some dependencies are disabled due to hairy dependency chains.
# * --enable-svg=yes \  # librsvg <= 2.40 dependency chain
# * --enable-xlib=yes \ # Building without X11 due to limited use
#                       # (but we can always reconsider it)
# * --enable-xcb=no \
# * --enable-xlib-xrender=yes \ # need fd.o/x.org Xrender in place of IBM's
# ax_cv_c_float_words_bigendian=yes is because the test is busted in autotools
%configure \
    LDFLAGS="-maix${OBJECT_MODE} -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static \
    --enable-svg=no \
    --enable-xlib=no \
    --enable-xlib-xrender=no \
    --enable-xcb=no \
    --enable-png=yes \
    --enable-ps=yes \
    --enable-pdf=yes \
    --enable-pthread=yes \
    --disable-some-floating-point \
    --disable-gtk-doc \
    ax_cv_c_float_words_bigendian=yes
%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc AUTHORS BIBLIOGRAPHY BUGS ChangeLog COPYING
%doc COPYING-LGPL-2.1 COPYING-MPL-1.1 NEWS
%doc PORTING_GUIDE README
%{_libdir}/libcairo-script-interpreter.so.2
%{_libdir}/libcairo-gobject.so.2
%{_libdir}/libcairo.so.2

%files devel
%defattr(-, qsys, *none)
%{_includedir}/cairo/*.h
%{_libdir}/libcairo-script-interpreter.so
%{_libdir}/libcairo-gobject.so
%{_libdir}/libcairo.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/cairo/*


%changelog
* Tue Mar 26 2019 Calvin Buckley <calvin@cmpct.info> - 1.16.0-1
- Upgrade to 1.16.0 (some tests failing)
- De-AIX, Rochester conventions
- Disabled X11 and SVG support due to dependency chain problems

* Fri Feb 01 2013 Michael Perzl <michael@perzl.org> - 1.10.2-3
- added missing 64-bit shared members of libcairo-gobject.a and
  libcairo-script-interpreter.a

* Mon Aug 20 2012 Michael Perzl <michael@perzl.org> - 1.10.2-2
- had to switch from IBM XL C/C++ to GCC now as otherwise cairo is miscompiled

* Sun Nov 20 2011 Michael Perzl <michael@perzl.org> - 1.10.2-1
- updated to version 1.10.2

* Sun Nov 20 2011 Michael Perzl <michael@perzl.org> - 1.10.0-1
- updated to version 1.10.0
- added RTL-style shared libraries

* Fri Feb 26 2010 Michael Perzl <michael@perzl.org> - 1.8.10-1
- updated to version 1.8.10

* Wed Jun 24 2009 Michael Perzl <michael@perzl.org> - 1.8.8-1
- updated to version 1.8.8

* Wed Dec 17 2008 Michael Perzl <michael@perzl.org> - 1.8.6-1
- updated to version 1.8.6

* Thu Nov 20 2008 Michael Perzl <michael@perzl.org> - 1.8.4-1
- updated to version 1.8.4

* Sat Nov 01 2008 Michael Perzl <michael@perzl.org> - 1.8.2-1
- updated to version 1.8.2

* Wed Oct 22 2008 Michael Perzl <michael@perzl.org> - 1.8.0-1
- updated to version 1.8.0

* Fri Jul 04 2008 Michael Perzl <michael@perzl.org> - 1.6.4-1
- updated to version 1.6.4

* Sat Apr 05 2008 Michael Perzl <michael@perzl.org> - 1.4.14-1
- first version for AIX V5.1 and higher
