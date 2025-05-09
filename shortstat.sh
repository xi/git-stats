#!/bin/sh -e

git rev-list HEAD --no-merges | while read commit; do
    printf '%s,' "$(git show -s --format='%cs')"
    git show --shortstat "$commit" | tail -n 1 | sed 's/ *\([0-9]\+\) files\? changed\(, \([0-9]\+\) insertions\?(+)\)\?\(, \([0-9]\+\) deletions\?(-)\)\?/\1,\3,\5/'
done
