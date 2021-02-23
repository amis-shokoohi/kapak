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

if [[ -d $OPT_KPK_DIR ]]; then
	rm -rf $OPT_KPK_DIR
fi

if [[ -h ${BIN_DIR}/kapak ]]; then
	rm ${BIN_DIR}/kapak
fi
if [[ -h ${BIN_DIR}/kapak-gui ]]; then
	rm ${BIN_DIR}/kapak-gui
fi

echo -e "Copying files to ${OPT_KPK_DIR}...\n"
sleep 2

mkdir $OPT_KPK_DIR

cp ${CURR_DIR}/kapak.py $OPT_KPK_DIR
cp ${CURR_DIR}/kapak-gui.py $OPT_KPK_DIR
cp ${CURR_DIR}/requirements.txt $OPT_KPK_DIR
cp ${CURR_DIR}/LICENSE $OPT_KPK_DIR
cp ${CURR_DIR}/README.md $OPT_KPK_DIR

mkdir ${OPT_KPK_DIR}/lib
if [[ -d ${CURR_DIR}/lib/__pycache__ ]]; then
	rm -rf ${CURR_DIR}/lib/__pycache__
fi
cp ${CURR_DIR}/lib/* ${OPT_KPK_DIR}/lib

mkdir ${OPT_KPK_DIR}/view
cp ${CURR_DIR}/view/* ${OPT_KPK_DIR}/view

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

ln -s ${OPT_KPK_DIR}/kapak ${BIN_DIR}/kapak
ln -s ${OPT_KPK_DIR}/kapak-gui ${BIN_DIR}/kapak-gui

echo "Done - Type kapak or kapak-gui in the terminal"
