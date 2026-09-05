---
title: "Claude Access to Jenkins MCP Server"
date: 2026-03-12T22:50:48Z
draft: false
slug: "claude-access-to-jenkins-mcp-server"
categories: ["Journal"]
author: "Kane"
aliases:
  - /index.php/blog/journal/claude-access-to-jenkins-mcp-server
joomla_id: 108
---

Spent some time getting my claude code agent hooked into our Jenkins CI/CD MCP server.

![](/images/image-20260310-043312.png)

Just put your username in plain text, and convert you api token to base64.

![](/images/image-20260310-043535.png)

Documentation is here: <https://plugins.jenkins.io/mcp-server/>

It's kinda handy asking Claude to review a failed build and plan a fix for the it.
