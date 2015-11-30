mod_include.la: mod_include.lo
	$(MOD_LINK) mod_include.lo $(MOD_INCLUDE_LDADD)
DISTCLEAN_TARGETS = modules.mk
static =  mod_include.la
shared = 
