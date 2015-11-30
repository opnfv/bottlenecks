

INCLUDES = -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include/private  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/include  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/xml/expat/lib

TARGETS = xlate.lo
CLEAN_TARGETS = xlate

SUBDIRS = @APR_ICONV_SUBDIRS@

# bring in rules.mk for standard functionality
include /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/build/rules.mk
