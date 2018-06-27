# Tutorial 1: Hello, csmake!

In this tutorial, you'll learn the basics of how csmake operates to construct a desired result.  In order to keep the tutorial easy to follow and execute, some of the finer points for this tutorial are reserved for the appendix at the end.

## Goals for this Tutorial

* Gain a basic understanding of how to start a csmake project from scratch
* Understand the basic operation of a csmakefile specification and csmake
* Learn how to set up a basic build using csmake

## Step 1: Ensure csmake is installed
For this tutorial, you only need to have csmake installed.  If you haven't done this yet, please do this now.

## Step 2: Create a new directory to do the tutorial
```
mkdir csmake-tutorial-1
cd csmake-tutorial-1
```

## Step 3: Create a csmakefile
Open an editor and enter the following text:

```
[Shell@hello]
command= echo "Hello, csmake!"
 
[command@]
0000=hello
```

Save this file as "csmakefile".  This defines a build that executes a shell script that echoes: Hello, csmake!.  See "Understanding the csmakefile" below.

## Step 4: Execute csmake
```
csmake build
```

You should see:
```
___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
     Begin csmake - version 1.3.1
------------------------------------------------------------------
` WARNING  : Phase 'build' not delcared in ~~phases~~ section
` WARNING  :   Run: csmake --list-type=~~phases~~ for help
       _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
    ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
    `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'
         BEGINNING PHASE: build
__________________________________________________________________
  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (
------------------------------------------------------------------
+ command@      ---  Begin
------------------------------------------------------------------
__________________________________________________________________
  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (
------------------------------------------------------------------
++ Shell@hello      ---  Begin
------------------------------------------------------------------
Hello, csmake!
------------------------------------------------------------------
 nununununununununununun   Step: Passed   nununununununununununun
------------------------------------------------------------------
++ Shell@hello      ---  End
------------------------------------------------------------------
__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)
------------------------------------------------------------------
 nununununununununununun   Step: Passed   nununununununununununun
------------------------------------------------------------------
+ command@      ---  End
------------------------------------------------------------------
__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)
         ENDING PHASE: build
       _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
    ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
    `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'
` WARNING  : Phase 'build' not delcared in ~~phases~~ section
` WARNING  :   Run: csmake --list-type=~~phases~~ for help
   SEQUENCE EXECUTED: build
------------------------------------------------------------------
  .--.      .--.      .--.      .--.      .--.      .--.      .--.      .
:::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::
'      `--'      `--'      `--'      `--'      `--'      `--'      `--'
     csmake: Passed
------------------------------------------------------------------
     End csmake - version 1.3.1
------------------------------------------------------------------
 ___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
```

If you execute csmake with the --quiet option, like this:
```
csmake --quiet build
```

Then you will see:
```
Hello, csmake!
```

The `--quiet` option suppresses all csmake output.

### Tutorial 1 Appendix

This appendix is designed to help gain a finer understanding of the reasons why the above steps worked, and what you can do to get a better understanding of how csmake operates.

#### Understanding the csmakefile

The csmakefile is a Python "INI" style file.  Just like with an INI file, a csmakefile has sections and key-value pairs for each section.

The csmakefile has a slightly more specific format than a regular "INI" file. For example, each section definition is of the form:
```
[<section type>@<id>]
```

The *\<section type\>* is implemented by a specific kind of python module that has been defined in a CsmakeModules directory (later tutorials will explore how CsmakeModules directories work).  The *\<id\>* is simply just a handle to allow you to distinguish between sections of identical type and for ease of reference.

Note that csmakefiles are declarative, that is, their purpose (like with SQL, for example) is simply to state what should happen.  Everything must fully declare what the build is expected to do.  There's no hidden behavior or special rules to shoehorn the tool into doing something special.  Everything in the specification has been defined as a module, including "control structure" sections such as "command" as seen above.

The key-value pairs provided under a given section are consumed by the section type module implementation.  These key-value pairs are extremely free-form, which makes it easy to express just about anything that is necessary to express in a csmakefile.  This, however, can also make csmakefiles feel unwieldy as it appears that the form, structure, and syntax of a csmakefile will ebb and flow from bash to python to expressions and syntax unique to individual sections whilst keeping with the "INI" type key-value basic syntax.

In an INI file, a key must start in the first column, not contain spaces, and be followed by an '=' (equals) sign.  If any one of these conditions are not met, the line in the csmakefile specification will be part of the previous key.  For example:
```
[MySectionType@my]
single_line=This is a value passed in for 'my'
multi_line= This is
 another=value
 *   passed in
 to the section 'my'
```
The single\_line result that the section implementation sees is literally "This is a value passed in for 'my'"

The multi\_line result that the section implementation sees is literally:
```
 "This is\nanother=value\n*   passed in\nto the section 'my'"
