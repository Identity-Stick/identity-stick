#!/bin/bash

#Change into correct directory
cd targets/stm32l432/

#Compile code
make build-hacker

#Change to root
cd ../..

#Enter bootload mode
solo program aux enter-bootloader

#Deploy code
solo program bootloader targets/stm32l432/solo.hex
