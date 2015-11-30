srcdir = .


INCLUDES = -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include/private  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/include  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/xml/expat/lib

PROGRAMS = testdbm testdate testmd4 testmd5 testxml testrmm teststrmatch \
	testuuid testreslist testqueue testuri testpass
TARGETS = $(PROGRAMS)

APRUTIL_DOTTED_VERSION=0.9.19
APRUTIL_MAJOR_VERSION=0
TARGET_LIB_PATH = ../libaprutil-${APRUTIL_MAJOR_VERSION}.la

# bring in rules.mk for standard functionality
include /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/build/rules.mk
PROGRAM_DEPENDENCIES = /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/xml/expat/libexpat.la /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/libapr-0.la -lrt -lm -lcrypt -lnsl -lpthread -ldl
APRUTIL_LDFLAGS = -L/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/xml/expat/lib -no-install

all: $(PROGRAMS)

check: $(PROGRAMS)
# For VPATH builds; where we have no ./data, copy us some data
	if test ! -d "./data"; then cp -r $(srcdir)/data data; fi
	for prog in $(PROGRAMS); do \
		if test "$$prog" = 'testmd4'; then \
			./$$prog -ssomestringtohash; \
			if test $$? = 255; then \
				echo "$$prog failed"; \
				break; \
			fi; \
		elif test "$$prog" = 'testdbm'; then \
			./$$prog auto SDBM; \
			if test $$? = 255; then \
				echo "$$prog failed"; \
				break; \
			fi; \
		else \
			./$$prog ;\
			if test $$? = 255; then \
				echo "$$prog failed"; \
				break; \
			fi; \
		fi; \
	done

testdbm_OBJECTS = testdbm.lo
testdbm_LDADD =  $(TARGET_LIB_PATH)
testdbm: $(testdbm_OBJECTS) $(testdbm_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testdbm_OBJECTS) $(testdbm_LDADD) $(PROGRAM_DEPENDENCIES)

testdate_OBJECTS = testdate.lo
testdate_LDADD =  $(TARGET_LIB_PATH)
testdate: $(testdate_OBJECTS) $(testdate_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testdate_OBJECTS) $(testdate_LDADD) $(PROGRAM_DEPENDENCIES)

testxml_OBJECTS = testxml.lo
testxml_LDADD =  $(TARGET_LIB_PATH)
testxml: $(testxml_OBJECTS) $(testxml_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testxml_OBJECTS) $(testxml_LDADD) $(PROGRAM_DEPENDENCIES)

testmd4_OBJECTS = testmd4.lo
testmd4_LDADD =  $(TARGET_LIB_PATH)
testmd4: $(testmd4_OBJECTS) $(testmd4_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testmd4_OBJECTS) $(testmd4_LDADD) $(PROGRAM_DEPENDENCIES)

testmd5_OBJECTS = testmd5.lo
testmd5_LDADD =  $(TARGET_LIB_PATH)
testmd5: $(testmd5_OBJECTS) $(testmd5_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testmd5_OBJECTS) $(testmd5_LDADD) $(PROGRAM_DEPENDENCIES)

testrmm_OBJECTS = testrmm.lo
testrmm_LDADD =  $(TARGET_LIB_PATH)
testrmm: $(testrmm_OBJECTS) $(testrmm_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testrmm_OBJECTS) $(testrmm_LDADD) $(PROGRAM_DEPENDENCIES)

teststrmatch_OBJECTS = teststrmatch.lo
teststrmatch_LDADD =  $(TARGET_LIB_PATH)
teststrmatch: $(teststrmatch_OBJECTS) $(teststrmatch_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(teststrmatch_OBJECTS) $(teststrmatch_LDADD) $(PROGRAM_DEPENDENCIES)

testuuid_OBJECTS = testuuid.lo
testuuid_LDADD =  $(TARGET_LIB_PATH)
testuuid: $(testuuid_OBJECTS) $(testuuid_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testuuid_OBJECTS) $(testuuid_LDADD) $(PROGRAM_DEPENDENCIES)

testreslist_OBJECTS = testreslist.lo
testreslist_LDADD =  $(TARGET_LIB_PATH)
testreslist: $(testreslist_OBJECTS) $(testreslist_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testreslist_OBJECTS) $(testreslist_LDADD) $(PROGRAM_DEPENDENCIES)

testqueue_OBJECTS = testqueue.lo
testqueue_LDADD =  $(TARGET_LIB_PATH)
testqueue: $(testqueue_OBJECTS) $(testqueue_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testqueue_OBJECTS) $(testqueue_LDADD) $(PROGRAM_DEPENDENCIES)

testuri_OBJECTS = testuri.lo
testuri_LDADD =  $(TARGET_LIB_PATH)
testuri: $(testuri_OBJECTS) $(testuri_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testuri_OBJECTS) $(testuri_LDADD) $(PROGRAM_DEPENDENCIES)

testpass_OBJECTS = testpass.lo
testpass_LDADD =  $(TARGET_LIB_PATH)
testpass: $(testpass_OBJECTS) $(testpass_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testpass_OBJECTS) $(testpass_LDADD) $(PROGRAM_DEPENDENCIES)

testxlate_OBJECTS = testxlate.lo
testxlate_LDADD =  $(TARGET_LIB_PATH)
testxlate: $(testxlate_OBJECTS) $(testxlate_LDADD)
	$(LINK) $(APRUTIL_LDFLAGS) $(testxlate_OBJECTS) $(testxlate_LDADD) $(PROGRAM_DEPENDENCIES)

