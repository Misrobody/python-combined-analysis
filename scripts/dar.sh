if [ "$#" -ne 1 ]; then
    echo "Usage: command <outdir>"
    exit 1
fi

mkdir "bin/$1"

./distrib/oceandsl-tools/bin/dar \
-l "dynamic" \
-c \
-o "bin/$1" \
-s java \
-m java-class-mode \
-E "anytree" \
-i "data/uxsim/" \

