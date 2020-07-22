#!/bin/bash

# clean the backlogs on the target machine

ARG_PREFIX=/opt/miniconda/envs/dev/bin
ARG_QUIET=false
ARG_USER=jvermosen
ARG_CHANNEL=stable
ARG_PROFILE=gcc93
ARG_OPTIONS=""
ARG_SETTINGS=""
ARG_PROFILE="gcc93"
ARG_VERBOSE=0
ARG_NOPKG=0

# script option parsing
OPT_MNEMOS=p:qhvo:s:p:n
OPT_NAMES=prefix:,quiet,help,verbose,options:,settings:,profile:,no-package

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
            echo "script usage:                                             "
            echo "-p   --prefix     location of conan binary                "
            echo "-q   --quiet      quiet mode                              "
						echo "-v   --verbose    additional logs                         "
						echo "-o   --options    conan options                           "
						echo "-s   --settings   conan settings                          "
						echo "-p   --profile    conan profile                           "
						echo "-n   --no-package only perform the configuration install  "
						echo "-h   --help       display this help                       "
						shift 1
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
				-o|--options)
						ARG_OPTIONS=$2
						shift 2
						;;
				-s|--settings)
						ARG_SETTINGS=$2
						shift 2
						;;
				-p|--profile)
						ARG_PROFILE=$2
						shift 2
						;;
				-v|--verbose)
						ARG_VERBOSE=1
						shift 1
						;;
				-n|--no-package)
						ARG_NOPKG=1
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

LIB_VERS[0]="pfr;1.0.0"
LIB_VERS[1]="tws;9.79.1"
LIB_VERS[2]="fmt;6.1.2"
LIB_VERS[3]="spdlog;1.5.0"
LIB_VERS[4]="gtest;1.8.1"
LIB_VERS[5]="gbench;1.4.1"
LIB_VERS[6]="zlib;1.2.11"
LIB_VERS[7]="lz4;1.9.2"
LIB_VERS[8]="zstd;1.4.4"
LIB_VERS[9]="bzip2;1.0.8"
LIB_VERS[10]="doxygen;1.8.18"
LIB_VERS[11]="rcpp;1.0.4"
LIB_VERS[12]="pybind11;2.5.0"
LIB_VERS[13]="boost;1.72.0"

#TODO: parse options and settings lines as "-s setting1 -s setting2, etc"
OPTIONS="${ARG_OPTIONS}"
SETTINGS="${ARG_SETTINGS}"

# refresh configuration
INSTALL_CMD="${CONAN} config install conf"
eval RESULT=\`${INSTALL_CMD}\`

if [ $? = 0 ]; then
	logline "configuration installation succeeded !"
	if [ $ARG_VERBOSE = 1 ]; then
    logline "output: ${RESULT}"
	fi
else
  logline "configuration installation failed !"
  exit 1
fi

if [ $ARG_NOPKG = 1 ]; then
		exit 0
else
  for lib in "${LIB_VERS[@]}"
  do
    IFS=";" read -r -a i <<< "${lib}"
    logline "installing library ${i[0]} version ${i[1]} ..."
    CONAN_CMD="$CONAN create ${i[0]}/${i[1]} ${i[0]}/${i[1]}@$ARG_USER/$ARG_CHANNEL -pr=$ARG_PROFILE $CONAN_OPTIONS $CONAN_SETTINGS"
    eval RESULT=\`${CONAN_CMD}\`

	  if [ $? = 0 ]; then
		  logline "${i[0]} installation succeeded"
	  else
		  logline "${i[0]} installation failed !"
		  exit 1
	  fi

	  if [ $ARG_VERBOSE = 1 ]; then
      logline "${i[0]} output:\n $RESULT"
	  fi
  done
fi
