# VkusVill Courier

This program helps me manage (automates) parcels tracking and tacking. It calles vkusvill API directly and works faster than webapp.

Example:

```sh
$ python3 check.py
Parcels prepare: 
- 9kg, 344m - Санкт-Петербург, Туристская улица, 28к3
Parcels ready: 
- No
```
## Project

**What?**: I want a program that helps me manage parcels as a courier.

1. Get parcels conveniently
2. Notify about new parcels
3. Automate taking parcels

## Program design

Program design (v1):

- design convinient CLI for retriving parcels


2021-08-7:

- Periodic execution
- Python console library (printing, colors, clearing, etc.)
- Runtime/persistant storage + notification


2021-08-14:

- Code API module
- Implement Telegram Bot using API

## macOS notifications

macOS notification center API levels:

1. macOS (operating system)
2. Objective-C (system programming language)
3. AppleScript (system scripting language)
4. Bash (system interface)
5. Python (general programming language)
