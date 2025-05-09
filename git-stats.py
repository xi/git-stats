import sys
import subprocess

# TODO aggregate by month/year


def run(args):
    proc = subprocess.run(args, check=True, stdout=subprocess.PIPE, encoding='utf-8')
    return proc.stdout


def parse_stats(s):
    line = s.splitlines()[-1].split()
    insertions = 0
    deletions = 0
    for i in range(1, len(line)):
        if line[i].startswith('insertion'):
            insertions = int(line[i - 1], 10)
        elif line[i].startswith('deletion'):
            deletions = int(line[i - 1], 10)
    return insertions, deletions

p = subprocess.Popen(
    ['git', 'rev-list', 'HEAD', '--no-merges'],
    stdout=subprocess.PIPE,
    encoding='utf-8',
)

data = {}

for i, commit in enumerate(p.stdout):
    print(i, file=sys.stderr)
    date = run(['git', 'show', '-s', '--format=%cs', commit.rstrip()]).rstrip()
    data.setdefault(date, [0, 0])
    d = parse_stats(run(['git', 'show', '--shortstat', commit.rstrip()]))
    data[date][0] += d[0]
    data[date][1] += d[1]

for key, value in data.items():
    print(key, *value)
