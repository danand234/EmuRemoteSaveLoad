# EmuRemoteSaveLoad

A dumb weekend art project which features an emulator running a playlist of retro games. When the player (or random observer) presses a large red button, the app saves the current game state and selects a random game from the playlist. If this game had previously been played, the previous save state is loaded. 

I figured I would find an emulator with scripting support instead of just modifying an open source fork. This would allow the majority of the playlist and save save state selection to be run server side and client emulators could be swapped out. As it turns out, tying blocking client operations to a frame can be problematic. Oh well. Beware some hacky implementation. 

Thank you to the amazing emulator and retro modding community. It is always a delight to see all the new tools and tech you have all been working on. 

## Installation

This project was designed to work with the [FCEUX](https://fceux.com/web/home.html) emulator version 2.6.6

## Usage

Work in progres...

1. Configuration
   1. Move ROM files into project library directory
   2. Populate project working directory with library.json/txt files (both for now). See project test directory for samples.
2. Run server/server.py
3. In FCEUX File->Lua->New Lua Script Window and select the client/emulator_client_script.lua

Note: All paths used in client Lua script are relative to script location.

## License

[MIT](https://choosealicense.com/licenses/mit/)