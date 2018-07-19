basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.
#run conductor containers
sh $basepath/plugin/run.sh

#run server
sh $basepath/server/run.sh

#run ui
sh $basepath/ui/run.sh