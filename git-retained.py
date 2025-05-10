# https://github.com/erikbern/git-of-theseus

import csv
import datetime
import functools
import subprocess
import sys


def run(cmd):
    p = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, encoding='utf-8')
    return p.stdout.strip()


def get_first_date():
    s = run(['sh', '-c', 'git log --reverse --format=%ad --date=iso | head -n 1'])
    dt = datetime.datetime.fromisoformat(s)
    return dt.date()


@functools.cache
def get_rev_at(date):
    return (
        run(['git', 'rev-list', '-n1', '--before', date.isoformat(), 'HEAD'])
        or run(['git', 'hash-object', '-t', 'tree', '/dev/null'])
    )


def get_changes(rev1, rev2):
    s = run(['git', 'diff', '--shortstat', rev1, rev2])
    parts = s.replace(',', '').split()

    try:
        i = parts.index('insertions(+)')
        added = int(parts[i - 1], 10)
    except ValueError:
        added = 0

    try:
        i = parts.index('deletions(-)')
        removed = int(parts[i - 1], 10)
    except ValueError:
        removed = 0

    return added, removed


def retained(a, b, c):
    added_after_b, _ = get_changes(b, c)
    added_in_total, _ = get_changes(a, c)
    return added_in_total - added_after_b


def iter_months_since(start):
    today = datetime.date.today()
    year = start.year
    month = start.month
    while True:
        date = datetime.date(year, month, 1)
        yield date
        if date > today:
            break
        month += 1
        if month == 13:
            year += 1
            month = 1


def iter_years_since(start):
    today = datetime.date.today()
    return range(start.year, today.year + 1)


if __name__ == '__main__':
    start = get_first_date()
    w = csv.writer(sys.stdout)
    w.writerow([''] + [str(year) for year in iter_years_since(start)])

    for date in iter_months_since(start):
        rev = get_rev_at(date)
        row = [date.isoformat()]

        for year in iter_years_since(start):
            date_start = datetime.date(year, 1, 1)
            date_end = datetime.date(year + 1, 1, 1)
            rev_start = get_rev_at(date_start)
            rev_end = get_rev_at(date_end)
            if date <= date_start:
                row.append('0')
            elif date <= date_end:
                row.append(str(retained(rev_start, rev, rev)))
            else:
                row.append(str(retained(rev_start, rev_end, rev)))

        w.writerow(row)
