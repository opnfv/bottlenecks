basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.
#build conductor
sh $basepath/plugin/build.sh

#build server
sh $basepath/server/build.sh

#build ui
sh $basepath/ui/build.sh