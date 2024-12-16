# kill all the processes in a loop
process=$1
# loop from 1 to 200
for i in {1..200}
do
    kill -9 $(pidof $process) || exit 0
done
