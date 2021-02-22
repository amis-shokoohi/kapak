#! /usr/bin/env bash

CURR_DIR=$(pwd)
OPT_KPK_DIR=/opt/kapak
BIN_DIR=/usr/local/bin

if [[ ! -f ${CURR_DIR}/kapak.py ]]; then
	echo "Error: You have to cd into kapak directory"
	exit 1
fi

echo -e "removing old kapak version...\n"
sleep 2

OLD_BIN_DIR=/bin/kapak
if [[ -d $OLD_BIN_DIR ]]; then
	rm -rf $OLD_BIN_DIR
fi

echo -e "Copying files to ${OPT_KPK_DIR}...\n"
sleep 2

if [[ -d $OPT_KPK_DIR ]]; then
	rm -rf $OPT_KPK_DIR
fi
mkdir $OPT_KPK_DIR

cp -r ${CURR_DIR}/* $OPT_KPK_DIR

echo '#! /usr/bin/env python3' > ${OPT_KPK_DIR}/kapak
echo 'from sys import path' >> ${OPT_KPK_DIR}/kapak
echo "path.insert(0, '${OPT_KPK_DIR}')" >> ${OPT_KPK_DIR}/kapak
cat ${OPT_KPK_DIR}/kapak.py >> ${OPT_KPK_DIR}/kapak
chmod +x ${OPT_KPK_DIR}/kapak
rm ${OPT_KPK_DIR}/kapak.py

echo '#! /usr/bin/env python3' > ${OPT_KPK_DIR}/kapak-gui
echo 'from sys import path' >> ${OPT_KPK_DIR}/kapak-gui
echo "path.insert(0, '${OPT_KPK_DIR}')" >> ${OPT_KPK_DIR}/kapak-gui
cat ${OPT_KPK_DIR}/kapak-gui.py >> ${OPT_KPK_DIR}/kapak-gui
chmod +x ${OPT_KPK_DIR}/kapak-gui
rm ${OPT_KPK_DIR}/kapak-gui.py

echo -e "Adding script to ${BIN_DIR}...\n"
sleep 2

if [[ -f ${BIN_DIR}/kapak ]]; then
	rm ${BIN_DIR}/kapak
fi
if [[ -f ${BIN_DIR}/kapak-gui ]]; then
	rm ${BIN_DIR}/kapak-gui
fi

ln -s ${OPT_KPK_DIR}/kapak ${BIN_DIR}/kapak
ln -s ${OPT_KPK_DIR}/kapak-gui ${BIN_DIR}/kapak-gui

echo "Done"
