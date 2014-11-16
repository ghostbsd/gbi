#!/bin/sh

if [ -z "$1" ] ; then
   LOCALBASE=/usr/local
else
   LOCALBASE="$1"
fi

if [ -d "${LOCALBASE}/lib/gbi" ] ; then
   rm -rf ${LOCALBASE}/lib/gbi
fi

mkdir -p ${LOCALBASE}/lib/gbi

# Copy gbi file  
cp -r gbi/* ${LOCALBASE}/lib/gbi

# Install the executable
if [ ! -d "${LOCALBASE}/bin" ] ; then
  mkdir ${LOCALBASE}/bin
fi

cp bin/gbi.sh ${LOCALBASE}/bin/gbi
chown root:wheel ${LOCALBASE}/bin/gbi

chmod 755 ${LOCALBASE}/bin/gbi
