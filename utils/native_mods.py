# -*- coding: utf-8 -*-
#
#   Native modules build
#
# 	Copyright (C) 2015-2018 by Ihor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import platform

from . import build
from . import pkgconfig

from setuptools import Extension


def make_modules(src_path, include_path, lib_path=None):
    if lib_path is None:
        lib_path = []
        
    if os.name == 'nt':
        include_path = 'C:/vcpkg/installed/x64-windows/include'
        lib_path.append('C:/vcpkg/installed/x64-windows/lib')
        
    modules = []

    # --- Cairo module

    cairo_src = os.path.join(src_path, 'uc2', 'libcairo')
    files = build.make_source_list(cairo_src, ['_libcairo.c', ])

    include_dirs = []
    cairo_libs = ['cairo']

    if os.name == 'nt':
        try:
            import cairo
            pycairo_inc = cairo.get_include()
        except ImportError:
            pycairo_inc = ''
        include_dirs = [include_path, include_path + '/cairo', pycairo_inc]
        cairo_libs = ['cairo']
    elif platform.system() == 'Darwin':
        include_dirs = pkgconfig.get_pkg_includes(['pycairo', 'cairo'])
        cairo_libs = pkgconfig.get_pkg_libs(['pycairo', 'cairo'])
    elif os.name == 'posix':
        include_dirs = pkgconfig.get_pkg_includes(['pycairo', ])
        cairo_libs = pkgconfig.get_pkg_libs(['pycairo', ])

    cairo_module = Extension(
        'uc2.libcairo._libcairo',
        define_macros=[('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
        sources=files, include_dirs=include_dirs,
        library_dirs=lib_path,
        libraries=cairo_libs)
    modules.append(cairo_module)

    # --- LCMS2 module

    pycms_files = ['_cms2.c', ]
    pycms_libraries = []
    extra_compile_args = []

    if os.name == 'nt':
        pycms_libraries = ['lcms2']
        include_dirs = [include_path, ]
    elif os.name == 'posix':
        pycms_libraries = pkgconfig.get_pkg_libs(['lcms2', ])
        extra_compile_args = ["-Wall"]
        include_dirs = [include_path, ]

    pycms_src = os.path.join(src_path, 'uc2', 'cms')
    files = build.make_source_list(pycms_src, pycms_files)
    pycms_module = Extension(
        'uc2.cms._cms',
        define_macros=[('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
        sources=files, include_dirs=include_dirs,
        library_dirs=lib_path,
        libraries=pycms_libraries,
        extra_compile_args=extra_compile_args)
    modules.append(pycms_module)

    # --- Pango module

    pango_src = os.path.join(src_path, 'uc2', 'libpango')
    files = build.make_source_list(pango_src, ['_libpango.c', ])
    pango_libs = [
        'pango-1.0', 'pangocairo-1.0', 'cairo', 'glib-2.0', 'gobject-2.0']

    if os.name == 'nt':
        include_dirs = [include_path, include_path + '/cairo', include_path + '/pango-1.0', include_path + '/glib-2.0']
        try:
            import cairo
            include_dirs.append(cairo.get_include())
        except: pass
    elif platform.system() == 'Darwin':
        include_dirs = pkgconfig.get_pkg_includes(['pangocairo', 'pango',
                                                   'pycairo', 'cairo'])
        pango_libs = pkgconfig.get_pkg_libs(['pangocairo', 'pango', 'pycairo',
                                             'cairo'])
    elif os.name == 'posix':
        include_dirs = pkgconfig.get_pkg_includes(['pangocairo', 'pycairo'])
        pango_libs = pkgconfig.get_pkg_libs(['pangocairo', ])

    pango_module = Extension(
        'uc2.libpango._libpango',
        define_macros=[('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
        sources=files, include_dirs=include_dirs,
        library_dirs=lib_path,
        libraries=pango_libs)
    modules.append(pango_module)

    # --- ImageMagick module

    compile_args = []
    libimg_libraries = ['CORE_RL_wand_', 'CORE_RL_magick_']
    im_ver = '6'

    if os.name == 'nt':
        include_dirs = [include_path, include_path + '/ImageMagick-6', include_path + '/ImageMagick']
        # Try MagickWand/MagickCore names commonly used by vcpkg
        libimg_libraries = ['MagickWand', 'MagickCore', 'CORE_RL_wand_', 'CORE_RL_magick_']
    elif os.name == 'posix':
        im_ver = pkgconfig.get_pkg_version('MagickWand')[0]
        libimg_libraries = pkgconfig.get_pkg_libs(['MagickWand', ])
        include_dirs = pkgconfig.get_pkg_includes(['MagickWand', ])
        compile_args = pkgconfig.get_pkg_cflags(['MagickWand', ])

    libimg_src = os.path.join(src_path, 'uc2', 'libimg')
    files = build.make_source_list(libimg_src, ['_libimg%s.c' % im_ver, ])
    libimg_module = Extension(
        'uc2.libimg._libimg',
        define_macros=[('MAJOR_VERSION', '1'), ('MINOR_VERSION', '0')],
        sources=files, include_dirs=include_dirs,
        library_dirs=lib_path,
        libraries=libimg_libraries,
        extra_compile_args=compile_args)
    modules.append(libimg_module)

    return modules
