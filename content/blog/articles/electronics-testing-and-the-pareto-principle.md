---
title: "Electronics Testing and the Pareto Principle"
date: 2025-07-09T20:34:59Z
lastmod: 2025-07-24T03:19:37Z
draft: false
slug: "electronics-testing-and-the-pareto-principle"
categories: ["Blog"]
author: "Kane"
aliases:
  - /index.php/blog/articles/electronics-testing-and-the-pareto-principle
joomla_id: 89
---

This article showcases how Q-PAC tests Fan Controllers, presents a framework for thinking about product testing, and discusses the highest leverage test opportunities to get the most bang for your buck.

---

## TL;DR

Q-PAC thoroughly tests Fan Controllers. We use the 80/20 principle to design tests that have the highest ROI to catch the most defects, as early as possible, for the least investment. There are 4 categories of tests, and they can be summarized by these quick taglines:

1. **Plan** for failure.
2. **Borrow eyes** early and often.
3. **Automate** what a script can do more cost effectively than a human.
4. **See what happens when you abuse it** late enough to matter, early enough to fix.

---

##

# Introduction

When I was just starting my career, I promised to myself:

*… of the best of my knowledge and power, I will not henceforward suffer or pass, or be privy to the passing of, Bad Workmanship or Faulty Material in aught that concerns my works before mankind as an Engineer, or in my dealings with my own Soul before my Maker.*

Two things I want to talk about today are bad workmanship and faulty material. I wish I could say I’ve never made a mistake. The truth is I’ve come to delight in my mistakes. Anyone who doesn’t make mistakes isn’t challenging themselves, stretching, or growing. I’ve done my share of learning from mistakes (note those first few words “of the best of my knowledge and power”).

A lofty vow for a rookie, but one I still try to honor. Mistakes? Plenty. Regrets? Only the ones I didn’t learn from.

In this post, we’re going to talk about how Q-PAC tests our Fan Controllers. Then, we’ll talk about our testing philosophy in general. We’ll discuss four categories of tests: planning ahead, another pair of eyes, scripted repeatable checks, and mess around and find out. We will use the Pareto Principle as a lens while thinking about which are the most worthwhile test methods.

---

# Fan Controller

#### Planning Ahead

Testing for the Q-PAC Fan Controller starts at the engineer’s desk. We designed the Fan Controller PCB from the beginning to persist even if the microcontroller fails or is unpowered. This is due to an onboard relay whose ‘normally closed’ state connects the fan speed signal directly to each motor on the multimotor plenum fan. If the microcontroller is alive and well, it commandeers control by switching the relay.

