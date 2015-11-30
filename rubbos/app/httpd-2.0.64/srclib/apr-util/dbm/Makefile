

INCLUDES = -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include/private  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/include  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/xml/expat/lib

TARGETS = apr_dbm.lo apr_dbm_berkeleydb.lo apr_dbm_gdbm.lo apr_dbm_sdbm.lo apr_dbm_ndbm.lo

# bring in rules.mk for standard functionality
include /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/build/rules.mk

SUBDIRS = sdbm .
