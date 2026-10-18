# Finpixelgames.github.io
FinPixel Games – Official website

## Pelit etusivulla (games.json)

Etusivun "Our games" -kortit ja About-osion julkaisulista rakennetaan tiedostosta `games.json`:

1. Lisää peli `games.json`:iin (`id`, `name`, `icon` (PNG sivun juuressa), `status` = `out` / `test` / `soon`,
   `released` = julkaisupäivä YYYY-MM-DD julkaistuille, `desc`, `url`, testeille ja tuleville `cta`).
2. Aja `python build_games.py` (kirjoittaa `index.html`:n merkkien `<!-- GAMES:START/END -->` ja
   `<!-- RELEASES:START/END -->` väliin; sivu pysyy staattisena HTML:nä).
3. Commit + push.

Julkaistu peli näkyy 30 päivää merkillä NEW, OUT NOW ja ensimmäisenä. Sen jälkeen järjestys: testit, tulossa
olevat, muut uusin ensin. Ruudukko sovittaa sarakkeet tilaan, joten pelejä voi olla rajattomasti. Aja
build uudelleen myös silloin, kun NEW-merkin pitäisi poistua (tai minkä tahansa muun muutoksen yhteydessä).
