---
title: Protect Your Node.js REST Clients with Circuit Breakers
layout: article.jade
date: 2017-01-05
draft: false
staging: false
---

One of the predominant patterns in today's Node.js applications
is the microservice, or µ-service. Applications are composed of a
suite of independently deployable services, usually running in
independent processes. These µ-services typically communicate with
each other using lightweight protocols such as REST over HTTP.

One of the side effects of this architecture, however, is that applications
need to be designed to handle failure. Any one of the service calls could
fail for any number of reasons at any time. Today, I'll explore one method
you can employ to gracefully handle service unavailability &mdash; the
Circuit Breaker pattern.

<!-- More -->

## Scenario

Let's imagine an application, built on µ-services. Clients connect to the
application through some kind of load balancer, and requests are then routed
to a set of containers, each running multiple Node.js server processes. Those
processes, in turn, depend on several µ-services not exposed to the clients.

<img src="/images/circuit-breaker-1.png" style="float: left"/>

In the diagram shown, services `B` and `C` are starting to become flakey, take too
long or outright fail. What's worse, service `A` depends on `B` and `C` to do
its job, and the problems on `B` &amp; `C` are beginning to cascade, causing requests
to service `A` to time out. This cascading failure then works its way up to the
Node.js server processes, causing them to timeout or fail. All of this is chewing
up valuable resources and almost certainly resulting in an unpleasant experience
for the end user.

To avoid these kinds of scenarios, circuit breakers allow us to easily monitor
the state of our service dependencies. When a service begins to fail too
frequently, the circuit will open and the client will go into fallback or
fail-fast mode, avoiding calls to the faulty service altogether for a while,
allowing it some time to recover. After a configurable timeout period,
the circuit breaker will enter the `halfOpen` state. In this state, it will
make a single call to the faulty service. If that call is successful, the
circuit will close and clients will resume as normal. However,
if the call to the service while in the `halfOpen` state fails, the circuit will
immediately open again, preventing further requests to the service.

## Example Code

There are a few different circuit breaker implementations for Node.js currently
published. For this example, we'll be using [Opossum](https://npmjs.com/package/opossum).
One of the nice features of this implementation is that it works well both with
`Promise`s and standard Node.js-style calllback functions. Additionally, Opossum
works both as a Node.js package and in the browser. We'll look at examples of all
of these.

### Networking with Circuit Breakers and Promises

Let's say `Service A` provides a simple REST service that exposes a user's
unread message count. When a user is logged in, the server is periodically
polled for this count, generating a `GET` request from the front-end server
to the service URL at `https://service-a.local/messages/[userid]/unread`.

The first thing we need to do is set up our circuit so that it can make a
simple HTTP GET call. In this case, we are using a client package
called `roi` which will perform an HTTP GET request for a given endpoint
and return a Promise.

We also provide a simplified fallback function that returns a resolved
Promise with a friendly error message.

<p class="filename"><code>app.js</code></p>
```js
const circuitBreaker = require('opossum');
const client = require('roi');

const circuit = circuitBreaker(client.get);

circuit.fallback(() => Promise.resolve({
  error: 'Unread messages currently unavailable. Try again later'
}));
```

Next, let's create a function to get a user's
unread messages. Here we fire the circuit, passing it parameters for
the call to `client.get()` which is the circuit's action. Since Opossum
uses a `Promise` API, we manage our flow control with `then()` and `catch()`,
each of which accepts a function. If the call is successful, or if the
fallback function is executed, the `then` function is applied. In the
event of an error, the `catch` function is applied.

