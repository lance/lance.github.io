---
title: Tracing Asynchronous Operations in Node.js
layout: article.jade
date: 2016-11-15
draft: true
gist: lance/c29af1f40fb8242a5ebc23225a467999:tracing-async-operations-0.js lance/c29af1f40fb8242a5ebc23225a467999:tracing-async-operations-1.js
---

If you've been working with Node.js for really any amount of time, you've
surely experienced completely useless stack traces. You know the ones I mean.
Here's some pretty simple code. What does it do?

<!-- More -->

gist:lance/c29af1f40fb8242a5ebc23225a467999:tracing-async-operations-1.js


Well, it doesn't output anything very helpful when it blows up, that's for sure.


gist:lance/c29af1f40fb8242a5ebc23225a467999:tracing-async-operations-0.js


I mean, I guess there's the fact that `foobar` barfed. That's helpful, I guess.
But there's not much else. What put `foobar` on the event loop?

There's not really any context whatsoever.
