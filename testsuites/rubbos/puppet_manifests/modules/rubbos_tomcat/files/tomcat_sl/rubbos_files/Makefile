

###########################
#    RUBBoS Makefile      #
###########################

include config.mk

##############################
#    Environment variables   #
##############################

JAVA  = $(JAVA_HOME)/bin/java
JAVAC = $(JAVA_HOME)/bin/javac
JAVACOPTS = -deprecation
JAVACC = $(JAVAC) $(JAVACOPTS)
RMIC = $(JAVA_HOME)/bin/rmic
RMIREGISTRY= $(JAVA_HOME)/bin/rmiregistry 
CLASSPATH = .:$(J2EE_HOME)/lib/j2ee.jar:$(JAVA_HOME)/jre/lib/rt.jar
JAVADOC = $(JAVA_HOME)/javadoc


#########################
#    Servlets version   #
#########################
#ServletPrinter 
Servlets = Config TimeManagement BrowseCategories Auth RegisterUser RubbosHttpServlet BrowseRegions SearchItemsByCategory SearchItemsByRegion ViewItem ViewBidHistory ViewUserInfo SellItemForm RegisterItem PutCommentAuth PutComment StoreComment BuyNowAuth BuyNow StoreBuyNow PutBidAuth PutBid StoreBid AboutMe

all_servlets_sources =  $(addprefix edu/rice/rubbos/servlets/, $(addsuffix .java, $(Servlets)))
all_servlets_obj = $(addprefix edu/rice/rubbos/servlets/, $(addsuffix .class, $(Servlets)))

servlets: $(all_servlets_obj)

clean_servlets:
	rm -f edu/rice/rubbos/servlets/*.class

####################
#       Client     #
####################

ClientFiles = URLGenerator URLGeneratorPHP RUBBoSProperties Stats \
	      TransitionTable ClientEmulator UserSession 

all_client_sources =  $(addprefix edu/rice/rubbos/client/, $(addsuffix .java, $(ClientFiles)))
all_client_obj = $(addprefix edu/rice/rubbos/client/, $(addsuffix .class, $(ClientFiles))) edu/rice/rubbos/beans/TimeManagement.class

client: $(all_client_obj)

initDB:
	${JAVA} -classpath .:./database edu.rice.rubbos.client.InitDB ${PARAM}

emulator:
	${JAVA} -classpath Client:Client/rubbos_client.jar:. -Xmx1300m -Dhttp.keepAlive=true -Dhttp.maxConnections=1000000 edu.rice.rubbos.client.ClientEmulator

emulatorDebug:
	${JAVA} -classpath Client:Client/rubbos_client.jar:. -Xdebug -Xrunjdwp:transport=dt_socket,address=8000,server=y,suspend=n -Xmx1300m -Dhttp.keepAlive=true -Dhttp.maxConnections=1000000 edu.rice.rubbos.client.ClientEmulator


############################
#       Global rules       #
############################


all: beans ejb_servlets client javadoc flush_cache

world: all servlets

javadoc :
	${JAVADOC} -d ./doc/api -bootclasspath ${CLASSPATH} -version -author -windowtitle "RUBBoS API" -header "<b>RUBBoS (C)2001 Rice University/INRIA</b><br>" edu.rice.rubbos.beans edu.rice.rubbos.beans.servlets edu.rice.rubbos.client

clean:
	rm -f core edu/rice/rubbos/beans/*.class edu/rice/rubbos/beans/JOnAS* edu/rice/rubbos/beans/servlets/*.class edu/rice/rubbos/client/*.class edu/rice/rubbos/servlets/*.class

%.class: %.java
	${JAVACC} -classpath ${CLASSPATH} $<

flush_cache: bench/flush_cache.c
	gcc bench/flush_cache.c -o bench/flush_cache

