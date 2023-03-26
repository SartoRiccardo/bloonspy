Installation
------------

.. note::
   Python 3.10 or higher is required.

.. code-block:: console
    python3 -m pip install bloonspy


Getting your Open Access Key
----------------------------

If you need an Open Access Key to access some of the endpoints, you can generate one in
any Ninja Kiwi game. You cand find instructions on how to generate one on the
`Ninja Kiwi website <https://support.ninjakiwi.com/hc/en-us/articles/13438499873937>`_.


Getting Started
---------------

Now that you've installed the package, you can import the Client.
If you need to, you can create an instance with an API key, otherwise you can use most
methods statically. ::

   from bloonspy import Client

   # Only needed if you actually need an API key for your endpoints.
   my_client = Client("oak_jEo4...l6R")

Now you can use all methods in :class:`~bloonspy.Client`! You can find all of them in its
`API reference <api.html>`_ section. Let's try getting the top players for the latest race event: ::

   latest_race = my_client.races()[0]
   # You can also use this method statically:
   # latest_race = Client.races()[0]
   leaderboard = latest_race.leaderboard()

   print(f"Top 3 players for the race {latest_race.name}:")
   for i in range(3):
       player = leaderboard[i]
       # player.score is a timedelta object in this case.
       minutes = int(player.score/60)
       seconds = int(player.score % 60)
       milliseconds = int((player.score*100) % 100)
       print(f"#{i+1}: {player.name} - {minutes}:{seconds}.{milliseconds}")
