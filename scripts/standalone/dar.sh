if [ "$#" -ne 1 ]; then
    echo "Usage: command <outdir>"
    exit 1
fi

mkdir "bin/$1"

./tools/oceandsl-tools/bin/dar \
-l "dynamic" \
-c \
-o "bin/$1" \
-s java \
-m java-class-mode \
-E "numpy" \
-i "data/numpy/operation-execution-logs/" \

