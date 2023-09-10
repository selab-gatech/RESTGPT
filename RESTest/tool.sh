#! /bin/bash
end=$((SECONDS+3600))

while [ $SECONDS -lt $end ]; do
    java -jar target/restest-full.jar src/test/resources/api.properties
done
