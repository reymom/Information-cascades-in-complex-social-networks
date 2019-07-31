cp -r inputs $TMPDIR
cd $TMPDIR/inputs

#he de recorrer de 0 a 15

/usr/local/anaconda/bin/python integrateandfire.py 0

cd ..

scp -p inputs/resultados1000nodos15ponderaciones0.txt nodo00:$SGE_O_WORKDIR/outputs/
