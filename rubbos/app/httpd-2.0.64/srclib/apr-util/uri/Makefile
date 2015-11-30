

INCLUDES = -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include/private  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/include  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/xml/expat/lib -I.

TARGETS = uri_delims.h apr_uri.lo
CLEAN_TARGETS = gen_uri_delims uri_delims.h

# bring in rules.mk for standard functionality
include /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/build/rules.mk

gen_uri_delims_OBJECTS = gen_uri_delims.lo
gen_uri_delims: $(gen_uri_delims_OBJECTS)
	$(LINK) $(EXTRA_LDFLAGS) $(gen_uri_delims_OBJECTS) $(EXTRA_LIBS)

apr_uri.lo: uri_delims.h apr_uri.c

uri_delims.h: gen_uri_delims
	./gen_uri_delims > uri_delims.h
