# Identity Stick
The Identity Stick is a security key based on [Solokey](https://github.com/solokeys/solo). It extends the functionality of the Solokey with the ability to identify users using the [identity-stick extension](https://github.com/Identity-Stick/identity-stick-extension). This is a prototype and will only work with the [Solo Hacker](https://solokeys.com/products/solo-hacker).

The basic functionality of supporting FIDO2 and U2F standards of the Solokey is still supported. This enables the Identity Stick to be used for identification, two-factor authentication and password-less login.

If you want to know more about the Solokey, visit their [repo](https://github.com/solokeys/solo) or [documentaion](https://docs.solokeys.dev/building/).

## Checking out the code
```bash
git clone --recurse-submodules https://github.com/solokeys/solo
cd identity-stick
```
If you forgot the `--recurse-submodules` while cloning, simply run `git submodule update --init --recursive`.

`make update` will also checkout the latest code on `master` and submodules.


## Prerequisites the toolchain and applying updates

### Getting the ARM Compiler tool chain

Download the Compiler tool chain for your system [here](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) and unzip it. There is a readme.txt __ in _gcc-arm-none-eabi-x-yyyy-dd-major/share/doc/gcc-arm-none-eabi_. It contains installation guides for Linux, Windows and Mac.  

Make sure to install the solo tool.
```bash
pip install solo-python

#Or
pip3 install solo-python
```

If you are on a linux system, you might have to add some udev rules as described [here](https://docs.solokeys.dev/udev/).

## Build
If you have everything installed, you can build the code with:
```bash
cd targets/stm32l432
make cbor
make build-hacker
cd ../..
```

You can then program your Solo Hacker with:
```bash
solo program aux enter-bootloader
solo program bootloader targets/stm32l432/solo.hex
```

You can also just run the script in the root folder:
```bash
./build-program-hacker.sh
```

# License

This software is fully open source.

All software, unless otherwise noted, is dual licensed under Apache 2.0 and MIT. You may use this software under the terms of either the Apache 2.0 license or MIT license.

All hardware, unless otherwise noted, is dual licensed under CERN and CC-BY-SA. You may use the hardware under the terms of either the CERN 2.1 license or CC-BY-SA 4.0 license.

All documentation, unless otherwise noted, is licensed under CC-BY-SA. You may use the documentation under the terms of the CC-BY-SA 4.0 license


# Supported by

This fork is part of the project Identity Stick. Identity Stick is a finalist of the <a href= "https://prototypefund.de/">PrototypeFund round 7</a>, see <a href="https://prototypefund.de/project/identity-stick/">our project site</a> for details.

[<img alt="BMBF" src="https://identity-stick.github.io/ressourcen/BMBF_gefîrdert%20vom_deutsch.jpg" height="150">](https://www.bmbf.de/de/software-sprint-freie-programmierer-unterstuetzen-3512.html "BMBF Software Sprint Förderrichtlinie")
[<img alt="Prototypefund" src="https://i0.wp.com/blog.okfn.org/files/2017/12/22137279_1679687182104997_6759961652435307500_o.jpg" height="150">](https://prototypefund.de "Prototypefund Website")

[![License](https://img.shields.io/github/license/solokeys/solo.svg)](https://github.com/solokeys/solo/blob/master/LICENSE)
[![Build Status](https://travis-ci.com/solokeys/solo.svg?branch=master)](https://travis-ci.com/solokeys/solo)

[![commits since last release](https://img.shields.io/github/commits-since/solokeys/solo/latest.svg)](https://github.com/solokeys/solo/commits/master)
