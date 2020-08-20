# Boardwatch API

## Splash
An API to interface with decoupled frontends. Provides search functionality to amassed catalog of consoles, games, and accessories. Subsequently provides presence-tracking service across a collection of secondhand market sites.

## Development to-do list
- [x] `[GET] /` pingable root
- [x] `[GET] /platforms` Read all platforms
- [x] `[GET] /platforms/<id>` Read platform by ID
- [x] `[GET] /platforms/search` basic platform search
- [x] `[GET] /platforms/<id>/platform-editions` Read all platform editions for console
- [x] `[GET] /platform-editions/<id>` Read platform edition by ID
- [x] `[GET] /platform-editions/search` basic platform edition search
- [x] `[GET] /games` Read all games
- [x] `[GET] /games/<id>` Read game by ID
- [ ] `[GET] /games/search` basic game search
- [ ] `[GET] /accessories` Read all accessories
- [ ] `[GET] /accessories/<id>` Read accessory by ID
- [ ] `[GET] /accessories/search` basic accessory search
- [ ] `[POST] /auth/signup` Create user
- [ ] `[GET] /account` Read own user profile
- [ ] auth middleware
- [ ] `[POST] /platforms/watch` Create platform watch
- [ ] `[GET] /platforms/watch/<id>` Read platform watch
- [ ] `[PUT] /platforms/watch/<id>` Update platform watch
- [ ] `[DELETE] /platforms/watch/<id>` Delete platform watch
- [ ] `[POST] /platform-editions/watch` Create edition watch
- [ ] `[GET] /platform-editions/watch/<id>` Read edition watch
- [ ] `[PUT] /platform-editions/watch/<id>` Update edition watch
- [ ] `[DELETE] /platform-editions/watch/<id>` Delete edition watch
- [ ] `[POST] /games/watch` Create game watch
- [ ] `[GET] /games/watch/<id>` Read game watch
- [ ] `[PUT] /games/watch/<id>` Update game watch
- [ ] `[DELETE] /games/watch/<id>`Delete game watch
- [ ] `[POST] /accessories/watch` Create accessory watch
- [ ] `[GET] /accessories/watch/<id>` Read accessory watch
- [ ] `[PUT] /accessories/watch/<id>` Update accessory watch
- [ ] `[DELETE] /accessories/watch/<id>` Delete accessory watch
- [ ] `[PUT] /account` Update user
- [ ] `[DELETE] /account` Delete user
- [ ] e-mail authentication-based password/e-mail change
