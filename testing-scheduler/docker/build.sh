# get the absolute path of this shell file.
basepath=$(cd `dirname $0`; pwd)

#build conductor
sh $basepath/plugin/build.sh

#build server
sh $basepath/server/build.sh

#build ui
sh $basepath/ui/build.sh