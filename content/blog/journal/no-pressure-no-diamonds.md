---
title: "No Pressure No Diamonds"
date: 2024-05-30T12:46:07Z
lastmod: 2024-05-31T12:10:51Z
draft: false
slug: "no-pressure-no-diamonds"
categories: ["Journal"]
author: "Kane"
aliases:
  - /index.php/blog/journal/no-pressure-no-diamonds
joomla_id: 35
---

![](/images/2024/05/30/no-pressure-no-diamonds.jpg)

It's been a while since I put anything here. Things have been a bit hectic in my life (in a good way). Here goes:

## Heroic

I've been training to become a Heroic Certified Coach (class XX), and I attended Heroic Workshop Instructor Training (class I). As part of that training, I ran my first-ever Spartan race. I completed a 5K race with 20 obstacles, finishing 18 of them. If anyone is interested in Heroic (it's for you; it's for everyone), please use my referral code: [Heroic Referral Code](https://www.heroic.us?fpr=kane). If you are interested in Heroic coaching or workshops, please get in touch with me.

## Work - Product Launch Challenges

Work has been in 'crunch time' since about January, and it is taking a toll on me. We have a new product launch that my team is working on, scheduled for release in July. Managing the complexity of this release has been a lot to handle. We have a new circuit board, new firmware, compliance tests to pass, test equipment to invent, SOPs, manuals, etc. Last week our product launch hit a snag. Our pre-compliance testing at the Intertek lab didn't go so well. The circuit board failed for radiated emissions. We were 10 dB over the 'B' limit line at 50 MHz. This is likely due to our Ethernet circuit, which uses a 25 MHz crystal and supplies a 50 MHz reference clock to the microcontroller for its RMII. I anticipated this and added a pi-filter on the ETH VDD line, but I made an error and put the same net name on both sides of the filter... doh! As a result, we couldn't test the filter. Another issue was that the ETH\_GND plane was only on the top layer, so the stitching vias didn't connect to the inner layer planes. Double doh! Resolving these errors should hopefully fix our 10dB overage. We don't have the facility and equipment to check that in-house, so we'll test it again in the compliance lab. This time we'll bring more samples with different modifications, and at least one of them should pass (or be tunable enough to pass).

## New House

The third big thing occupying my time is our pre-move preparations. We have a builder constructing a home for us right now, and we're planning our move. It's scheduled to be complete early August. Since our rental lease ends July 21, we decided to be homeless for a few weeks or a month. We're using this opportunity to road trip and travel up to Canada - hit me up if you want to connect while we're there. We've rented a storage locker to keep all of our stuff while we're homeless until we take possession of the new house. We've been busy hauling loads of boxes and seasonal things (Christmas tree, etc.), and art and random stuff.

## Looking Ahead

I hope to get back to regular posts soon, now that life is returning to normal. Soon this product will be released, my Heroic training will be complete, and we'll be moved into our new home. At that point, the next challenge is to transition our kids into homeschooling and "unschooling" them. But I'll have lots more time for my writing practice.

## Eating Stress Like an Energy Bar

All of this to say... "no pressure, no diamonds".  It's a Thomas Carlyle quote I heard in Heroic. Check out this 2-minute video about it here: [Eating Stress Like an Energy Bar](https://www.heroic.us/plus-one/how-to-eat-stress-like-an-energy-bar?fpr=kane&fpr=kane). It basically means that your personal growth is always on the other side of your comfort zone.

> "How you perceive stress is actually the largest determinant of how it affects you. In short: if you think life is challenging you to step up and give your best, you'll use that energy to do your best and feel energized. If on the other hand, you think life is threatening you and your well-being, that stress will erode your health and you'll feel enervated".

If you're not at least a little uncomfortable, you're not expanding. You need to push yourself to learn more, do more, risk more, and take on bigger challenges. I'm thanking the Stoic and Heroic gods for the opportunity to practice my philosophy, and push past my comfort zone. Things are busy, but good. What about you? Are you doing something to get yourself out of your comfort zone? Let me know what you think in the comments!

Disclaimer: AI helped me fine-tune this post, and created the image.
