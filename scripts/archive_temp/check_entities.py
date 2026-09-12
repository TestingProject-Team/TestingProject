import os, re

backend_src = r'E:\TestingProject\backend\src\main\java\com\bookstore\entity'
tables = []
enums = []
for f in os.listdir(backend_src):
    if f.endswith('.java'):
        content = open(os.path.join(backend_src, f), encoding='utf-8').read()
        m_table = re.search(r'@Table\s*\(\s*name\s*=\s*"([^"]+)"', content)
        if m_table:
            tables.append((f, m_table.group(1)))
        elif 'enum ' in content:
            enums.append(f)
        elif '@Entity' in content:
            tables.append((f, '(default table name)'))

print(f'Entity with @Table ({len(tables)}):')
for jf, tname in sorted(tables):
    print(f'  {jf} -> {tname}')
print(f'Enums ({len(enums)}):', enums)
