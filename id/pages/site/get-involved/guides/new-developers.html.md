 Panduan Pengembang
Baru 2021-01 

1. [Get to Know Java](#basic-study)
2. [Getting the I2P code](#getting-the-i2p-code)
 - [The new way: Git](#git)
3. [Building I2P](#building-i2p)
4. [Development ideas](#development-ideas)
5. [Making the results available](#making-the-results-available)
6. [Get to know us!](#get-to-know-us)
7. [Translations](#translations)
8. [Tools](#tools)

 

So you want to start work on I2P? Great! Here\'s a quick guide to
getting started on contributing to the website or the software, doing
development or creating translations. 

The I2P router and its embedded applications use Java as the main
development language. If you don\'t have experience with Java, you can
always have a look at [Thinking in
Java](http://www.mindview.net/Books/TIJ/).

Study the [how intro](), the [other \"how\"
documents](), the [tech
intro](), and associated documents. These
will give you a good overview of how I2P is structured and what
different things it does.

## Getting the I2P code

For development on the I2P router or the embedded applications, you need
to get the source code:

### Our current way: Git {#git}

I2P has official Git services and accepts contributions via Git at [our
own gitlab](). Trac issues have also been migrated
to Git issues. Two-way syncing of issues between Gitlab and Github is a
work-in-progress.

Install [Git]().

- **[Di dalam I2P - (http://git.idk.i2p)](http://git.idk.i2p)**
- **[Di luar I2P - (https://i2pgit.org)](https://i2pgit.org)**

The read-only mirror is also still available at github.

- **[GitHub mirror]()**:\
 `git clone https://github.com/i2p/i2p.i2p.git`

## Building I2P

To compile the code, you need the Sun Java Development Kit 6 or higher,
or equivalent JDK ([Sun JDK 6]() strongly
recommended) and [Apache ant](http://ant.apache.org/) version 1.7.0 or
higher. If you go are working on the main I2P code, you can go into the
i2p.i2p directory and run \'ant\' to see the build options.

To build or work on console translations, you need the xgettext, msgfmt,
and msgmerge tools from the [GNU gettext
package](http://www.gnu.org/software/gettext/).

For development on new applications, see the [application development
guide]().

## Development ideas

See [the project TODO list]() or [the issue list
on GitLab]() for ideas.

## Making the results available

See the bottom of [the licenses page](#commit)
for commit privilege requirements. You need these to put code into
i2p.i2p (not required for the website!).

## Get to know us!

The developers hang around on IRC. They can be reached on the Freenode
network, OFTC, and on the I2P internal networks. The usual place to look
is #i2p-dev. Join the channel and say hi! We also have [additional
guidelines for regular developers]().

## Translations

Website and router console translators: See the [New Translator\'s
Guide]() for next steps.

## Tools

I2P is open source software that is mostly developed using open sourced
toolkits. The I2P project recently acquired a license for the YourKit
Java Profiler. Open source projects are eligible to receive a free
license provided that YourKit is referenced on the project web site.
Please get in touch if you are interested in profiling the I2P codebase.

YourKit is kindly supporting open source projects with its full-featured
Java Profiler. YourKit, LLC is the creator of innovative and intelligent
tools for profiling Java and .NET applications. Take a look at
YourKit\'s leading software products: [YourKit Java
Profiler]() and [YourKit .NET
Profiler]().


