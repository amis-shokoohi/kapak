#! /usr/bin/env bash

echo '#! /usr/bin/env python3' > kapak
cat ./kapak.py >> kapak

CURRENT_DIR=$(pwd)
ROOT_DIR=/root/kapak
BIN_DIR=/bin/kapak

if [[ $CURRENT_DIR != $ROOT_DIR ]]; then
	if [[ -d $ROOT_DIR ]]; then
		rm -rf $ROOT_DIR
	fi

	mkdir $ROOT_DIR
	cp -r ${CURRENT_DIR}/* $ROOT_DIR
	cd $ROOT_DIR
fi

echo -e "\nFixing permissions..."
sleep 2
chmod +x ${ROOT_DIR}/install.sh
chmod +x ${ROOT_DIR}/kapak

if [[ -d $BIN_DIR ]]; then
	rm -rf $BIN_DIR
fi

mkdir $BIN_DIR

echo "Copying files to $BIN_DIR..."
sleep 2
cp -r ${ROOT_DIR}/* $BIN_DIR
if [[ -f ${BIN_DIR}/kapak.py ]]; then
	rm ${BIN_DIR}/kapak.py
fi

rm -rf $ROOT_DIR

echo "Adding kapak script to PATH..."
sleep 2
export PATH=${BIN_DIR}:$PATH
echo "export PATH=${BIN_DIR}:$PATH" >> ~/.bashrc
echo "Done"
echo -e '\nOpen another terminal and type "kapak"\n'
