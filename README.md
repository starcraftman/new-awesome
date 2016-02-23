# New Awesome

A site similar to vim-awesome.
The purpose is to collect, showcase and discover all the available plugins.

Key features:
- Trying to be fully tested with travis build.
- Focus on community editting/contributing instead of scraping.
- Easily fetched/parsed json for plugin managers to use.

See [DESIGN.md] for more details.

## Demo

Provision a testbed with vagrant and then connect:
```sh
vagrant up
vagrant ssh
```
Once done, you will be in `/vagrant` the project root.
Execute `awe -h` to inspect the small utility controlling the site or execute tests.

It is very much early, so it doesn't do much yet.

## Inspiration

- [vim-awesome]: Awesome project built with datamining. I may lift some features.
- [plug-search]: My own plugin, lacking an appropriate database to be useful.

<!-- Links -->
[DESIGN.md]: https://github.com/starcraftman/new-awesome/blob/master/DESIGN.md
[plug-search]: https://github.com/starcraftman/plug-search
[vim-awesome]: https://github.com/divad12/vim-awesome
