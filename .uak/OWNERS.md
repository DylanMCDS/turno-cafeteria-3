# Shared-file owners

One writer per shared file. Others ask the owner with `uak msg ID --kind request`. Patterns are relative, with no spaces; directories end in `/`.
An owner is not a prerequisite for everyone: consumers work on published contracts and mocks. To transfer ownership, open a PR to main.

| Pattern | Owner task |
|---|---|
| pyproject.toml | HACK-001 |
| uv.lock | HACK-001 |
| web/package.json | HACK-001 |
| web/package-lock.json | HACK-001 |
| web/vite.config.ts | HACK-001 |
| web/index.html | HACK-001 |
| web/src/main.tsx | HACK-001 |
| app/main.py | HACK-001 |
| app/schemas/ | HACK-001 |
| web/src/fixtures/ | HACK-001 |
| Dockerfile | HACK-001 |
| render.yaml | HACK-001 |
| web/src/App.tsx | HACK-002 |
| web/DESIGN.md | HACK-002 |
| web/src/index.css | HACK-002 |
| web/src/lib/ui/ | HACK-002 |
