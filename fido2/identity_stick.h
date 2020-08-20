// Copyright 2020 Identity Stick Developers
//
// Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
// http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-MIT or
// http://opensource.org/licenses/MIT>, at your option. This file may not be
// copied, modified, or distributed except according to those terms.
#include<stdio.h>
#include<string.h>
#include <stdbool.h>

#ifndef _IDENTITY_STICK_H
#define _IDENTITY_STICK_H

int getAvailableData(char * dest);

int nextString(const char * type, int number, char * nextString, int len);

int safeStrCopyFromConstant(char * dest, const char * origin, int len, size_t offset);

int getPartLength();

int lenRequestedString(const char * type);

bool isValidAttribute(const char * type);

#endif