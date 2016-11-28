---
title: Forget Data Encapsulation - Embrace Immutability
layout: article.jade
date: 2016-11-18
draft: false
staging: true
---

A couple of weeks ago, I wrote a fairly [long post](/words/es6-data-hiding.html) attempting to shed some light on a few things you can do in your JavaScript classes to enforce the concept of data encapsulation - or data "hiding". But as soon as I posted it, I got some flak from [a friend](http://twitter.com/jcrossley3) who is a Clojure programmer. His first comment about the article was this.

> Mutability and data encapsulation are fundamentally at odds.

Eventually, he walked that back - but only just a little bit. His point, though, was intriguing. I asked him to explain what he meant.

<!-- More -->

> Why is it so wrong to return the `id` in your example? I'm guessing it's not. It might be darn useful to fetch it. In fact, it might greatly enhance the data model for it to be there. But you feel you must "hide" it. Why? Because it's mutable, or because you must go to great lengths to make it immutable. Because JavaScript. But if you were returning an immutable data structure, you wouldn't even think about it. All that stress just falls away; you no longer care about hiding your data or encapsulating it. You only care that it's correct and that it properly conveys the essential complexity of your system.

We'll ignore his little dig on the language itself, for now. But maybe what he's saying has some value. I do like the idea of a bunch of "stress just falling away". Let's look at where we ended up in that last post about data encapsulation.

````js
const ID = Symbol('id');
class Product {
  constructor (name) {
    this.name = name;
    this[ID] = 2340847;
  }
  related () {
    return lookupRelatedStuff( this[ID] );
  }
}
````

So, here we've done our best to hide the `id` property using a `Symbol` as a property key. It's not accessible within user land, and it's barely visible, unless you know about `Reflect.ownKeys()` or `Object.getOwnPropertySymbols()`. And of course, I never mentioned the `name` property in the last article. But the truth is, it suffers from the same issues that plague the `id` property. It really shouldn't change.

But to accomplish that, I have to replace every `this.name` with `this[NAME]` using a `Symbol` for the property key. And like my friend said, these proerties are arguably useful in userland. I just don't want them changed. I want **immutability**. How can I do this using JavaScript?

## Is it cold in here, or is it just me?
`Object.freeze()` is nothing new. It's been around forever. Let's take a look at how we'd use it to make our `Product` instances immutable.

````javascript
class Product {
  constructor (name) {
    this.name = name;
    this.id = 2340847;
    // make this instance immutable
    Object.freeze(this);
  }
}
const widget = new Product('a-widget');
// Setting the name to something else has no effect.
widget.name = 'something-else';
widget.name; // << 'a-widget'
````

There now. That wasn't so hard, was it? We give a `Product` instance the deep freeze and return it.

What about those situations where you really _need_ to mutate your application state. What if, for example, there's a `price` that could change over time? Normally, we'd do something super simple. Like just update the price.

````js
this.price = getUpdatedPrice(this);
````

But of course, if we're going for immutability and the safety that comes along with that, then this is clearly not the corret approach. We are mutating the `Product` instance when we do `this.price = someValue()`.

So, what can we do about it? One strategy might be to use `Object.assign()` to copy properties from one object to another, always generating a new object for every data mutation. Perhaps something like this.

````js
class Product {
  updatePrice () {
    // check DB to see if price has changed
    return Object.assign(new Product(), this, { price: getNewPrice(this) } );
  }
}
````

OK, we are getting somewhere, I guess. We can use `Object.freeze()` to make our objects immutable, and then `Object.assign()` to generate a new object using existing properties whenever something needs to be mutated. Let's see how well this works.

````js
acmeWidget.updatePrice();
TypeError: Cannot assign to read only property 'price' of object '#<Product>'
    at repl:1:23
    at sigintHandlersWrap (vm.js:22:35)
    at sigintHandlersWrap (vm.js:96:12)
    at ContextifyScript.Script.runInThisContext (vm.js:21:12)
    at REPLServer.defaultEval (repl.js:313:29)
    at bound (domain.js:280:14)
    at REPLServer.runBound [as eval] (domain.js:293:12)
    at REPLServer.<anonymous> (repl.js:513:10)
    at emitOne (events.js:101:20)
    at REPLServer.emit (events.js:188:7)
````

Ughh. This is happening because I've got `new Product()` as the first parameter to the `Object.assign()` call, and once a `Product` is constructed, it's frozen. I need to defer freezing the object until _after_ it's constructed, I guess. Otherwise, if instead I just use `{}` then the returned object won't be an instance of `Product`.

But how can I do that? I could use a factory function to return instances of `Product`. Or to simplify things even more, I guess we could change our data model to not use a class at all. For the sake of simplification and experimentation, let's give it a shot. Maybe the plain old JavaScript objects are all we need.

````js
// Use a factory function to return plain old JS objects
const productFactory = (name, price) => Object.freeze({ name, price });

// Always bump the price by 4%! :)
const updatePrice = (product) => Object.freeze(
      Object.assign({}, product, { price: product.price * 1.04 }));

const widget = productFactory('Acme Widget', 1.00);
// => { name: 'Acme Widget, price: 1 }

const updatedWidget = updatePrice(widget);
// => { name: 'Acme Widget, price: 1.04 }

widget;
// => { name: 'Acme Widget, price: 1 }
````

## Lingering doubts

I still have lingering doubts, though. For one thing, making a new instance for every change seems pretty inefficient, doesn't it? And for another, what happens when my data model has nested objects as properties? Do I have to freeze those as well? It turns out, yes I do. All of the properties on my product object are immutable. But properties of nested objects can be changed. That freeze doesn't go very deep.

Maybe I can fix that by just freezing the nested objects.

````js
const productFactory = (name, price) =>
  Object.freeze({
    name,
    price,
    metadata: Object.freeze({
      manufacturer: name.split(' ')[0]
    })
  });
````

Well, that's OK, I guess. But there is still a problem here. Can you tell what it is?

What if my data model is nested several layers deep? That's not very uncommon, and now my code ends up looking something like this.

````javascript
const productFactory = (name, price) =>
  Object.freeze({
    name,
    price,
    metadata: Object.freeze({
      manufacturer: name.split(' ')[0],
      region: Object.freeze({
        country: 'Denmark',
        address: Object.freeze({
          street: 'HCA Way',
          city: 'Copenhagen'
        })
      })
    })
  });
````

Ugghh. This can start to get ugly real fast. And we haven't even started to discuss collections of objects, like `Arrays`.

Maybe my friend was right. Maybe this is a language issue.

>You feel you must "hide" it. Why? Because it's mutable, or because you must go to great lengths to make it immutable. Because JavaScript.

OK. so is this it? Should I just throw in the towel and give up on immutability in my JavaScript applications? After all, I've gone this far without it. And I didn't have _that many_ bugs. Really... I promise!

What's a coder to do? Your best bet, if you want to embrace this style fully is to write your application in Clojure or Scala or a similarly designed language where data is immutable. Immtable data is a fundamental part of the Clojure language. Instead of spending all of your time reading blog posts about fitting a square peg into a round hole, with Clojure you can just focus on writing your application and be done with it.

 But maybe that's not an option. Maybe you've got to follow company language standards. And anyway, some of us kind of do like writing code in JavaScript, so let's, for the sake of argument, take a look at some options. But first, let's just review _why_ we're going to all of this trouble.

## The case for immutability

So much of what makes software develoment hard (other than cache invalidation, and naming) has to do with state maintenance. Did an object change state? Does that mean that other objects need to know about it? How do we propagate that state across our system? There's so much bookkeeping and overhead involved in these activitites that bugs are inevitable.

If, however, we start to think a little differently, these problems begin to disappear. Instead of thinking about _objects_, if we shift our thinking about data so that everything is simply a _value_, then there is no state maintenance to worry about. Don't think of references to these values as _variables_. It's just a reference to a single, unchanging _value_.

But this shift in thinking must also affect how we structure and think about our code. Really, we need to start thinking more like a functional programmer. Any function that changes the application's state, should receive an input value, and return some mutated output value - without changing the input.

When you think about it, this constraint pretty much eliminates the need for the `class` and `this` keywords. Or at least it eliminates the use of any data type that can modify itself in the traditional sense, for example with an instance method. In this world view, the only use for the `class` keyword is namespacing your functions by making them static. And you don't need `this` at all.

````js
class Product {
  constructor () {
    throw new Error('Not allowed');
  }

  static factory (name, price) {
    return Object.freeze({
      name, price
    });
  }

  static updatePrice (product) {
    return Object.freeze(Object.assign({}, product, { price: value.price * 1.04 }));
  }
}
module.exports = exports = Product;
````

To me, that seems a little weird. Wouldn't it just be easier to stick to native data types? Especially since the module system effectively provides namespacing for us. It's a lot less code too! When we `require()` this file our product functions are namespaced by whatever name we choose to bind them to.

**`product.js`**

````js
const factory = (name, price) => Object.freeze({ name, price });

const updatePrice = (product) => Object.freeze(
  Object.assign({}, product, { price: product.price * 1.04 }));

module.exports = exports = { factory, updatePrice };
````

<hr/>

**`app.js`**

````js
const Product = require('./product.js');
Product.factory; // => [Function: factory]
Product.updatePrice; // => [Function: updatePrice]
````

Once we start thinking like this and enter the world of functional programming, there is a whole raft of topics to discuss. But for the sake of this endeavor, let's just focus primarily on immutability. As for functional programming in general, check the links at the bottom. And I'll make a note to write more blog posts, because this one is already too long.

For now, just keep these few things in mind.

  * Think of variables (or preferably `const`s) as _values_ not _objects_. A value cannot be changed, while objects can be.
  * Avoid the use of `class` and `this`. Use only native data types, and if you must use a class, don't ever modify its internal properties in place.
  * Never mutate native type data in place, functions that alter the application state should always return a copy with new values.

## Seriously, that seems like a lot of extra work

Yeah, it is a lot of extra work. And as I noted earlier, it sure seems inefficient to make a full copy of your objects every time you need to change a value. Truthfully, to do this properly, you need to be using shared [persistent data](http://en.wikipedia.org/wiki/Persistent_data_structure) structures which employ techniques such as [hash map tries](http://en.wikipedia.org/wiki/Hash_array_mapped_trie) and [vector tries](http://hypirion.com/musings/understanding-persistent-vector-pt-1) to efficiently avoid deep copying. This stuff is hard, and you probably don't want to roll your own. I know I don't.

## Someone else has already done it

Facebook has released a popular NPM module called, strangely enough, [`immutable`](https://www.npmjs.com/package/immutable). By employing the techniques above, `immutable` takes care of the hard stuff for you, and provides an efficient implementation of

> A mutative API which does not update the data in-place, but instead always yields new updated data.

Rather than turning this post into an `immutable` module tutorial, I will just show you a few interesting techniques that we can use in our examples. If you want to learn more, follow the links at the end of the post.

First let's examine our data model. The `immutable` module has a number of different data types. Since we've already seen our `Product` model as a plain old JavaScript `Object`, it probably makes the most sense to use the `Map` data type from `immutable`.

**`product.js`**

````js
const Immutable = require('immutable');
const factory = (name, price) => Immutable.Map({name, price});
module.exports = exports = { factory };
````

That's it. Pretty simple, right? We don't need an `updatePrice` function, since we can just use `set()`, and `Immutable.Map` handles the creation of a new reference. Check out some example usage.

**`app.js`**

````js
const Product = require('./product.js');

const widget = Product.factory('Acme widget', 1.00);
const priceyWidget = widget.set('price', 1.04);
const clonedWidget = priceyWidget;
const anotherWidget = clonedWidget.set('price', 1.04);

console.log(widget); // => Map { "name": "Acme widget", "price": 1 }
console.log(priceyWidget); // => Map { "name": "Acme widget", "price": 1.04 }
console.log(clonedWidget); // => Map { "name": "Acme widget", "price": 1.04 }
console.log(anotherWidget); // => Map { "name": "Acme widget", "price": 1.04 }
````

Things to take note of here: first, take a look at how we are creating the `priceyWidget` reference. We use the return value from `widget.set()`, which oddly enough, doesn't actually change the `widget` reference. Also, I've cloned `priceyWidget`. To create a clone we just need to assign one reference to another. And then, finally, an equivalent value for `price` is set on `clonedWidget` to create yet another value.

## Value comparisons

Let's see how equality works with these values.

````js
// everything but 'widget' has a price of 1.04
// so 'widget' is not equivalent to any of them
assert(widget !== priceyWidget);
assert(widget !== clonedWidget);
assert(!widget.equals(priceyWidget));
assert(!widget.equals(clonedWidget));
assert(!widget.equals(anotherWidget));
````

This all makes some intuitive sense. We create a `widget` and when we modify it, the return value of the mutative function provides us with a new value that is not equivalent as either a reference or value. Additional references to the new value instance `priceyWidget` are also not equivalent.

But what about comparisons between `priceyWidget` and its clone. Or `priceyWidget` and a mutated version of the clone that actually contains all of the same property values. Whether we are comparing references with `===` or using the deep `Map.equals`, we find that equivalence holds. How cool is that?

````js
// priceyWidget is equivalent to its clone
assert(priceyWidget === clonedWidget);
assert(priceyWidget.equals(clonedWidget));

// It's also equivalent to another, modified value
// because, unlike setting a new value for 'price'
// to create 'priceyWidget', this modification didn't
// actually change the value.
assert(priceyWidget === anotherWidget);
assert(priceyWidget.equals(anotherWidget));
````

## This is just the beginning

There is a lot of territory to cover with the `immutable.js` package, which I won't get into here. But I encourage you to read futher. Topics such as nested data structures, merging data from multiple values, and collections are all worth exploring. Find below links for additional reading.

* `immutable.js` documentation: http://facebook.github.io/immutable-js/docs/#/
* Persistent data structures: http://en.wikipedia.org/wiki/Persistent_data_structure
* Hash map tries: http://en.wikipedia.org/wiki/Hash_array_mapped_trie
* Vector tries: http://hypirion.com/musings/understanding-persistent-vector-pt-1