```
Notice first, that any leading and trailing white space for a multiline value is discarded.  There are times when the whitespace can be meaningful, so use of a delimiter like '\*' as seen above, is used to keep the left side spacing correct (putting a patch inline or, say, python code in a build specification may require the use of a left hand side delimiter to denote where the left hand side of the lines start and process the contents based on this as necessary.

As mentioned above, the syntax of the csmakefile itself is very regular and specific, but is also extremely flexible, allowing for bash scripts, next to simple string input, next to some python code.  Even though it may make a csmakefile confusing at first glance, this is one of the strengths of the tool: the ability to express and pull together all of the parts and processes of a complex build into a single specification.

Every section specified in the csmakefile has documentation associated with it that can be accessed using --list-type.  For example:
```
csmake --list-type=Shell
```

will list the documentation for the "Shell" module.  You can also list all of the available types using "--list-types".  The documentation for the sections available from the current working directory will be output in (ASCII) alphabetical order, meaning capital lettered sections will be listed before lower case sections.  By convention, the "core" csmake sections should all start lowercase, thus listed at the end of the --list-types output.  Some examples of these special sections include: command, subcommand, include, metadata, and versioning.

An individual section type's documentation may be accessed using `--list-type`

Here's a full example of requesting the documentation for one of the most key modules, command:

```
$ csmake --list-type=command

___________________________________________________
Section Type: command
Path:         /usr/lib/python2.7/dist-packages/Csmake/CsmakeModules
----Info----
Library: csmake
Purpose: Execute a series of build steps - the initial step is
         a command seeded by the command line input (see --command)
Phases: *any*
Options: The keys are used to order the steps lexicographically
       1, 10, 2, 20, 200, 3, A, a (suggestion use 00-99)
       The values are atomic groups of steps
          , - denotes step follows the next
          & - denotes steps that can be run in parallel
Example:
    [command@build]
    description = "This will build a small pond"
    00 = init
    01 = repo1 & repo2 & repo3, repo4
    02 = createPond
    03 = stockFish
```

#### Understanding the csmake Command Line

The basic csmake command line structure is:
```
csmake <flags> <phases>
```

where `<flags>` are the list of flags (use `--help` for a listing of possible flags) and `<phases>` is one or more build phases (which are specific to the csmakefile used, and if defined in the csmakefile explicitly, can be listed using `--list-phases`).

##### The --command Flag

The executed entry point for processing in csmake is defined using the
`--command` flag.

"command" sections in the csmakefile define which entrypoints are expected
in a csmakefile.

The default command in a csmakefile when the command flag is omitted from
the command line is:

```
[command@]
```

If an id-less command section is not found, the next target is:

```
[command@default]
```

If this is also not defined, csmake will take a command section of its choosing
and execute that section (this is not suggested practice).

The goal should be for the csmakefile developer to have the default command
do what your developer would expect to be the most helpful thing.

All available commands may be listed by using the `--list-commands` flag on the command line.  Here's an example from a very complex csmakefile:

```
$ csmake --list-commands
 
================= Defined commands =================
    local - Setup a local build - must be used with an appliance build
e.g., --command=local, base-foundation
    jenkins - Setup a jenkins build - must be used with an appliance build
e.g., --command=jenkins, base-foundation
    rc - Setup an rc build - must be used with an appliance build
    pr - Setup a partner release build - must be used with an appliance build
    base-mgmt - Create a first phase base image for the management appliance
    base-foundation - Create a first phase base image for the foundation appliance
    base-enterprise - Create a first phase base image for the enterprise appliance
    partner-enterprise - Create a second (partner) phase image for the enterprise appliance
    base-swift - Create a first phase base image for the swift appliance
    base-monasca - Create a first phase base image for the monasca appliance
    base-update - Create a first phase base image for the update appliance
    base-sdn - Create a first phase base image for the sdn appliance
    mgmt - Create a management appliance from a base management image
    foundation - Create a foundation appliance from a base foundation image
    enterprise - Create a enterprise appliance from a base enterprise image
    swift - Create a swift appliance from a base swift image
    monasca - Create a monasca appliance from a base monasca image
    update - Create an update appliance from a base swift image
    sdn - Create an sdn appliance from a base swift image
    local-base-mgmt - (Local) Create a first phase base image for the management appliance
    local-base-foundation - (Local) Create a first phase base image for the foundation appliance
    local-base-enterprise - (Local) Create a first phase base image for the enterprise appliance
    local-partner-enterprise - (Local) Create a second (partner) phase image for the enterprise appliance
    local-base-swift - (Local) Create a first phase base image for the swift appliance
    local-base-monasca - (Local) Create a first phase base image for the monasca appliance
    local-base-update - (Local) Create a first phase base image for the update appliance
    local-base-sdn - (Local) Create a first phase base image for the sdn appliance
    local-mgmt - (Local) Create a management appliance from a base management image
    local-foundation - (Local) Create a foundation appliance from a base foundation image
    local-enterprise - (Local) Create a enterprise appliance from a base enterprise image
    local-swift - (Local) Create a swift appliance from a base swift image
    local-monasca - (Local) Create a monasca appliance from a base monasca image
    local-update - (Local) Create a update appliance from a base update image
    local-sdn - (Local) Create a sdn appliance from a base sdn image
