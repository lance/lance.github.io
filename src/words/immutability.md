---
title: Forget Data Encapsulation - Embrace Immutability
layout: article.jade
date: 2016-11-18
draft: false
gist: lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex7.js lance/53d5ab381b3336a82c8426f517253070:immutability.js lance/53d5ab381b3336a82c8426f517253070:immutability-1.js
---

A couple of weeks ago, I wrote a fairly [long post](/words/es6-data-hiding.html) attempting to shed some light on a few things you can do in your JavaScript classes to enforce the concept of data encapsulation - or data "hiding". But as soon as I posted it, I got some flak from [a friend](http://twitter.com/jcrossley3) who is a Clojure programmer. His first comment about the article was this.

> Mutability and data encapsulation are fundamentally at odds.

Eventually, he walked that back - but only just a little bit. His point, though, was intriguing. I asked him to explain what he meant.

<!-- More -->

> Why is it so wrong to return the `id` in your example? I'm guessing it's not. It might be darn useful to fetch it. in fact, it might greatly enhance the data model for it to be there. But you feel you must "hide" it. why? Because it's mutable, or because you must go to great lengths to make it immutable. Because JavaScript. But if you were returning an immutable data structure, you wouldn't even think about it. All that stress just falls away; you no longer care about hiding your data or encapsulating it. You only care that it's correct and that it properly conveys the essential complexity of your system.

We'll ignore his little dig on the language itself. But maybe what he's saying has some value? I do like the idea of a bunch of "stress just falling away". Let's look at where we ended up in that last post about data encapsulation.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex7.js

So, here we've done our best to hide the `id` property. It's not accessible within user land, and it's barely visible, unless you know about `Reflect.ownKeys` or `Object.getOwnPropertySymbols`. And of course, I never mentioned the `name` property in the last article. But the truth is, it suffers from the same issues that plague the `id` property. It really shouldn't change.

But rats, now I have to replace every `this.name` with `this[NAME]` using a `Symbol` for the property key. And like my friend said, these proerties are arguably useful in userland. I just don't want them changed. How can I do this using JavaScript?

## Is it cold in here, or is it just me?
`Object.freeze()` is nothing new. It's been around forever. Let's take a look at how we'd use it to make our `Product` instances immutable.

gist:lance/53d5ab381b3336a82c8426f517253070:immutability.js

There now. That wasn't so hard, was it?

But wait! What if we _need_ to mutate our objects? What if, for example, there's a `price` property that could change over time? Normally, we'd do something super simple like this.

gist:lance/53d5ab381b3336a82c8426f517253070:immutability-1.js
