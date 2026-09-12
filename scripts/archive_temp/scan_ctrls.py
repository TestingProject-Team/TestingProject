import os

def scan_controllers():
    ctrl_dir = 'backend/src/main/java/com/bookstore/controller'
    controllers = {}
    for f in sorted(os.listdir(ctrl_dir)):
        if f.endswith('.java'):
            path = os.path.join(ctrl_dir, f)
            lines = open(path, encoding='utf-8').readlines()
            endpoints = []
            base_mapping = ''
            for line in lines:
                l = line.strip()
                if l.startswith('@RequestMapping'):
                    base_mapping = l
                elif any(l.startswith(x) for x in ['@GetMapping', '@PostMapping', '@PutMapping', '@DeleteMapping', '@PatchMapping']):
                    endpoints.append(l)
            controllers[f] = {'base': base_mapping, 'endpoints': endpoints}
    return controllers

ctrls = scan_controllers()
print(f'Found {len(ctrls)} Controllers:')
for c, d in ctrls.items():
    print(f"  {c:<25} -> {d['base']:<35} ({len(d['endpoints'])} endpoints)")
