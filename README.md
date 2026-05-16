# Skills

Claude Code skills repository.

## Structure

```
skills/
  development/       # coding, debugging, architecture
  product_management/ # PRDs, planning, reviews
  personal/          # personal productivity
scripts/
  install.sh         # one-time setup per machine
  update.sh          # pull latest + cleanup
```

## Bootstrap a new machine

```bash
git clone https://github.com/erik-saltwell/skills.git
cd skills
./scripts/install.sh
```

## Update

```bash
./scripts/update.sh
```

## Adding a skill

1. Create a directory under `skills/<category>/<skill-name>/`
2. Add a `SKILL.md` with the skill instructions
3. Run `./scripts/install.sh` (or it will be picked up on next `update.sh`)
4. Commit and push
