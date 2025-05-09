#!/bin/sh -e

now=$(date '+%Y')
echo 'date,commit,files,language,blank,comment,code'
for year in $(seq 2018 "$now"); do
    for month in $(seq 1 12); do
        date=$(printf '%04i-%02i-01' "$year" "$month")
        commit=$(git rev-list -n 1 --before="$date" HEAD)
        if [ -n "$commit" ]; then
            printf '%s,%s,' "$date" "$commit"
            cloc --git "$commit" --exclude-dir tests,migrations --csv | tail -n 1
            # cloc --git "$commit" --exclude-dir tests,migrations --include-lang Python --csv | tail -n 1
        fi
    done
done
