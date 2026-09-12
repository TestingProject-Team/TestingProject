import os, re

def scan_frontend():
    fe_dir = 'frontend/src'
    api_calls = []
    files_scanned = 0
    for root, dirs, files in os.walk(fe_dir):
        for f in files:
            if f.endswith(('.js', '.jsx', '.ts', '.tsx')):
                files_scanned += 1
                path = os.path.join(root, f)
                content = open(path, encoding='utf-8').read()
                rel = os.path.relpath(path, fe_dir)
                
                # find axios / api calls like api.get('/...'), axios.post('/...')
                matches = re.findall(r'(?:api|axios|fetch)\s*\.\s*(get|post|put|delete|patch)\s*\(\s*[`\'"]([^`\'"]+)[`\'"]', content)
                for method, url in matches:
                    api_calls.append({'file': rel, 'method': method.upper(), 'url': url})
                
                # template literals
                matches_tl = re.findall(r'(?:api|axios|fetch)\s*\.\s*(get|post|put|delete|patch)\s*\(\s*`([^`]+)`', content)
                for method, url in matches_tl:
                    api_calls.append({'file': rel, 'method': method.upper(), 'url': url})

    return files_scanned, api_calls

count, calls = scan_frontend()
print(f"Scanned {count} frontend files, found {len(calls)} API call points.")
calls_by_url = {}
for c in calls:
    u = c['url'].split('?')[0] # remove query string
    calls_by_url.setdefault(u, []).append(f"{c['method']} ({c['file']})")

print(f"\nUnique API endpoints called from Frontend ({len(calls_by_url)}):")
for u, callers in sorted(calls_by_url.items()):
    print(f"  {u:<45} -> {', '.join(callers[:3])}")
