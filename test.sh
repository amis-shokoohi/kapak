#! /usr/bin/env bash

python3 -m unittest discover -p "*_test.py" -v

if [[ $? != 0 ]]; then
	exit 1
fi

DATA='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et 
dolore magna aliqua. Mus mauris vitae ultricies leo. Tempor nec feugiat nisl pretium fusce. Sollicitudin ac 
orci phasellus egestas tellus rutrum tellus pellentesque. Imperdiet proin fermentum leo vel orci porta. 
Purus non enim praesent elementum facilisis leo vel. Proin sed libero enim sed faucibus. Volutpat lacus laoreet 
non curabitur gravida arcu ac. Diam vulputate ut pharetra sit amet aliquam id diam. Posuere ac ut consequat 
semper viverra nam libero. Porttitor massa id neque aliquam vestibulum morbi blandit. Nunc consequat interdum 
varius sit amet mattis. Turpis egestas pretium aenean pharetra magna ac placerat vestibulum. Nulla aliquet enim 
tortor at auctor urna. Ut morbi tincidunt augue interdum. Netus et malesuada fames ac turpis egestas maecenas 
pharetra convallis. Ornare aenean euismod elementum nisi quis. Sit amet aliquam id diam maecenas ultricies mi. 
Aliquet enim tortor at auctor urna nunc id. Sed sed risus pretium quam.'

FILE_NAME=test_file.txt
FILE_NAME_KPK=test_file.kpk
if [[ -e $FILE_NAME ]]; then
	rm $FILE_NAME
fi
echo $DATA > $FILE_NAME
FILE_HASH=$(sha256sum $FILE_NAME)

echo 'password' > password.txt
python3 kapak.py encrypt -r -b=1 $FILE_NAME

echo 'password' > password.txt
python3 kapak.py decrypt -r -b=1 $FILE_NAME_KPK

if [[ $(sha256sum $FILE_NAME) != $FILE_HASH ]]; then
	echo 'failed'
	rm $FILE_NAME
	exit 1
fi
rm $FILE_NAME

DIR_NAME=test-dir
DIR_NAME_KPK=test-dir.kpk
if [[ -d $DIR_NAME ]]; then
	rm -rf $DIR_NAME
fi
mkdir $DIR_NAME
for i in {1..3}; do
	echo $DATA > ${DIR_NAME}/f_${i}.txt
done

echo 'password' > password.txt
python3 kapak.py encrypt -r -b=1 $DIR_NAME

echo 'password' > password.txt
python3 kapak.py decrypt -r -b=1 $DIR_NAME

echo 'password' > password.txt
python3 kapak.py encrypt -rz -b=1 $DIR_NAME

echo 'password' > password.txt
python3 kapak.py decrypt -r -b=1 $DIR_NAME_KPK

rm -rf $DIR_NAME
