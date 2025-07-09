# abbsolve

[![codecov](https://codecov.io/gh/anthonylabarga/abbsolve/graph/badge.svg?token=2O2COINS7F)](https://codecov.io/gh/anthonylabarga/abbsolve)

`abbsolve` is an abbreviation, initialism, and acronym resolver and
inverter.

This package is designed to construct jargon dictionaries, especially
in large organizations where ambiguous initialisms are used in regular
communication. Such organizations often *attempt* to keep wiki pages
or other internal lingo dictionaries, but this is rarely a
high-priority task and they rarely stay fresh for long.

This package is specifically designed to help in cases where people
keep saying things like "make sure to connect the ABC to the XYZ", and
it's not clear what those things refer to. If you've been in a
situation like that where you didn't want to stop a meeting to ask
what those terms stand for, then I built this for you. If someone asks
you for a "rundown" and you don't know what that is, then this package
probably won't help you.

`abbsolve` works by finding semantically-related initialisms and
corresponding full-text terms using a body of text from the context or
organization where those terms occur. It runs entirely on your machine
and makes no use of large language models (LLMs).

## Roadmap

### v0.0.1

- [X] `grep`-based brute force calculation of inversion candidates
- [ ] initial performance optimization for large datasets

### v0.1.0

- [ ] CLI version for terminal use
- [ ] word2vec-based expansion ranker

### v0.2.0

- [ ] transformer-based expansion ranker