mod_http.la: http_core.lo http_protocol.lo http_request.lo
	$(MOD_LINK) http_core.lo http_protocol.lo http_request.lo $(MOD_HTTP_LDADD)
mod_mime.la: mod_mime.lo
	$(MOD_LINK) mod_mime.lo $(MOD_MIME_LDADD)
DISTCLEAN_TARGETS = modules.mk
static =  mod_http.la mod_mime.la
shared = 
