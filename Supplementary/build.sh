# build cdcl_ocac
echo "build cdcl_ocac..."
cd cdcl_ocac/
rm -rf build/
mkdir 1200
pip install toml
pip install pyparsing
./configure.sh --auto-download --poly --cocoa
cd build/
make -j12
cd ../../
