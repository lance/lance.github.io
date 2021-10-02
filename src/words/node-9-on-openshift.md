---
title: Node.js 9.x on OpenShift
layout: article.jade
date: 2017-11-07
draft: true
---
# Running Node.js 9.x on OpenShift

Sometimes it's nice to be able to play with the newest and most
cutting edge tools when you're developing an application. So it
goes with the latest major version bump to Node.js 9.0.0. There
are some nice features to the latest release line, as well as in
the newly released LTS version 8.9.0. Both of these new Node
releases now include V8 6.1. "The new V8 engine comes with Turbofan
and the Ignition pipeline, which leads to lower memory consumption
and faster startup time across Node.js applications"
[\*](https://medium.com/the-node-js-collection/news-node-js-8-moves-into-long-term-support-and-node-js-9-becomes-the-new-current-release-line-74cf754a10a0).
If that's not enough for you, now HTT2 is no longer hidden
behind a flag. For these and other reasons, you should give the new
Node.js versions a spin. Here's how you can run your shiny new 9.0.0
(or 8.9.0) application on OpenShift.

## A Basic Application Skeleton

Let's start with a simple [express.js](https://expressjs.com)
application. I will use this for my example because it's very easy
to get a project created and running by using the generator
tool. First install the `express-generator` command line tools
to your global NPM repository.

```sh
$ npm install -g express-generator
```

Then you can create a new project using the generator. For now, let's
not worry about any of the application logic. The generator will do
enough to get us going quickly, and we can add logic and persistence
to our application later.

```sh
$ express --view=pug my-todos
```

You should see in the terminal what files the command creates, and
how to start the server.  After running `npm install` and `npm start`, you can open your a browser window to http://localhost:3000.
The generator creates a simple web application with two routes:
`/` and `/users`. As you can see, there is not much to these
generated routes. Application logic will be left as an exercise for
you.

## Deploying to OpenShift

OK - so this is all well and good, but it's nothing different, really,
than what you can find on the Express.js website. Running the app
locally is nice, but what we're here for is learning how to run this
thing on OpenShift - specifically using Node.js 9.0.0.

### Minishift

One of the neat things about OpenShift is that it doesn't just run
in the cloud as a PaaS. You can also run OpenShift locally on your
laptop by using a tool called [`minishift`](https://github.com/minishift/minishift/). If you don't
already have it installed, you can download it
[here](https://github.com/minishift/minishift/releases). Follow the
[instructions](https://github.com/minishift/minishift/blob/master/README.adoc#getting-started) to install it for your operating system, and
then start it up with the appropriate command for your environment.
Here is the command to start `minishift` on OSX using VirtualBox
as the virtual machine driver, giving it a little extra memory.

```sh
$ minishift start --memory=4096 --vm-driver=virtualbox
```

The first time you run `minishift` it will take a little while to
start up. It needs to pull a number of Docker images, and depending
on your connection speed this could be time consuming. Once minishift
startup has completed, you should see something like this in your
terminal.

```sh
Starting OpenShift using openshift/origin:v3.6.0 ...
OpenShift server started.

The server is accessible via web console at:
    https://192.168.99.100:8443
```

Browse to that URL, or just type `minishift console` on the command
line, and you should see a fully functional OpenShift instance running
on your laptop. Woot!

When you start `minishift` you are automatically logged in to your
local OpenShift instance using the `developer` account. But if you
open another terminal, you'll need to login there as well. You can
login using the `oc` tool that is shipped with `minishift`. First
run `$ minishift oc-env` and follow the instructions. Then run:

```sh
$ oc login -u developer
```

The OpenShift web console is shipped as a part of `minishift`.
Log in to the console with the username and password `developer`
to see your default project in place. Now, let's look at how
we can deploy our simple Express.js application to our local
`minishift`.

### Nodeshift

Nodeshift is a command line application that you can use to deploy
Node.js projects to OpenShift. It's currently under heavy development
and APIs are still shifting a bit. However, in spite of its beta
nature, you can use `nodeshift` today to deploy Node.js applications
to OpenShift.

Install `nodeshift` in your project.

```sh
$ npm install --save-dev nodeshift
```

This will add `nodeshift` as a developent dependency in `package.json`.
Now let's add a `deploy` command. Open the `package.json` file
and add this line to the `scripts` section.

```json
"deploy": "nodeshift --osc.strictSSL=false"
```

The `osc.strictSSL` flag is used to tell `nodeshift` that it's OK if
the host we are deploying to has a self-signed security certificate.
In this case, we're just deploying to our local `minishift` instance
so it's expected.

`nodeshift` works its magic through a combination of YAML configuration
files which describe the deployment, and a
[source to image](https://github.com/openshift/source-to-image)
"builder"
[image](https://hub.docker.com/r/bucharestgold/centos7-s2i-nodejs/).
Our application source code is applied on top of this builder image
to create the runtime container for the application. `nodeshift`
defaults to using the `latest` tag from the
`bucharestgold/centos7-s2i-nodejs` builder image which currently
provides Node.js 9.0.0. However, if you would like to
stick to an LTS version, you can specify this in the `nodeshift`
command. Change your script to look something like this.

```json
"deploy": "nodeshift --osc.strictSSL=false --nodeVersion=Carbon"
```

You can specify a version line like `8.x` or an LTS tag like `Carbon`.
In either case, `nodeshift` will use this as the tag when pulling the
s2i Docker image.

Next, we'll need to configure `nodeshift` using some simple YAML
files that provide deployment metadata. By default, `nodeshift` will
create a `BuildConfiguration` for us, but to really deploy the
application, we'll want to tell openshift what to do with that
build. Create three YAML files in a `.nodeshift` directory
in your project. They should look like this.

<label>deployment.yaml</label>
```yaml
apiVersion: v1
kind: Deployment
metadata:
  name: my-todos
spec:
  template:
    spec:
      containers:
        - env:
          - name: PORT
            value: "8080"
```
<label>svc.yaml</label>
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-todos
spec:
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
  type: ClusterIP
```
<label>route.yaml</route>
```yaml
apiVersion: v1
kind: Route
metadata:
  name: my-todos
spec:
  port:
    targetPort: 8080
  to:
    kind: Service
    name: my-todos
```

These three files tell `nodeshift` all it needs to know to deploy
your application to OpenShift and expose it over port 8080. In my
next post, we will dig a little deeper into these configuration
files so you know exactly what's going on. For now, you can just
copy and paste them into your project in the `.nodeshift` directory.

Run the NPM script we created earlier.

```sh
$ npm run deploy
```

If all goes well, you should now have your Express.js application
running in your local `minishift` instance. One of the final lines
of output from this command should look something like this.

```log
2017-11-06T19:28:52.892Z INFO route host mapping my-todo-myproject.192.168.99.100.nip.io
```

You should be able to open your browser to port 8080 at that URL
and see your running application. Or instead, just run
`minishift console` on the command line.

### OpenShift Online

Deploying your application to `minishift` is a good way to test how
the application will behave when running in a cloud environment, but
`minishift` is not where your application will ultimately be deployed.
Ultimately, you'll want to push your application to a production
OpenShift environment. This is easy to do. It just requires logging
into the remote OpenShift on the command line. When you next execute
`$ npm run deploy`, your application will be deployed to the remote
OpenShift instance.

For example:

```sh
$ oc login https://console.starter-us-east-2.openshift.com -u lba11@redhat.com
# login succeeds, then run
$ npm run deploy
# application is deployed to remote OpenShift
$ oc get pods
NAME                   READY     STATUS      RESTARTS   AGE
my-todos-1-n973l       1/1       Running     0          2m
my-todos-s2i-1-build   0/1       Completed   0          4m
```

## Recap

So that's about it for this quick introduction. To review, we
created a simple Express.js application, added a `.nodeshift`
directory to the project, created OpenShift configuration files
to describe our application's deployment, and in a single command
line deployed the application to whichever OpenShift instance
we were logged into, running on Node.js 9.0.0.
It was all pretty quick and painless. But
I'll admit that I glossed over many of the details. In future
posts, I will explore some of the powerful Kubernetes/OpenShift
features that Nodeshift exposes. For now, happy coding!
