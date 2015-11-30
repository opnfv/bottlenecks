top_srcdir   = /bottlenecks/rubbos/app/httpd-2.0.64
top_builddir = /bottlenecks/rubbos/app/httpd-2.0.64
srcdir       = /bottlenecks/rubbos/app/httpd-2.0.64/test
builddir     = /bottlenecks/rubbos/app/httpd-2.0.64/test
VPATH        = /bottlenecks/rubbos/app/httpd-2.0.64/test

# no targets: we don't want to build anything by default. if you want the
# test programs, then "make test"
TARGETS =

PROGRAMS =

PROGRAM_LDADD        = $(EXTRA_LDFLAGS) $(PROGRAM_DEPENDENCIES) $(EXTRA_LIBS)
PROGRAM_DEPENDENCIES =  \
	$(top_srcdir)/srclib/apr-util/libaprutil.la \
	$(top_srcdir)/srclib/apr/libapr.la

include $(top_builddir)/build/rules.mk

test: $(PROGRAMS)

# example for building a test proggie
# dbu_OBJECTS = dbu.lo
# dbu: $(dbu_OBJECTS)
#	$(LINK) $(dbu_OBJECTS) $(PROGRAM_LDADD)
