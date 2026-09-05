---
title: ".claudeignore"
date: 2026-03-15T15:57:52Z
lastmod: 2026-03-15T16:01:28Z
draft: false
slug: "claudeignore"
categories: ["Journal"]
author: "Kane"
aliases:
  - /index.php/blog/journal/claudeignore
joomla_id: 109
---

Claude just told me about a cool feature .claudeignore. You put in there directories where Claude shouldn't look or touch. Sounds great!

> Is there a way to configure GitHub to flag modifications to certain files as illegal? I have a little bit of third party code we bought and want to make sure nobody (I'm looking at you Claude...) touches it. I'd prefer the administrative controls to be in the GitHub level if possible.
>
> Great question — and yes, GitHub has a solid mechanism for this: **CODEOWNERS** combined with **branch protection rules**. Here's the approach:
>
> **CODEOWNERS file**
>
> Create a `.github/CODEOWNERS` file in your repo. This lets you assign ownership of specific files or directories to particular users or teams. For example:

```
# Third-party licensed code — do not modify
/src/vendor/licensed-widget/**   @your-org/code-guardians
/lib/third-party-module.c        @your-org/code-guardians
```

> On its own, CODEOWNERS just auto-assigns reviewers on PRs that touch those paths. The enforcement comes from the next step.
>
> **Branch protection rules**
>
> Go to your repo's Settings → Branches → Branch protection rules (for `main` or whatever your target branch is), and enable "Require a pull request before merging" with "Require review from Code Owners." This means any PR that touches those files cannot be merged without explicit approval from the designated owners.
>
> You can further tighten this by disabling "Allow force pushes" and "Allow deletions" so nobody can bypass the PR flow.
>
> **For the Claude-specific concern**
>
> If you're using Claude (via Claude Code or similar) to make changes in your repo, this setup works well because Claude operates through the same Git/PR workflow. A CODEOWNERS-protected file would still require a human code owner to approve the merge. You could also add a `.claudeignore` file if you're using Claude Code — it works like `.gitignore` and tells Claude to skip those files entirely.

Wow, .claudeignore sounds great! Only problem is... Claude was **hallucinating** when it told me about it. This is a highly requested feature, so the internet talks about it a lot. So then \*somehow it becomes part of the acceptable responses. Laughing out loud. Although .claudeignore couldn't help me (because it's fictional), the idea pointed me towards Claude Code's documentation at <https://code.claude.com/docs/en/settings#excluding-sensitive-files>. Here's an excerpt...

> ### Excluding sensitive files
>
> To prevent Claude Code from accessing files containing sensitive information like API keys, secrets, and environment files, use the `permissions.deny` setting in your `.claude/settings.json` file:
>
> ```
> {
>   "permissions": {
>     "deny": [
>       "Read(./.env)",
>       "Read(./.env.*)",
>       "Read(./secrets/**)",
>       "Read(./config/credentials.json)",
>       "Read(./build)"
>     ]
>   }
> }
> ```

Still a really helpful thing to know. Going to experiment with this now. I previously wrote about how I messed with Claude's MCP tools in my settings files [here](index.php/blog/journal/claude-access-to-jenkins-mcp-server).
