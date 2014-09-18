curdir=$(pwd)
euler=$(which euler)
srcdir=$(dirname $euler)
prodir=$(dirname $srcdir)
cd $prodir
cd bbox-lattice
input=$curdir/$1

echo "preprocessing..."
python preprocess.py $input;
echo "saving all worlds...";
python awf.py -filter=i,o expWorlds.asp;
echo "creating the lattice without color...";
dlv -silent -filter=up  wexp-up.asp expWorlds_aw.asp > up.dlv;
echo "running euler to get MIS...";
euler -i $input -e mnpw --repair=HST > output.txt;
echo "from MIS to MAC and get lattice..."
python lattice.py $input;
echo "finish";
