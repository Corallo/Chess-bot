# Chess-bot

This repo contains my bot that plays chess on chesss.com

## To Do

### Features

- [x] Web Scrapper to read current game
- [x] Parser to parse the chesboard to pychess (use move list)
- [x] Dummy engine
- [x] Extend web scarper with make_move function
- [x] Add checkmate to eval function
- [X] Add draw to eval function
- [x] Implement alpha beta
- [ ] Create automatic test as GitHub action to check if commit improve against last version of engine
- [ ] Verify caching is actually working.
- [ ] Implement Iterative deepening
- [ ] Implement heuristic to decide how much time to spend
- [ ] Implement piece positional value
- [ ] Speed up board handling
- [ ] ...

### Bugfixes

- [ ] Fix parser bug causing crash when game end
- [ ] Fix attempt to login without entering password
- [x] Catch exception when failing to move, and just make it try again
- [ ] Draw detection doesn't seem to work properly


## Notes for myself in the future

If you try to implement a new feature, remember to restart the ipynb python kernel, otherwise the old cached version of the python files will be used.