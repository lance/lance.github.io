const metalsmith = require('metalsmith');
const layouts = require('metalsmith-layouts');
const markdown = require('metalsmith-markdown');
const jade = require('metalsmith-jade');
const less = require('metalsmith-less');
const serve = require('metalsmith-serve');
const watch = require('metalsmith-watch');
const msIf = require('metalsmith-if');
const permalinks = require('metalsmith-permalinks');
const moment = require('moment');
const fs = require('fs');

moment.locale('en', {
  calendar: {
    lastDay: '[Yesterday, ] MMM Do',
    sameDay: '[Today, ] MMM Do',
    lastWeek: '[last] dddd[, ] MMM Do',
    sameElse: 'll'
  }
});

build();

function build () {
  const serveAndWatch = process.argv.length > 2 && process.argv[2] === 'serve';
  const metadata = JSON.parse(fs.readFileSync('./site.json', 'utf8'));

  Error.stackTraceLimit = 100;
  metadata.devMode = serveAndWatch;

  metalsmith(__dirname)
    .metadata(metadata)
    .source('./src')
    .destination('./build')

    // Write pages in markdown
    .use(markdown())
    .use(jade())

    // use less for css
    .use(less())

    // Jade templates
    .use(layouts({
      engine: 'jade',
      moment: moment
    }))

    // allow for draft posts and permalinks
    .use(drafts)
    .use(permalinks({
      pattern: ':title'
    }))

    // when we run as `node build serve` we'll serve the site and watch
    // the files for changes. Note: This does not reload when templates
    // change, only when the content changes
    .use(msIf(
      serveAndWatch,
      watch({
        pattern: '**/*',
        livereload: false
      })))

    .use(msIf(
      serveAndWatch,
      serve({
        port: 8080,
        verbose: true
      })))

    .build(err => {
      if (err) {
        console.log(err);
        throw err;
      } else {
        console.log('Site build complete.');
        publish();
      }
    });
}

function drafts (files, metalsmith, done) {
  files.forEach(f => {
    if (files[f].draft) delete files[f];
  });
  done();
};

function publish () {
  if (process.argv[2] === 'publish') return;

  const ghpages = require('gh-pages');
  const path = require('path');
  const options = {
    branch: 'master',
    repo: 'https://github.com/lance/lance.github.io.git',
    dotfiles: true
  };

  ghpages.publish(path.join(__dirname, 'build'), options, (err) => {
    if (err) {
      console.error(`Cannot publish site. %{err}`);
      throw err;
    } else {
      console.log('Site published.');
    }
  });
}
