#!/usr/bin/env python
# Set up build environment on Ubuntu or other Debian-based
# Linux distribution.

import platform, re
from bootstrap import *
from subprocess import check_call, Popen, PIPE

bootstrap_init()

# Install build tools.
check_call(['apt-get', 'update'])
packages = [
  'git-core', 'gcc', 'g++', 'gfortran', 'ccache', 'make',
  'python-dev', 'default-jdk', 'unixodbc-dev'
]
x86_64 = platform.machine() == 'x86_64'
if x86_64:
  packages.append('libc6-i386')
check_call(['apt-get', 'install', '-y'] + packages)

install_cmake('cmake-2.8.12.2-Linux-i386.tar.gz')

# Installs symlinks for ccache.
for name in ['gcc', 'cc', 'g++', 'c++']:
  add_to_path(which('ccache'), name)

install_f90cache()
output = Popen(['gfortran', '--version'], stdout=PIPE).communicate()[0]
version = re.match(r'.* (\d+\.\d+)\.\d+', output).group(1)
add_to_path('/usr/local/bin/f90cache', 'gfortran-' + version)

copy_optional_dependencies('linux-' + platform.machine())
install_buildbot_slave('lucid64' if x86_64 else 'lucid32')
