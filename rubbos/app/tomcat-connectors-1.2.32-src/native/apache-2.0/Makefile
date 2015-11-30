# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

##

APXS=/bottlenecks/rubbos/app/apache2/bin/apxs
OS=linux
JAVA_HOME=/bottlenecks/rubbos/app/jdk1.6.0_27
CP=/bin/cp
APACHE_DIR=/bottlenecks/rubbos/app/apache2
MKDIR=/bin/mkdir
APXSCFLAGS= -g -O2 -pthread -DHAVE_APR  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/include -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include  -DHAVE_CONFIG_H -DHAVE_JNI
APXSCPPFLAGS=-D_REENTRANT -D_GNU_SOURCE
APXSLDFLAGS=
CC=gcc

# Defaults
libexecdir=${APACHE_DIR}/modules

JK=../common/
# Defines APACHE_OBJECTS - the list of all common files
include ../common/list.mk

# Apache2 settings, values guessed by Apache config and used to build it
# Will define libexecdir, LIBTOOL, etc
include /bottlenecks/rubbos/app/apache2/build/config_vars.mk

# Local settings ( overriding/appending to Apache's )
COMMON=../common
JK_INCL=-DUSE_APACHE_MD5 -I ${COMMON}
JAVA_INCL=-I ${JAVA_HOME}/include -I ${JAVA_HOME}/include/${OS}
JAVA_LIB=-L ${JAVA_HOME}/jre/lib/${ARCH} -L ${JAVA_HOME}/lib/${ARCH}/native_threads
CFLAGS=-I/bottlenecks/rubbos/app/apache2/include  -DHAVE_CONFIG_H -DHAVE_JNI ${JK_INCL} ${JAVA_INCL} ${APXSCPPFLAGS} ${APXSCFLAGS} ${EXTRA_CFLAGS} ${EXTRA_CPPFLAGS}


# Implicit rules
include ../scripts/build/rules.mk

OEXT=.lo

all: Makefile mod_jk.so
install: install_dynamic

Makefile: Makefile.in
	echo Regenerating Makefile
	( cd ..; ./config.status )

lib_jk.la: mod_jk.lo ${APACHE_OBJECTS}
	$(LIBTOOL) --mode=link $(CC) -o lib_jk.la -static -rpath ${libexecdir}/jk mod_jk.lo $(APACHE_OBJECTS)

install_static:
	@echo ""
	@echo "Copying files to Apache Modules Directory..."
	-${MKDIR} ${APACHE_DIR}/modules/jk
	${CP} config.m4 ${APACHE_DIR}/modules/jk
	${LIBTOOL} --mode=install cp lib_jk.la ${APACHE_DIR}/modules/jk
	@echo ""
	@echo "Please be sure to re-compile Apache..."
	@echo ""
	@echo "cd ${APACHE_DIR}"
	@echo "./buildconf"
	@echo "./configure --with-mod_jk"
	@echo "make"
	@echo ""

#################### Dynamic .so file ####################
# APXS will compile every file, this is derived from apxs

mod_jk.la: mod_jk.lo $(APACHE_OBJECTS)
	$(LIBTOOL) --mode=link ${COMPILE} $(APXSLDFLAGS) -o $@ -module -rpath ${libexecdir} -avoid-version mod_jk.lo $(APACHE_OBJECTS)

mod_jk.so: mod_jk.la
	../scripts/build/instdso.sh SH_LIBTOOL='$(LIBTOOL)' mod_jk.la `pwd`

install_dynamic:
	@echo ""
	@echo "Installing files to Apache Modules Directory..."
	$(APXS) -i mod_jk.la
	@echo ""
	@echo "Please be sure to arrange ${APACHE_DIR}/conf/httpd.conf..."
	@echo ""

clean:
	rm -f *.o *.lo *.a *.la *.so *.so.* *.slo
	rm -rf .libs

maintainer-clean: clean
