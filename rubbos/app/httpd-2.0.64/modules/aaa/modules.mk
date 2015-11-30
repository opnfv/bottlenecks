mod_access.la: mod_access.lo
	$(MOD_LINK) mod_access.lo $(MOD_ACCESS_LDADD)
mod_auth.la: mod_auth.lo
	$(MOD_LINK) mod_auth.lo $(MOD_AUTH_LDADD)
DISTCLEAN_TARGETS = modules.mk
static =  mod_access.la mod_auth.la
shared = 
