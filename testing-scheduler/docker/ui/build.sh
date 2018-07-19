basepath=$(cd `dirname $0`; pwd)					# get the absolute path of this shell file.
projectpath=$basepath/../..							# get the root directory of this project
ui_image='leoc/testing-scheduler:ui'				# ui image name

# build the ui-project and generate the dist package.
sudo sh $basepath/pre-builder/build.sh
sudo sh $basepath/pre-builder/run.sh

sudo docker build -t $ui_image -f $basepath/Dockerfile $projectpath