basepath=$(cd `dirname $0`; pwd)                                        # get the absolute path of this shell file.
projectpath=$basepath/../../..                                          # get the root directory of this project
group="x-lab"
ui_image="$group/testing-scheduler:ui-builder"                            # ui image name
docker build -t $ui_image -f $basepath/Dockerfile $projectpath