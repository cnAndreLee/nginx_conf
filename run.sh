#!/bin/bash

path=`dirname $0`
cd $path

echo "Input the object you want to operate ! TOS or XCC or ACT or XJD : "
read object


case $object in
    TOS)
    name=TOS.sh
    ;;
    ACT)
    name=ACT.sh
    ;;
    XCC)
    name=XCC.sh
    ;;
    XJD)
    name=TOS_XJD.sh
    ;;
    *)
    echo "Input Error !"
    exit 6
    ;;
esac

echo object is $object
bash ${name}

