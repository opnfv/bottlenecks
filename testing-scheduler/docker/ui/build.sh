# get the absolute path of this shell file.
basepath=$(cd `dirname $0`; pwd)
# get the root directory of this project
projectpath=$basepath/../..
group="x-lab"
# ui image name
ui_image="$group/testing-scheduler:ui"

# build the ui-project and generate the dist package.
sh $basepath/pre-builder/build.sh
sh $basepath/pre-builder/run.sh

docker build -t $ui_image -f $basepath/Dockerfile $projectpath