============= Suggested Multicommands ==============
    local, <appliance>: builds a local build of the appliance
    jenkins, <appliance>: does a jenkins build of the appliance
    rc, <appliance>: does an rc versioned build of the appliance
    pr, rc, <appliance>: does a partner release release candidate
    pr, <appliance>: does a final partner release
    <appliance>: does a final release
```

The documentation associated with the commands are provided from the
`command` sections' "description" options, e.g.:

```
[command@local-swift]
description=(Local) Create a swift appliance from a base swift image
```

###### Multicommands

Multicommands are a way to launch several sections in a single execution.
The syntax for launching a multicommand is the same that you would use when
writing a line in a "command" section in a csmakefile.

For example, you might say:
```
$ csmake --command "local-swift & local-monasca & local-update"
```

And csmake would start doing all three commands in parallel

Multicommands are especially helpful for complex builds when most of each of
the builds are the same.  For example, above, you see various multicommands
suggested that have prefixes that help define the final purpose of the build.

Practices may differ on how this is used, but some suggestions include:
* A prefix command that specifies the build is a pre-release
* A prefix command that defines one of several environments for a build
* A postfix command that defines which backend to store a build to

Essentially, use of a multicommand is preferred to using branching (which isn't
provided in csmake) or shell environment variables to define how a build
should operate.  Obviously, there are times when use of shell environment
variables can be useful if well documented, but this should be avoided whenever
possible to make each build self-contained.

#### Build Phases

Phases are used to control the actions or set of actions each module will take
based on what is called out in the csmakefile.  When a phase is specified on
the csmake command line, csmake will dispatch that message to the
implementation of every build section from the `--command` specified in 
csmake.

So, for example:
* `csmake build` will tell csmake to send the `build`
message to every section's implementation evaluated from the csmakefile's
default command. 
* `csmake clean` would send "clean" to every section implementation.
* `csmake clean build` would send "clean" to every section specified in the
default command, followed by sending "build" to the same sections.

Optionally, a csmakefile may contain a `[~~phases~~]` section which is a
built in csmake module.  The documentation for the section may be obtained
in the standard way described above: `csmake --list-type=~~phases~~`.  

This will provide a short description of all the valid phases (as explicitly
defined in the `~~phases~~` section, anticipated combinations of phases and
descriptions of what they do, the default sequence of phases (the phases csmake
will perform if no phases are listed on the command line), and any suggested
 multicommands.  The information contained in the `~~phases~~` section can be
accessed from the command line using `--list-phases`.

Here is an example:

```
$ csmake --list-phases
 
=================== Valid Phases ===================
clean_build: Cleans just the build directory for the given appliance build
build: Builds an appliance based on the given command(s)
clean: Cleans all build artifacts from the given command
clean_results: Cleans the given appliance build and results directories
=============== Valid Phase Sequences ==============
clean_results -> build:  Generates a clean build of an appliance
clean_results -> build -> clean_build:  Keeps only the results
Default sequence: clean_results -> build -> clean_build
   (Executed when phase(s) not given on command line)
============= Suggested Multicommands ==============
    local, <appliance>: builds a local build of the appliance
    jenkins, <appliance>: does a jenkins build of the appliance
    rc, <appliance>: does an rc versioned build of the appliance
    pr, rc, <appliance>: does a partner release release candidate
    pr, <appliance>: does a final partner release
    <appliance>: does a final release
```

#### --help Flag and Friends

Several of the flags provide help:

* `--help` - brief synopsis flags available for use with csmake
* `--help --verbose` - full command line flag help
* `--list-type=<module type>` - provides help for a single section module type
* `--list-types` - provides the help for all available section module types
* `--list-commands` - provides a list of valid commands and multicommands
* `--list-phases` - provides a list of:
   - valid phases
   - combinations of phases
   - the default combination of phases
   - and multicommands
                (if provided by a ~~phases~~ section)
* `--help-all` - will dump all available information

#### Output Verbosity Flags

Some of the flags provide control over how much output csmake will provide. 

By default, csmake will provide all its visual cues and any WARNINGs, ERRORs, and EXCEPTIONs (and CRITICALs as well) that a build produces. 

Here is a list of the flags that will help control levels of output:

* `--verbose` - will also allow "INFO" output.
* `--debug` - will also allow "INFO" and "DEBUG" output.
   - This will also turn on any stack traces produced from a failed build or exception.
* `--quiet` - Turn off all visual cues, Turn off all WARNING and ERROR messages.
* `--dev-output` - will turn on very verbose output that describes the
                   specific workflow csmake is executing
   - This operates independently of --quiet, --verbose, and --debug
* `--no-chatter` - Turns off banner decorations
* `--log` - will send the csmake output to the path specified for --log.

The rest of the flags are used to control various aspects of the execution flow of csmake itself and are used less often in the course of doing everyday builds with csmake.  The documentation for these flags can be found by invoking `--help`.

<sub>This material is under the GPL v3 license:

<sub>(c) Copyright 2017 Hewlett Packard Enterprise Development LP

<sub>This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

<sub>This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
Public License for more details.

<sub>You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

