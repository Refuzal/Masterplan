# Installing Masterplan

## Ask Claude to do it

Give Claude Code this message:

> Install the Masterplan skill from https://github.com/Refuzal/Masterplan

## Instructions for Claude

If a user asks you to install this skill:

1. Clone the repository to a temporary folder: `git clone --depth 1 https://github.com/Refuzal/Masterplan <tmp>/masterplan`
2. Run `<tmp>/masterplan/install.sh` to install for the user, or `<tmp>/masterplan/install.sh --project` from the project root if they want it in one project only. Ask which they prefer only if they mention a project; otherwise install for the user.
3. Check that `~/.claude/skills/masterplan/SKILL.md` (or `.claude/skills/masterplan/SKILL.md`) exists, then delete the temporary clone.
4. Tell the user it's installed and that they can start with `/masterplan` followed by their idea. A new session may be needed before the skill appears.

If you can't run commands (for example in the Claude apps), tell the user to download `masterplan.skill` from the repository's Releases page and add it in the app's skill settings.

## By hand

```
git clone https://github.com/Refuzal/Masterplan masterplan
cd masterplan
./install.sh              # for your user
./install.sh --project    # or, from a project folder, for that project only
```

To update later, pull the repository and run `install.sh` again.
