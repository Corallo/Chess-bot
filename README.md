# Corallotto Chess Bot

Corallotto is my simple chess bot that plays on chess.com
At the moment he reached an Elo of 811

## To Do

### Features

- [x] Web Scrapper to read current game
- [x] Parser to parse the chesboard to pychess (use move list)
- [x] Dummy engine
- [x] Extend web scarper with make_move function
- [x] Add checkmate to eval function
- [X] Add draw to eval function
- [x] Implement alpha beta
- [x] Implement piece positional value
- [x] Simplify engine code
- [x] Implement promotion
- [ ] Create automatic test as GitHub action to check if commit improve against last version of engine
- [ ] Implement caching
- [ ] Implement Iterative deepening
- [ ] Implement heuristic to decide how much time to spend
- [ ] Speed up board handling
- [ ] ...

### Bugfixes

- [ ] Fix parser bug causing crash when game end
- [ ] Fix attempt to login without entering password
- [x] Catch exception when failing to move, and just make it try again
- [x] Fix bug that was making black lose intentionally
- [x] Draw detection doesn't seem to work properly
- [x] Stalemate not detected as draw
- [x] Fix positional score bug for black
- [ ] Fix crash when engine return -inf for checkmate

## Notes for myself in the future

If you try to implement a new feature, remember to restart the ipynb python kernel, otherwise the old cached version of the python files will be used.