#!/bin/sh

BASEDIR=$PWD
echo "alias pipfreezeignore='pip freeze | grep -vFxf ignore_requirements.txt'" >> ".bashrc"


# Create virtual environment and install requirements that will be ignored later
python -m venv venv
source venv/Scripts/activate
venv/Scripts/pip install -r ignore_requirements.txt

# Create hello world file
PRJDIR="$BASEDIR/project"
PRJFILE="$PRJDIR/main.py"
echo $PRJDIR
mkdir -p $PRJDIR
echo "print('setting env up')" >> $PRJFILE

# Create a gitignore for venv and vscode (optional)
cat <<END_CONCAT >> "$BASEDIR/.gitignore"
.vscode/*
venv/*
END_CONCAT