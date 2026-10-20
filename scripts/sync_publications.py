#!/usr/bin/env python3
"""Generate website publication data from the resume repository's bibliography."""
import argparse
import json
import re
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('bibliography', type=Path)
args = parser.parse_args()
source = args.bibliography.read_text()

def clean(value):
    return ' '.join(value.replace('\\_', '_').replace('{', '').replace('}', '').split())

records = []
for entry in re.finditer(r'@(article|inproceedings)\s*\{\s*([^,]+),', source, re.I):
    pos = entry.end()
    fields = {}
    while pos < len(source):
        while source[pos].isspace() or source[pos] == ',': pos += 1
        if source[pos] == '}': break
        match = re.match(r'([\w+]+)\s*=\s*', source[pos:])
        if not match: raise ValueError(f'Invalid field near {source[pos:pos+60]}')
        name = match[1].lower()
        pos += match.end()
        start = pos
        if source[pos] == '{':
            depth = 1
            pos += 1
            start = pos
            while depth:
                if source[pos] == '{': depth += 1
                elif source[pos] == '}': depth -= 1
                pos += 1
            value = source[start:pos-1]
        elif source[pos] == '"':
            pos += 1
            start = pos
            while source[pos] != '"': pos += 1
            value = source[start:pos]
            pos += 1
        else:
            while source[pos] not in ',}\n': pos += 1
            value = source[start:pos]
        fields[name] = clean(value)
    authors = []
    for author in re.split(r'\s+and\s+', fields['author']):
        if ',' in author:
            family, given = author.split(',', 1)
            author = given.strip() + ' ' + family.strip()
        authors.append(author)
    key = entry[2]
    records.append(dict(id=key, title=fields['title'], authors=authors,
                        year=int(fields['year']),
                        venue=fields.get('booktitle', fields.get('journal', '')),
                        url='https://doi.org/' + fields['doi'] if fields.get('doi') else fields['url'],
                        preprint='preprint' in fields.get('keywords', ''),
                        code={'z3alpha_2024':'https://github.com/JohnLyu2/z3alpha',
                              'z3alpha_acta_2025':'https://github.com/JohnLyu2/z3alpha',
                              'btor2select':'https://gitlab.com/sosy-lab/software/btor2-select',
                              'btor2select_student':'https://gitlab.com/sosy-lab/software/btor2-select'}.get(key)))
records.sort(key=lambda r: (-r['year'], r['title']))
target = Path(__file__).resolve().parents[1] / '_data/publications.json'
target.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
print(f'Wrote {len(records)} publications to {target}')
