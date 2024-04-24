# EmuRemoteSaveLoad

A dumb weekend art project which features an emulator running a playlist of retro games. When the player (or random observer) presses a large red button, the app saves the current game state and selects a random game from the playlist. If this game had previously been played, the previous save state is loaded. 

I figured I would find an emulator with scripting support instead of just modifying an open source fork. This would allow the majority of the playlist and save save state selection to be run server side and client emulators could be swapped out. As it turns out, tying blocking client operations to a frame can be problematic. Oh well. Beware some hacky implementation. 

Thank you to the amazing emulator and retro modding community. It is always a delight to see all the new tools and tech you have all been working on. 

## Installation

This project was designed to work with the [FCEUX](https://fceux.com/web/home.html) emulator version 2.6.6

## Usage

Check back later... Implementation in progress. 

## License

[MIT](https://choosealicense.com/licenses/mit/)