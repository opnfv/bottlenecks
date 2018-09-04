#!/bin/bash
for file in `find ./`
do
vi +':w ++ff=unix' +':q' ${file}
done
