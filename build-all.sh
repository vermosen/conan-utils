#!/bin/bash

# clean the backlogs on the target machine

ARG_PREFIX=/opt/miniconda/bin
ARG_QUIET=false
ARG_USER=jvermosen
ARG_CHANNEL=stable
ARG_PROFILE=gcc84
ARG_OPTIONS=""
ARG_SETTINGS=""
ARG_CLEAN=false

# script option parsing
OPT_MNEMOS=p:q
OPT_NAMES=prefix:,quiet

PARSED=$(getopt --options=$OPT_MNEMOS --longoptions=$OPT_NAMES --name "$0" -- "$@")

if [ $? != 0 ] ;
then
    echo "Failed parsing options." >&2
    exit 1
fi

eval set -- "$PARSED"

while true; do
    case "$1" in
        -h|--help)
            echo "script usage:                          "
            echo "-p   --prefix location of conan binary "
            echo "-q   --quiet  quiet mode               "
            shift
            exit 0
            ;;
        -p|--prefix)
            ARG_PREFIX=$2
            shift 2
            ;;
        -q|--quiet)
            ARG_QUIET=true
            shift 1
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Programming error"
            exit 3
            ;;
    esac
done

logline () {
  if [ $ARG_QUIET = false ]
  then
      echo $1
  fi
}

CONAN=$ARG_PREFIX/conan

declare -a LIB_VERS

LIB_VERS[0]="bzip2;1.0.8"
LIB_VERS[1]="tws;9.79.1"
LIB_VERS[2]="fmt;6.1.2"
LIB_VERS[3]="gtest;1.8.1"
LIB_VERS[4]="zlib;1.2.11"
LIB_VERS[5]="zlib;1.2.11"
LIB_VERS[6]="lz4;1.9.2"
LIB_VERS[7]="zstd;1.4.4"
LIB_VERS[8]="doxygen;1.8.18"
LIB_VERS[9]="rcpp;1.0.4"
LIB_VERS[10]="pybind11;2.5.0"
LIB_VERS[11]="boost;1.72.0"
LIB_VERS[12]="spdlog;1.5.0"
LIB_VERS[13]="gbench;1.4.1"
LIB_VERS[14]="doxygen;1.8.18"
LIB_VERS[14]="pfr;1.0.0"
LIB_VERS[15]="gbench;1.4.1"

#TODO: parse options and settings lines
OPTIONS=""
SETTINGS=""

for lib in "${LIB_VERS[@]}"
do
  IFS=";" read -r -a i <<< "${lib}"
  
  # if not ARG_CLEAN
  #logline "checking if ${i[0]} version ${i[1]} is installed"
  #CONAN_SEARCH_CMD = 'conan search | grep "${i[0]}/${i[1]}@$ARG_USER/$ARG_CHANNEL" | wc -l'
  #eval RESULT=\`${CONAN_SEARCH_CMD}\`
  
  #if RESULT=1
  #logline "checking if ${i[0]} version ${i[1]} is installed"
  
  logline "installing library ${i[0]} version ${i[1]} ..."
  CONAN_CMD="$CONAN create ${i[0]}/${i[1]} ${i[0]}/${i[1]}@$ARG_USER/$ARG_CHANNEL -pr=$ARG_PROFILE $CONAN_OPTIONS $CONAN_SETTINGS"
  eval RESULT=\`${CONAN_CMD}\`
  logline "conan returned result value ${RESULT}"
done
