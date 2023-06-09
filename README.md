# BloonsPy

BloonsPy is a Python wrapper for the [Ninja Kiwi Open Data API](https://data.ninjakiwi.com/),
that makes you write more readable code and handles rate limiting automatically.

## Installing

**Python 3.10 or higher is required**

```bash
python3 -m pip install bloonspy
```

## Quick example

```python
from bloonspy import Client

boss_event = Client.bosses()[0].standard()
boss_standard_top_3 = boss_event.leaderboard()[:3]
for player in boss_standard_top_3: 
    print(f"{player.name} - {player.score}")
```

## Resources
+ [Documentation](https://bloonspy.readthedocs.io/en/latest/)
+ [Github](https://github.com/SartoRiccardo/bloonspy)
