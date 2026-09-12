import os, re

def audit_backend_code():
    src_dir = 'backend/src/main/java/com/bookstore'
    findings = []
    
    # 1. Inspect Controllers
    ctrl_dir = os.path.join(src_dir, 'controller')
    for f in os.listdir(ctrl_dir):
        if not f.endswith('.java'): continue
        content = open(os.path.join(ctrl_dir, f), encoding='utf-8').read()
        
        # Check for direct ID access without auth check
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            if '@DeleteMapping' in line or '@PutMapping' in line:
                # check surrounding lines
                snippet = '\n'.join(lines[idx:min(len(lines), idx+15)])
                if '{id}' in line and 'Authentication' not in snippet and 'Admin' not in f and 'Ping' not in f:
                    findings.append(f"[POTENTIAL IDOR / UNCHECKED AUTH] {f}:{idx+1} -> {line.strip()}")
            if 'System.out.println' in line or 'printStackTrace' in line:
                findings.append(f"[CONSOLE LOG] {f}:{idx+1} -> {line.strip()}")

    # 2. Inspect Services
    svc_dir = os.path.join(src_dir, 'service')
    for f in os.listdir(svc_dir):
        if not f.endswith('.java'): continue
        content = open(os.path.join(svc_dir, f), encoding='utf-8').read()
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            if '.get()' in line and 'Optional' not in line and 'Optional<' not in line and not line.strip().startswith('//'):
                findings.append(f"[UNSAFE OPTIONAL GET] {f}:{idx+1} -> {line.strip()}")
            if 'System.out.println' in line or 'printStackTrace' in line:
                findings.append(f"[CONSOLE LOG] {f}:{idx+1} -> {line.strip()}")

    # 3. Inspect Repositories
    repo_dir = os.path.join(src_dir, 'repository')
    for f in os.listdir(repo_dir):
        if not f.endswith('.java'): continue
        content = open(os.path.join(repo_dir, f), encoding='utf-8').read()
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            if '@Query' in line and 'nativeQuery = true' in line:
                findings.append(f"[NATIVE QUERY CHECK] {f}:{idx+1} -> {line.strip()}")

    return findings

findings = audit_backend_code()
print(f"Total findings: {len(findings)}")
for f in findings:
    print(" ", f)
