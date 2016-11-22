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

We'll ignore his little dig on the language itself. But maybe what he's saying has some value? I do like the idea of a bunch of "stress just falling away". Let's look at where we ended up in that last post about data encapsulation.

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

But rats, now I have to replace every `this.name` with `this[NAME]` using a `Symbol` for the property key. And like my friend said, these proerties are arguably useful in userland. I just don't want them changed. I want **immutability**. How can I do this using JavaScript?

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

What about those situations where you really _need_ to mutate your objects. What if, for example, there's a `price` property that could change over time? Normally, we'd do something super simple. Like just update the price. `this.price = getUpdatedPrice(this);`.

But of course, if we're going for immutability and the safety that comes along with that, then this is clearly not the corret approach.  So, what can we do about it? One approach might be to use `Object.assign()` to copy properties from one object to another, always generating a new object for every data mutation. Perhaps something like this.

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

But how can I do that? The constructor really is the only place that makes sense. I could use a factory function to return instances of `Product`. Or to simplify things even more, I guess we could change our data model to not use a class at all. For the sake of experimentation, let's give it a shot. Maybe the plain old JavaScript objects are all we need.

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
````

## Lingering doubts

I still have lingering doubts, though. For one thing, making a new instance for every change seems pretty inefficient, doesn't it? And for another, what happens when my data model has nested objects as properties? Do I have to freeze those as well? It turns out, yes I do. All of the properties on my product object are immutable. But properties of nested objects can be changed. That freeze doesn't go very deep. I guess I can fix that by just freezing the nested objects.

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

Ugghh. This can start to get ugly real fast.

Maybe my friend was right. Maybe this is a language issue.

>You feel you must "hide" it. Why? Because it's mutable, or because you must go to great lengths to make it immutable. Because JavaScript.

OK. so is this it? Should I just throw in the towel and give up on immutability in my JavaScript applications? After all, I've gone this far without it. And I didn't have _that many_ bugs. Really! I promise!