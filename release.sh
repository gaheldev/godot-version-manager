system="linux"
dir="release/${system}/gdvm"
mkdir -p ${dir}/dist

cp dist/gdvm ${dir}/dist/
cp gdvm.completion ${dir}/
cp godot.png ${dir}/
cp install.sh ${dir}/

(
cd ${dir}/..
archive="gdvm_${system}.zip"
zip -r ${archive} gdvm
mv ${archive} ..
)
