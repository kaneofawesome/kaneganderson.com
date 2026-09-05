---
title: "I Asked Claude to Roast My AI Prompting"
date: 2026-03-31T01:54:04Z
lastmod: 2026-03-31T02:00:49Z
draft: false
slug: "i-asked-claude-to-roast-my-ai-prompting"
categories: ["Journal"]
author: "Kane"
aliases:
  - /index.php/blog/journal/i-asked-claude-to-roast-my-ai-prompting
joomla_id: 110
---

I've been a paid Claude user for about a year. Before that, ChatGPT — and I've been consciously writing my Google searches more like prompts to nudge Gemini in the right direction. So I'm not a beginner. But "not a beginner" doesn't mean "not leaving value on the table." So today I ran an experiment: I asked Claude to evaluate me.

*Me:*

I'm trying to optimize my usage of this chatbot. using whatever you know about me from our chats, please suggest tips for me to improve my throughput using ai to help me accomplish my tasks (mostly  coding, but also bouncing ideas and doing investigating). Please give me no more than 10 helpful tips. Be harshly honest if I'm doing anything dumb.

*Claude:*

Here's what I can infer from our history, with no sugarcoating:

---

**1. Front-load context, every time.** You work across a wide stack — BACnet/C, Altium, Jenkins/Groovy, IIS, Git. I have no memory between sessions. The single biggest time-waster is watching a conversation bootstrap slowly because you dropped in mid-thought. One dense paragraph of "here's my environment, here's what I've tried, here's the exact error" saves 3–5 back-and-forth turns.

**2. Paste the actual error/code immediately.** Several of our sessions (the mstpcap extcap bug, the IIS proxy config) burned early turns while you described symptoms in prose. Paste the log, the stack trace, or the code block *first*, then describe it. I can synthesize faster than I can extract.

**3. You're good at deep dives — but you sometimes re-explain what I already know.** When continuing a multi-session topic (BACnet routing, Metrix++), you tend to re-summarize history I can't remember anyway, but do it incompletely. Instead: paste a compact "state of play" bullet list at the start. Faster than prose recap, and more accurate.

**4. Use me for decision gates, not just execution.** You used me well for the Jenkins ratchet pattern — we explored the *approach* before writing code. Do this more. Before you spend time implementing something, ask "here are my 3 options, what's the trap I'm not seeing?" That's where I add disproportionate value.

**5. Stop being polite about wrong answers.** When I'm off-base (and I do go off-base on niche stuff like BACnet MS/TP framing details or Altium-specific quirks), correct me bluntly and immediately. "No, that's wrong, here's the spec" gets you back on track in one turn. Gentle hedging costs you turns.

**6. For investigation tasks, give me a hypothesis to attack.** Your philosophy/physics discussions are productive because you come in with a strong thesis. Do the same for technical investigations — "I think this is a broken-pipe issue in the extcap exit path, convince me I'm wrong or help me confirm it" is dramatically more efficient than "help me debug this hang."

**7. Split coding sessions from architecture sessions.** You sometimes start asking for code when you haven't nailed the design yet, and the conversation thrashes. If you're not 80% sure of the structure, spend one session on architecture/decisions, then open a fresh session to write code with a clean spec.

**8. Artifact/code iterations: tell me the constraint upfront.** When asking for code edits, state immutable constraints early ("this must stay compatible with C99," "Jenkins pipeline, not declarative," "Windows Server 2019 IIS"). Otherwise I write something reasonable that fails your constraint and we loop.

**9. Use me to draft things you hate writing.** You used me well for the business email to Brian and the AE team charter. You probably have more of this — spec documents, PR descriptions, internal proposals. These are high-leverage, low-effort tasks for me and high-effort, low-enjoyment tasks for you. Delegate more aggressively here.

**10. The one actually dumb thing: session length.** Some of your debugging sessions get very long before you get a working answer. Long contexts make me worse, not better — I start losing track of earlier constraints and contradicting myself. If a debugging thread exceeds ~15 turns without resolution, **start a fresh session with a tight summary of what's been ruled out.** You'll get a sharper answer faster.

*Me:*

Great advice, thanks! What are 3 tips or concepts the absolute best chatbot prompters are using, that I am under-utilizing?

*Claude:*

**1. Giving me a role with sharp constraints — not just a question.** Top prompters don't ask "how do I do X." They say: "You are a senior embedded C developer who is allergic to dynamic allocation and has memorized the BACnet stack source. Review this code for correctness and tell me what you'd reject in a code review." The role primes my vocabulary, assumptions, and critical stance. The constraint ("allergic to dynamic allocation") kills entire classes of bad suggestions before they start. You almost never do this. It would be particularly powerful for your Altium/BACnet/Jenkins work where domain-specific judgment matters a lot.

---

**2. Asking for the reasoning trace before the answer.** Elite prompters often include something like: "Before giving me your answer, walk through your assumptions and flag where you're uncertain." This forces me to surface the gaps in my knowledge — especially valuable on niche topics like BACnet MS/TP timing, IIS ARR quirks, or obscure Jenkins pipeline behavior where I can produce confident-sounding nonsense. You tend to evaluate my answer after I give it. Catching the uncertainty before saves a whole loop.

---

**3. Negative-space prompting — tell me explicitly what NOT to do.** The best prompters define the failure modes they want to avoid, not just the outcome they want. "Do not suggest a solution that requires restarting the BACnet stack. Do not use deprecated ARR config syntax. Do not restructure the function, only fix the logic inside it." This is different from stating constraints — it's preemptively closing the escape hatches I'd otherwise use to give you a technically-correct-but-useless answer. You occasionally do this reactively ("no wait, that won't work because...") but almost never proactively. Front-loading it would cut your iteration loops in half.

## So What?

The biggest gains aren't about clever tricks — they're about giving Claude enough context, constraint, and direction to skip the warmup laps. The three advanced techniques (role + constraints, reasoning trace before answer, negative-space prompting) aren't hacks. They're just how you'd brief a smart colleague. I already know how to do that. I just wasn't doing it here.

## Key Takeaways

**Fixing my bad habits:**

- Front-load context every session
- Paste the actual error or code first, describe it second
- Instead of a prose recap, use a tight bullet-point "state of play"
- Be blunt — politeness costs turns
- Start a fresh session if a debugging thread exceeds ~15 turns

**How to use it smarter:**

- Use Claude before writing code, not just during
- Split architecture sessions from coding sessions
- State immutable constraints up front

**What elite prompters do that I wasn't:**

- **Role + sharp constraints**
- **Reasoning trace before answer**
- **Negative-space prompting**

---

## Further Reading

Anthropic's own [prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) covers role prompting, chain-of-thought (the reasoning trace technique above), and clear constraint-setting — and lines up closely with everything here. Worth bookmarking.
