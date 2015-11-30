

INCLUDES = -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/include/private  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr/include  -I/bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/xml/expat/lib 

TARGETS = apr_buckets_file.lo apr_buckets_pool.lo apr_buckets_flush.lo \
          apr_buckets_refcount.lo apr_buckets_heap.lo apr_buckets_simple.lo \
          apr_buckets.lo apr_buckets_mmap.lo apr_buckets_socket.lo \
          apr_buckets_eos.lo apr_buckets_pipe.lo apr_brigade.lo \
          apr_buckets_alloc.lo

# bring in rules.mk for standard functionality
include /bottlenecks/rubbos/app/httpd-2.0.64/srclib/apr-util/build/rules.mk
