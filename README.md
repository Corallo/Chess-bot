# Chess-bot

This repo contains my bot that plays chess on chesss.com

## To Do

### Features

- [x] Web Scrapper to read current game
- [x] Parser to parse the chesboard to pychess (use move list)
- [x] Dummy engine
- [x] Extend web scarper with make_move function
- [ ] Speed up processing by using native san format
- [ ] Add checkmate to eval function
- [ ] Add draw to eval function
- [ ] Create automatic test as GitHub action to check if commit improve against last version of engine
- [ ] Implement proper caching
- [ ] Implement alpha beta
- [ ] Implement Iterative deepening
- [ ] Implement heuristic to decide how much time to spend
- [ ] Implement piece positional value
- [ ] ...

### Bugfixes

- [ ] Fix parser bug causing crash when game end
- [ ] Fix attempt to login without entering password
- [ ] Catch exception when failing to move, and just make it try again


## Notes for myself in the future

If you try to implement a new feature, remember to restart the ipynb python kernel, otherwise the old cached version of the python files will be used.