
# This  is Bash: beware of he spaces, e.g.
# A=2 is an asssignment
# A= 2 is NOT an assignment!

numrun=$1
folder=run$numrun
highT=1.0
runT=0.1
density=0.85
runtime=10.0
snapshottime=1.0

mkdir $folder
cd $folder
pwd

# prepare start configuration 
python ../../src/prepare.py --density $density --thermostat $highT
# run the dynamics at high temperature for some time to ge a liquid 
dynarun start.shoulder.xml  -f 1.0 --snapshot 1.0 -o disordered.start.xml
echo "::: Converting to LAAMPS atom file for visualisation in Ovito"
python ../../src/convertconf.py disordered.start.xml 0
# change the thormostat temperature
startconf=start.T${runT}rho${density}.xml
dynamod -T $runT disordered.start.xml -o $startconf   
# quench at the desired sampling temperature 
dynarun $startconf  -f $runtime --snapshot $snapshottime 
echo "::: Converting last configuration to LAAMPS atom file for visualisation in Ovito" 
python ../../src/convertconf.py config.out.xml.bz2 -1