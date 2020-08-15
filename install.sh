#! /bin/bash

echo '#! /usr/bin/env python' > kapak
cat ./kapak.py >> kapak

CURRENT_DIR=$(pwd)

if [[ "$CURRENT_DIR" != "/root/kapak" ]]; then
	if [[ -d /root/kapak ]]; then
		rm -r /root/kapak
	fi

	mkdir /root/kapak
	cp -r "$CURRENT_DIR"/* /root/kapak

	echo -e "\nFixing permissions..."
	sleep 1
	chmod +x /root/kapak/install.sh
	chmod +x /root/kapak/kapak

	if [[ -d /bin/kapak ]]; then
		rm -r /bin/kapak
	fi

	mkdir /bin/kapak

	echo "Copying script to /bin/kapak..."
	sleep 1
	cp -r /root/kapak/* /bin/kapak

	rm -r /root/kapak	

	echo "Adding kapak script to PATH..."
	sleep 1
	export PATH=/bin/kapak:$PATH
	echo "export PATH=/bin/kapak:$PATH" >> ~/.bashrc
elif [[ "$CURRENT_DIR" == "/root/kapak" ]]; then
	echo -e "\nFixing permissions..."
	sleep 1
	chmod +x /root/kapak/install.sh
	chmod +x /root/kapak/kapak

	if [[ -d /bin/kapak ]]; then
		rm -r /bin/kapak
	fi

	mkdir /bin/kapak

	echo "Copying script to /bin/kapak..."
	sleep 1
	cp -r /root/kapak/* /bin/kapak

	echo "Adding kapak script to PATH..."
	sleep 1
	export PATH=/bin/kapak:$PATH
	echo "export PATH=/bin/kapak:$PATH" >> ~/.bashrc
fi
echo "Done"
echo -e '\nOpen another terminal and type "kapak"\n'