```js
function getUnreadMessages (req, resp) {
  return circuit.fire({
    endpoint: `https://service-a.local/messages/${getUserId(req)}/unread`
  })
  .then((messages) => sendResponse(resp, messages))
  .catch((err)     => sendError(resp, err))
}
```

Then we configure our HTTP server. I don't show the full server setup here,
just the parts we care about right now. Let's create a route to `/messages/unread`
that fires the circuit.

```js
// set up the server routes. use whatever server you like - here it's hapi
server.route({
  method: 'GET',
  path: '/messages/unread',
  handler: (req, resp) => getUnreadMessages(req, resp)
});
```

And that's it. Now, when our web server makes a call to `Service A`, if that
service starts failing or timing out, we can handle those failures gracefully.

### Circuit Breakers with Node.js Callbacks

OK, well that's all fine and dandy, but not everything uses Promises.
Consider, for example, file system operations in Node.js. These async
calls might easily fail. No worries, it's simple to add a circuit breaker
to these calls by using Opossum's `promisify` function.

<p class="filename"><code>config.js</code></p>
```js
const fs = require('fs');

const readFile = circuitBreaker.promisify(fs.readFile);
const circuit = circuitBreaker(readFile);

// read the config file - use defaults if it's not available
breaker.fire('./app.config')
  .then((data) => processConfig(data))
  .catch((err) => useDefaults(err));
```

### JQuery AJAX calls with Circuit Breakers

Circuit breakers can be very useful in the browser for handling remote
asynchronous calls. It's pretty simple to wire up your AJAX calls to use
the circuit breaker pattern, freeing them from convoluted error handling,
duplicated code, and flakey backend services.

Start by adding the `opossum-min.js` file to your HTML document.

<p class="filename"><code>index.html</code></p>
```html
<script type='text/javascript' src="/opossum-min.js"></script>
```

Next, install opossum
and add it to package.json with the `--save` option.

```shell
npm install --save opossum
```

The browserified files will be in `node_modules/opossum/dist/opossum[-min].js`.
Then you'll need to let your server know where to find it.

Set a route to the browserified file. In this example, I'm using Hapi.js
but most (all?) Node.js server frameworks provide some mechanism for serving
static files for a given route.

<p class="filename"><code>server.js</code></p>
```js
server.route({
  method: 'GET',
  path: '/opossum.js',
  handler: {
    file: {
      path: path.join(__dirname, 'node_modules', 'opossum', 'dist', 'opossum-min.js'),
    }
  }
});
```

When the browser loads the `opossum-min.js` file, a `circuitBreaker` function will
become available in the global scope. You can use it to create circuit breakers
that guard against your JQuery AJAX calls.

<p class="filename"><code>app.js</code></p>
```js
const route = 'https://example-service.com/rest/route';

const circuit = circuitBreaker(() => $.get(route));
circuit.fallback(() => `${route} unavailable right now. Try later.`));
circuit.on('success', (result) => $(element).append(JSON.stringify(result)}));

$(() => {
  $('#serviceButton').click(() => circuit.fire().catch((e) => console.error(e)));
});
```

### Circuit Events

Opossum provides a number of events you can listen for so that
you can effectively log or otherwise more finely control the behavior of the
circuit. An example might be that we'd like to log an error message each time
our fallback function is applied.

```js
circuit.on('fallback', logError);
```

Or send a notification to some poor sysadmin every time the circuit opens.

```js
circuit.on('open', sendOpenNotification);
```

For more information on the many events you can listen for, documentation about
the configuration, and the overall API, please refer to the [documentation for
opossum](https://bucharest-gold.github.io/opossum/).

## Further Reading

If you are unfamiliar wtih the µ-service pattern and want to learn more
there are plenty of good resources on the web. Here are a couple of places
you might want to start.

* [CircuitBreaker](http://www.martinfowler.com/bliki/CircuitBreaker.html) - Martin Fowler
* [Making the Netflix API More Resilient](http://techblog.netflix.com/2011/12/making-netflix-api-more-resilient.html) - Netflix Blog
* [Fault Tolerance in a High Volume Distributed System](http://techblog.netflix.com/2012/02/fault-tolerance-in-high-volume.html) - Netflix Blog

Opossum itself was inspired by a few different existing circuit
breaker implementations in Node.js. Here are a couple that were particularly
useful for study.

* Levee - https://github.com/krakenjs/levee
* node-circuitbreaker - https://github.com/ryanfitz/node-circuitbreaker
* circuit-breaker-js - https://www.npmjs.com/package/circuit-breaker-js