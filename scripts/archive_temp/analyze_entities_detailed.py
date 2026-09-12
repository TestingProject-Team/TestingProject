import os, re

entity_dir = r"E:\TestingProject\backend\src\main\java\com\bookstore\entity"
entities = {}
enums = {}

for fname in sorted(os.listdir(entity_dir)):
    if not fname.endswith(".java"):
        continue
    fpath = os.path.join(entity_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if Enum
    if re.search(r"\bpublic\s+enum\s+(\w+)", content):
        m_enum = re.search(r"\bpublic\s+enum\s+(\w+)\s*\{([^}]+)\}", content, re.DOTALL)
        if m_enum:
            enum_name = m_enum.group(1)
            vals = [v.strip().split('(')[0].strip() for v in m_enum.group(2).split(',') if v.strip()]
            enums[enum_name] = vals
        continue
    
    # Entity Class
    m_cls = re.search(r"\bpublic\s+class\s+(\w+)", content)
    cls_name = m_cls.group(1) if m_cls else fname.replace(".java", "")
    
    # Table name
    m_tbl = re.search(r'@Table\s*\(\s*name\s*=\s*"([^"]+)"', content)
    tbl_name = m_tbl.group(1) if m_tbl else cls_name.lower()
    
    # Find fields, PK (@Id), and relationships
    fields = []
    relationships = []
    
    lines = content.splitlines()
    current_annotations = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("@"):
            current_annotations.append(stripped)
            continue
        
        # Field declaration
        m_field = re.search(r"private\s+([A-Za-z0-9_<>]+)\s+([A-Za-z0-9_]+)\s*;", stripped)
        if m_field:
            ftype, fname_var = m_field.group(1), m_field.group(2)
            is_pk = any("@Id" in a for a in current_annotations)
            
            # Check relationships
            rel_type = None
            join_col = None
            for a in current_annotations:
                if "@ManyToOne" in a:
                    rel_type = "ManyToOne"
                elif "@OneToMany" in a:
                    rel_type = "OneToMany"
                elif "@OneToOne" in a:
                    rel_type = "OneToOne"
                elif "@ManyToMany" in a:
                    rel_type = "ManyToMany"
                
                m_jc = re.search(r'@JoinColumn\s*\(\s*name\s*=\s*"([^"]+)"', a)
                if m_jc:
                    join_col = m_jc.group(1)
            
            if rel_type:
                relationships.append({
                    "field": fname_var,
                    "type": rel_type,
                    "target": ftype,
                    "join_column": join_col
                })
            else:
                fields.append({
                    "name": fname_var,
                    "type": ftype,
                    "pk": is_pk
                })
            current_annotations = []
        elif stripped and not stripped.startswith("//") and not stripped.startswith("/*") and not stripped.startswith("*"):
            current_annotations = []
            
    entities[cls_name] = {
        "table": tbl_name,
        "fields": fields,
        "relationships": relationships
    }

with open(r"E:\TestingProject\schema_analysis.txt", "w", encoding="utf-8") as out:
    out.write(f"Total Enums: {len(enums)}\n")
    for ename, evals in enums.items():
        out.write(f"  Enum {ename}: {evals}\n")
    out.write(f"\nTotal Entities / Tables: {len(entities)}\n")
    for cname, edata in entities.items():
        out.write(f"\nEntity {cname} -> Table '{edata['table']}':\n")
        out.write(f"  PK/Fields: {[f['name'] + (' (PK)' if f['pk'] else '') for f in edata['fields']]}\n")
        out.write(f"  Relationships:\n")
        for r in edata["relationships"]:
            out.write(f"    - {r['type']} with {r['target']} (col: {r['join_column']})\n")

print(f"Analysis done! Enums: {len(enums)}, Entities/Tables: {len(entities)}")
