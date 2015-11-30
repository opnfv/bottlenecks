srcdir = .


TARGETS = \
	proc.lo \
	procsup.lo \
	thread.lo \
	threadpriv.lo \
	signals.lo

# bring in rules.mk for standard functionality
include /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/build/apr_rules.mk

INCDIR=../../include
DEFOSDIR=$(INCDIR)/arch/unix
INCLUDES=-I$(INCDIR) -I$(DEFOSDIR)

# DO NOT REMOVE
