---
title: Data Hiding in ES6
layout: article.jade
date: 2016-10-14
draft: false
gist: lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex1.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex2.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex3.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex4.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex5.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex6.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex7.js lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex8.js
---

For a lot of my early career, I was an OO developer. I genuflected regularly in
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
I hated the fact that most properties I chose to add to it were typically
just there - sticking out for everyone to see and perhaps corrupt. The language
didn't make it very easy to keep this data protected.

Take a look at how this simplistic approach to the `{}` data structure
might cause some real headaches. Here we have a `productCatalog()` lookup
function that returns a `Product` data object. It might look something like
this:

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex1.js

Notice that the object returned here contains a function, `related()` which
will find the set of products related to this one using this object's `id`
or `name` property. But those properties are just there hanging on to the
returned object by their fingernails. What if some evil bit of code came along
and did this: `product.id = 0x00034` just to see what would happen? How
would the `related()` function handle that? We just don't know.

There are ways to deal with this of course. One of the great things
about Javascript is how flexible it can be. Maybe the developer who wrote
the `productCatalog()` function knew some of these tricks. Here's one way
to handle it using Javascript's `Object.defineProperty` function.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex2.js

**But... eeewwww.**

Let's see how well that worked. At first things look great -
no `id` property on basic inspection. And if you do try to modify it,
the value can't be changed. Yay!

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex3.js

But darn it. The property name appears in the `Object.getOwnPropertyNames()`
result. This isn't terrible, but we're not doing a great job of hiding data.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex4.js

What I'd really like is for the `Product` object to have a reference to the
`id` but no way for client code to read it or even see it. Closures, for example,
provide a way to do this. But that's really an entirely separate blog post, and what
I really want to talk about here is ES6.

## EcmaScript 2015

ES6 or EcmaScript 2015, as it is formally known, introduces lots of great
new language features. I wish I had time to tell you about them all, but
for now, I'll just focus on one subject. Data Hiding and Encapsulation.

There are a few new ways developers can approach this problem now, when
using modern Javascript interpreters with ES6 features available.

### Getters

First let's take a look at Getters. ES6 getters allow you to easily
use a function that makes a property read only. And since a getter is a
function, the value could even be the result of some calculation. But
that's not the point here.

Here's how you would use a getter in ES6 and how you could achieve the
same functionality in ES5. The new syntax is way better.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex5.js

But this still doesn't really get what we want. There are two tools
besides closures we can use to really and truly hide our data. Those are
`WeakMap` and `Symbol`. Let's look at the `WeakMap` first.

### WeakMaps

The `WeakMap` is a new data structure in ES6. It acts a lot like
a regular map data structure. They are `iterable`, and have getters and
setters for objects. What makes them unique is that the keys are weakly
referenced. This means, essentially, that when the only remaining reference
to the key is the key itself, the entry is removed from the map. Here's
how you can use the `WeakMap` data structure to effectively hide private
class data.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex6.js

Assuming this code is in a module that exports the `productCatalog`
function, there is no way for client code to see or modify the `id`
property. Success!

I like this approach. It's elegant and simple. The only real drawback I
have found with this is performance. It's pretty expensive to do these
`WeakMap` lookups to get a handle on a property. So if performance is
paramount. Consider using `Symbol` as property keys.

### Symbols

I have found that using properties whose keys are `Symbol`s, while not
as elegant as `WeakMap` in my opinion is my preferred data hiding
technique, because it's just so much faster.

One of the interesting things about `Symbol` is that each `Symbol`
is unique. If we can keep the `Symbol` private within our module,
then we don't have to worry about client code accessing the property.
Here's how our `Product` object would look if we took this approach.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex7.js

Additionally, when you use a `Symbol` for a property key, the property
does not appear in the list of properties returned from
`Object.getOwnPropertyNames()`. This is nice. The downside is that
the property leaks when using `Reflect.ownKeys()`.

gist:lance/0aa47a11aefd4f2c1ef21c034e5b0110:es6-data-hiding-ex8.js

But I can live with that when performance matters. For
[Fidelity](https://npmjs.com/package/fidelity), we found that moving
from `WeakMap` to `Symbol` for private data gave us a measurable, and
quite significant performance boost.
