srcdir = .


TARGETS = \
	poll.lo \
	pollacc.lo 


# bring in rules.mk for standard functionality
include /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/build/apr_rules.mk

INCDIR=../../include
OSDIR=$(INCDIR)/arch/unix
DEFOSDIR=$(INCDIR)/arch/unix
INCLUDES=-I$(INCDIR) -I$(OSDIR) -I$(DEFOSDIR)

# DO NOT REMOVE
