---
title: Data Hiding in ES6
layout: article.jade
date: 2016-10-14
draft: true
gist: lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex1.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex2.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex3.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex4.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex5.js
---

For much of my early career, I was an OO developer. I genuflected regularly in
front of the altar of data encapsulation, object heirarchies and static typing.
And the syntax. Oh the syntax!

But I have changed, of course, and so much of the dogma and ceremony that
I participated in during those times has come to seem a lot less important
than it was 20 years ago. Languages, and developers evolve. But that doesn't
mean there aren't some really good lessons to learn.

Take, for instance, data encapsulation.

<!-- More -->

When I first began to seriously look at Javascript as a language, data
encapsulation - or the lack of it - was one of the things that really stuck
in my old OO craw. While I loved the simplicity of the `{}` data structure,
the fact that most properties I chose to add to it were typically just there -
sticking out for everyone to see (and perhaps corrupt). The language didn't
make it very easy to keep this data protected.

Take a look at how this simplistic approach to the `{}` data structure
might cause some real headaches. Here we have a `productCatalog()` lookup
function that returns a data object containing the properties for a product.
It might look something like this:

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex1.js

Notice that the object returned here contains a function, `related()` which
will find the set of products related to this one using this object's `id`
or `name` property. But those properties are just there hanging on to the
returned object by their fingernails. What if some evil bit of code came along
and did this: `product.id = 0x00034` just to see what would happen? How
would the `related()` function handle that? We just don't know.

There have been ways to deal with this of course. One of the great things
about Javascript is how flexible it can be. Maybe the developer who wrote
the `productCatalog()` function knew some of these tricks. Here's one way
to handle it using Javascript's `Object.defineProperty` function.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex2.js

**But... eeewwww.**

Ok, well let's see how well that worked. At first things look great -
no `id` property on basic inspection, but it's there! And it can't be changed!

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex3.js

But darn it. The property name appears in the `Object.getOwnPropertyNames()`
result. This isn't terrible, but we're not doing a great job of hiding data.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex4.js

## Enter ES6

ES6 or EcmaScript 2015, as it is formally known, introduces lots of great
new language features. I wish I had time to tell you about them all! But
for now, let's just focus on one thing. Data Hiding and Encapsulation.

There are a few new ways developers can approach this problem now, when
using modern Javascript interpreters with ES6 features available.

### Getters

First let's take a look at Getters. ES6 getters allow you to easily
use a function that makes a property essentially read only (and which
can also be the result of some calculation within the function - but
that's not the point here). Here's how you would use a getter in ES6
and how you could achieve the same functionality in ES5. The new syntax
is way better.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex5.js