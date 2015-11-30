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

#### XXXX DO we need this Makefile ????
srcdir = .
top_srcdir = ..

prefix = /usr/local
exec_prefix = ${prefix}
APXSLDFLAGS=
APXSCFLAGS= -g -O2 -pthread -DHAVE_APR  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/include -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include  -DHAVE_CONFIG_H -DHAVE_JNI
APXSCPPFLAGS=-D_REENTRANT -D_GNU_SOURCE

top_builddir = ..

LIBTOOL = /bin/bash /bottlenecks/rubbos/app/apache2/build/libtool --silent
CC = gcc

OEXT=.lo
include list.mk

JAVA_INCL=-I /bottlenecks/rubbos/app/jdk1.6.0_27/include -I /bottlenecks/rubbos/app/jdk1.6.0_27/include/linux
CFLAGS=-I/bottlenecks/rubbos/app/apache2/include  -DHAVE_CONFIG_H -DHAVE_JNI ${APXSCFLAGS} ${APXSCPPFLAGS} ${JAVA_INCL}

include ../scripts/build/rules.mk

JK=./

all: ${APACHE_OBJECTS}

install:

clean:
	rm -f *.o *.lo *.a *.la *.so *.so.* *.slo
	rm -rf .libs

maintainer-clean: clean