The PCB needs to be programmed with our home-grown firmware, which has a similar level of robust testing. Again, it begins at the engineer’s desk. We architected our firmware to be robust, modular, and scalable. We follow SOLID principles and the “clean code” modus operandi. Our firmware runs through scripted unit tests after each program revision. We use the [git-flow workflow](https://www.gitkraken.com/learn/git/git-flow "https://www.gitkraken.com/learn/git/git-flow") to organize our releases.

#### Another Pair of Eyes

Once the combined changes are ready to be prototyped, we put another set of eyes on it and do a PDR (preliminary design review), following a PCB design checklist. Once accepted, we order prototypes and test them with a DVT (design validation test). For code, once our modifications are ready, we do pull requests and code reviews. Other engineers inspect the code, looking to offer improvements or advice.

#### Scripted Automated Checks

Whenever a developer edits the PCB design, they run automated ERC (electrical rule checks) and DRC (design rule checks). Over 500 mistake conditions are checked after each and every revision of the design. For programming, our CI/CD pipeline takes over and runs its analysis tools on the changes to re-run unit tests, check for warnings, test for complexity, and do static analysis on the code. This process, testing, and analysis all comprise our ‘scripted automated test’ strategy, and greatly reduces the amount of bugs, all before the product is ever built.

#### Mess Around and Find Out

If the prototypes meet their design spec, we do some ‘mess around and find out’ tests, as we prepare for production. We try to stress the device and find out where the limits are. For example, run the device at low temperature, provide higher than expected pressure, supply a voltage that’s too high, or transfer a malformed packet and see how the device responds.

## Production Tests

After the design is released for production, we test our materials and assemblies. Q-PAC has incoming inspection tests for the smaller PCB inside the fan controller, known as the MIIB (motorized impeller interface board).

The Fan Controller is assembled in the factory, and the mains supply terminals are checked using a “high potential test.”

Then the Controller is programmed with its Hardware Test Application, which is a special firmware version for interacting with an automated test fixture. The Hardware Test Application can communicate with the tester, perform test sequences, report voltages and readings, and save important information like the serial number to non-volatile memory. The automated test fixture is used to carry out these operations and apply known stimuli to the PCB, such as specific voltages and specific air pressures to be sensed by the PCB sensors.

The test fixture then queries the device for its perception of the stimuli and records any physical outputs from the DUT (device under test). The test fixture checks for communication protocols, eventually judges the DUT to pass or fail, and saves a test report for later review.

In integration testing, pressure sensors get calibrated for accuracy. Calibrations are saved on each Fan Controller in EEPROM memory. Once the Fan Controller passes the hardware test application checks, production application firmware is programmed to the microcontroller, and the test fixture is again used to validate the correct functionality of the Fan Controller under simulated “realistic” conditions.

After production firmware checks have passed, an employee puts a “QC Approved” sticker on and initials it.

This procedure is applied to every fan controller produced.

---

# General Philosophy and Approach to Testing

In the next part, we’re going to cover a variety of tests that we *could* do, and talk about the Pareto 80/20 Principle to focus on tests that we *will* do. I categorize testing into four different buckets, and discuss them through the lens of the Pareto principle.

# The Tools

Bad workmanship or faulty material. There are myriad tools to help with these problems.

Code reviews, PRs (pull requests), checklists, double checks, and prototypes. DVT (design verification tests), PDRs (preliminary design reviews), CDRs (critical design reviews), root cause analyses, FMEA (failure mode and effects analysis), QC (quality control) checks, SOPs (standard operating procedures). There are DRCs (design rule checks), ERC (electrical rule checks), FEA (finite element analysis). There’s CFD (computational flow dynamics), DFM (design for manufacturing). To name a few. Engineers love their TLAs (three-letter acronyms). All these tools aim to eliminate defects. If you use them all it takes *ages* to get anything done.

What a pain.

There are days I just can’t be bothered. But most days I take my medicine. And all this quality assurance stuff really is analogous with medicine. Just as taking too much medicine can kill you, too much testing can grind innovation to a halt. Medicine has side effects, and you need other medicine to counteract those. Similarly, performing a few tests can entice you to do a second set, which in turn points out the need for yet a third. It can get so complicated that you need a PhD in pharmacology to sort it out.

So let’s simplify it down to just a few fundamentals of testing.

# The Fundamentals

I like to think of testing tools in a few categories, like the four main food groups (**candy, candy canes, candy corn, and syrup**).

Consider using tests from each of the categories:

1. Planning ahead
2. Another pair of eyes
3. Scripted, repeatable checks
4. Mess around and find out

The list above is in order of efficacy (just my opinion). As with anything, the devil is in the details. I like the Pareto Principle, which states that 20% of efforts yield 80% of results. So, I try to focus on the highest-leverage actions I can take that will catch the most defects.

#### 1 - Planning Ahead

It comes with experience and requires discernment. Murphy’s Law states if something can go wrong, then it will – don’t be surprised. Tests that fall into this category are FMEA, QC checklists, backup plans, or, in essence, any test that is prepared in anticipation of a defect. For your 80/20 here, checklists are your best friend.

#### 2 - Another Pair of Eyes

When it comes to *another pair of eyes*, the highest ROI comes from deep-focused reading. This gives experts a chance to go deep. It’s underrated and gets no attention because there’s (usually) no clear pass/fail criteria, no consistency, and a shortage of true masters of their arts.

This is quiet contemplation, deep understanding, and when it bears fruit there’s no fanfare nor white knight riding in. Not a single parade. It usually comes in the form of a question: “Did you consider *abc*?” or “What about when *x,y,z* happens?” And the engineer feels like he’s been hit by a ton of bricks and skulks back to the drawing board. Meanwhile, nobody else but the engineers ever knew the potential crisis was avoided, and millions of dollars in losses were avoided.

See also: [Charles Proteus Steinmetz, the Wizard of Schenectady](https://www.smithsonianmag.com/history/charles-proteus-steinmetz-the-wizard-of-schenectady-51912022/), the man who charged Henry Ford $10,000 in an itemized bill that read: making chalk mark on generator $1. Knowing where to make mark $9,999.

#### 3 - Scripted Repeatable Checks

I like [Elon’s “algorithm”](https://www.inc.com/jeff-haden/elon-musks-algorithm-a-5-step-process-to-dramatically-improve-nearly-everything-is-both-simple-brilliant.html "https://www.inc.com/jeff-haden/elon-musks-algorithm-a-5-step-process-to-dramatically-improve-nearly-everything-is-both-simple-brilliant.html") for this situation. Question requirements, delete, simplify, accelerate, and automate. For scripted/repeatable checks, automate them so a computer can run them instantly and focus your efforts on the most complicated part.

I once wrote some code that compares two numbers to be `equal_within_tolerance`. Due to the way decimal numbers are saved in a computer, called a *float*, with zeros and ones, the computer has a hard time comparing them for equality. You save 0.1, and the closest possible 32-bit representation is 0.10000000149011611938 (actual value stored in 32-bit float). My `equal within tolerance` function had a bug, which was found easily by a unit test. Fortunately, this bug was fixed before it was ever released.

That’s just one tiny example, but when you stack up hundreds of small unit tests and perform them automatically by a computer in a few milliseconds, the resulting confidence can be a game changer.

#### 4 - Mess Around and Find Out

This is sometimes called “limit testing,” “design abuse testing,” “adversarial testing,” “chaos engineering,” and/or “destructive testing.” These tests should be done at major milestones. Prefer passing the “normal” tests first so that you can be confident enough to use “mess around and find out” sparingly.

The reasons to reserve these until major milestones are that they take a while, ruin prototypes, and have no clear end state. Examples of this include smoke tests, stress tests, cycle tests, black hat tests, red team tests, and anything that proves it can “take a punch”.

| Group | Quick Definition | Typical Tools |
| --- | --- | --- |
| 1. **Planning Ahead** | Spot trouble before it starts | FMEA, checklists, backup plans |
| 2. **Another Pair of Eyes** | Fresh human scrutiny | Design reviews, focused doc reads |
| 3. **Scripted, Repeatable Checks** | Let a machine patrol the details | Unit tests, DRC/ERC, automated simulations, AOI |
| 4. **Mess Around & Find Out** | Full-system experiments | Prototypes, release-candidate trials, destructive testing, limit tests |

# When to Catch a Defect

In one of my favorite books on writing software, *Code Complete*, Steve McConnel talks about the fact that you save the most money by catching defects earliest. A bug found late in the game is very costly and difficult to fix. A bug caught the same day it’s created is quick and easy to fix. The same holds true for physical products. The best place to catch a defect is in design. See [the Raygun blog post](https://raygun.com/blog/cost-of-software-errors/ "https://raygun.com/blog/cost-of-software-errors/") on how

> The [big Facebook outage](https://en.wikipedia.org/wiki/2021_Facebook_outage "https://en.wikipedia.org/wiki/2021_Facebook_outage") in 2021 (remember that?) was reported to cost [$65 million](https://www.forbes.com/sites/abrambrown/2021/10/05/facebook-outage-lost-revenue/ "https://www.forbes.com/sites/abrambrown/2021/10/05/facebook-outage-lost-revenue/") in advertising revenue, and (temporarily) tanked Mark Zuckerberg’s personal wealth to the tune of $6 billion.

This [2004 paper from NASA](https://ntrs.nasa.gov/api/citations/20100036670/downloads/20100036670.pdf "https://ntrs.nasa.gov/api/citations/20100036670/downloads/20100036670.pdf") goes into detail about software errors.

As for physical products, one big example is [the Tylenol recall of 2010](https://www.cbsnews.com/news/the-tylenol-crisis-one-recall-is-a-misfortune-five-looks-like-carelessness/ "https://www.cbsnews.com/news/the-tylenol-crisis-one-recall-is-a-misfortune-five-looks-like-carelessness/"). According to [a government oversight committee](https://oversightdemocrats.house.gov/legislation/hearings/johnson-johnsons-recall-of-childrens-tylenol-and-other-pediatric-medicines "https://oversightdemocrats.house.gov/legislation/hearings/johnson-johnsons-recall-of-childrens-tylenol-and-other-pediatric-medicines"), Johnson & Johnson [ignored internal audit](https://oversightdemocrats.house.gov/sites/evo-subsites/democrats-oversight.house.gov/files/documents/20100527Sharfstein.pdf "https://oversightdemocrats.house.gov/sites/evo-subsites/democrats-oversight.house.gov/files/documents/20100527Sharfstein.pdf") results that showed it did not meet its own standards, and a “musty smell” was ignored. This is an example of how catching that defect early and solving for the root cause could have prevented a corporate catastrophe.

---

# Summary

That was a long brain dump about the **idea** of testing. We use the 80/20 principle to design tests that have the highest ROI to catch the most defects, for the least investment. There are four categories of tests, and they can be summarized by these quick taglines:

1. **Plan** for failure.
2. **Borrow eyes** early and often.
3. **Automate** what a script can do more cost effectively than a human.
4. **See what happens when you abuse it** late enough to matter, early enough to fix.

What are we testing here at Q-PAC?

| Group | What Q-PAC does for Fan Controllers |
| --- | --- |
| 1. **Planning Ahead** | We strive to make the most robust and durable fan available. We designed the circuit board to fail over to manual control of the motors even when the microprocessor fails or loses power. |
| 2. **Another Pair of Eyes** | Pull request code reviews, preliminary design review, design validation testing, ECO (engineering change order) procedure including document circulation, and, of course, regulatory compliance test. |
| 3. **Scripted, Repeatable Checks** | Software and firmware unit tests. Build custom in-factory product testing workstations for subassemblies. Standard operating procedures. Incoming material test for circuitry. Automated test scripts. Harness continuity checks. Plug fan subassembly functional test. High-potential voltage test. Routine sensor calibrations. |
| 4. **Mess Around & Find Out** | Full-system experiments, limit testing, and resilience testing. |

---
