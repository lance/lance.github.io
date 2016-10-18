const metalsmith = require('metalsmith');
const layouts = require('metalsmith-layouts');
const markdown = require('metalsmith-markdown');
const pug = require('metalsmith-pug');
const serve = require('metalsmith-serve');
const watch = require('metalsmith-watch');
const msIf = require('metalsmith-if');
const permalinks = require('metalsmith-permalinks');
const collections = require('metalsmith-collections');
const excerpts = require('metalsmith-better-excerpts');
const gist = require('metalsmith-gist');
const branch = require('metalsmith-branch');
const feed = require('metalsmith-feed');
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
  const now = new Date();

  Error.stackTraceLimit = 100;
  metadata.devMode = serveAndWatch;

  metalsmith(__dirname)
    .metadata(metadata)
    .source('./src')
    .destination('./build')

    // easy gist insertion
    .use(gist({
      caching: false
    }))

    // write blog posts in markdown
    .use(markdown())

    // allow for draft posts
    .use(drafts)

    // for the listing of posts
    .use(excerpts({
      pruneLength: 40,
      stripTags: false
    }))

    // let's write a blog!
    .use(collections({
      articles: {
        pattern: 'words/**.html',
        sortBy: 'date',
        reverse: true
      }
    }))

    .use(branch('words/**.html')
      // use permalinks for blog posts
      .use(permalinks({
        match: { collection: 'articles' },
        pattern: 'words/:date/:title'
      })))

    // Index page is pug
    .use(pug({
      useMetadata: true
    }))

    // Pug templates
    .use(layouts({
      engine: 'pug',
      moment: moment
    }))

    // RSS Feed
    .use(feed(
      {
        collection: 'articles',
        pubDate: now,
        postDescription: (file) => file.excerpt || file.contents,
        copyright: `Lance Ball ${now.getFullYear()}`,
        description: 'Occasional musings of a crotchety old developer',
        language: 'en-us',
        categories: ['programming', 'javascript', 'node.js', 'coding'],
        site_url: 'http://lanceball.com'
      }
    ))

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
  Object.keys(files).forEach(f => {
    if (files[f].draft) delete files[f];
  });
  done();
}

function publish () {
  if (process.argv[2] !== 'publish') return;

  const ghpages = require('gh-pages');
  const path = require('path');
  const options = {
    branch: 'master',
    repo: 'https://github.com/lance/lance.github.io.git',
    dotfiles: true
  };

  console.log('Publishing build dir to master');

  ghpages.publish(path.join(__dirname, 'build'), options, (err) => {
    if (err) {
      console.error(`Cannot publish site. %{err}`);
      throw err;
    } else {
      console.log('Site published.');
    }
  });
}
