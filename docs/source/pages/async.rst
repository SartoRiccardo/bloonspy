Usage in an asynchronous environment
------------------------------------

``bloonspy`` is a synchronous library, but it can be used asynchronously thanks to ``asyncio.to_thread``.

::

    from bloonspy import Client
    import asyncio


    async def get_race_summary():
        """Print general information about the latest race events."""
        races = await asyncio.to_thread(Client.races)

        # Load all Race objects concurrently
        futures = []
        for race in races:
            futures.append(asyncio.to_thread(race.load_resource))
        await asyncio.gather(*futures)

        for race in races:
            print(f"Race {race.name} went from {race.start} to {race.end}. "
                  f"It was on {race.gamemode.difficulty.value} difficulty and "
                  f"ended at round {race.end_round}.")


    async def other_task_not_getting_blocked():
        """Some other task doing whatever."""
        for _ in range(10):
            print("Task not getting blocked reporting for duty.")
            await asyncio.sleep(1)


    async def main():
        """Launches the two tasks above concurrently."""
        await asyncio.gather(
            get_race_summary(),
            other_task_not_getting_blocked()
        )


    if __name__ == "__main__":
        asyncio.run(main())


Since all objects are lazy loaded by default, it's important to call the :func:`bloonspy.model.Loadable.load_resource`
or :func:`bloonspy.model.Event.load_event` explicitely at times, or set the ``eager`` parameter to ``True`` on methods
that support it, and then turn those functions into an asyncio thread. If you don't, and call a property that's lazily
loaded, the module will make an API call to fetch it, which will result in a blocking function.

Note that not all properties are lazily loaded. Some can be loaded right away, in the example below, ``Race.name`` is
already loaded when a result of :func:`bloonspy.Client.races`, so no need to load the whole resource.
This is lined out in the documentation for the function.

::

    async def print_race_difficulty_bad():
        race = await asyncio.to_thread(Client.races)[0]

        # Bad! Since Race.gamemode is not currently loaded,
        # a blocking API call will be made to fetch it.
        print(race.gamemode.difficulty.value)


    async def print_race_difficulty_good():
        race = await asyncio.to_thread(Client.races)[0]

        # Good! Load the resource and await it before accessing lazy loaded properties.
        await asyncio.to_thread(race.load_resource)
        print(race.gamemode.difficulty.value)

        race = await asyncio.to_thread(Client.races, eager=True)[1]

        # Also good! The races were loaded thanks to eager=True.
        print(race.gamemode.difficulty.value)


    async def print_race_name():
        race = await asyncio.to_thread(Client.races)[0]

        # As pointed out in the API reference page, Race.name already gets
        # loaded when calling Client.races, so there's no need to load the whole
        # resource if not necessary.
        print(race.name)


For more info on lazy and eager loading, see the section below.

Lazy and Eager loading
----------------------

By default, whenever you request a resource, it will be lazily loaded, meaning not all
properties will be available straight away. They will be loaded when you need them instead;
this is to limit unnecessary API calls that could make you hit the rate limit. For example:

::

    >>> # The race event is fetched, but only has a few properties available.
    >>> # Read the documentation on the Client.get_race function to see which ones.
    >>> race = Client.get_race("The_Abyssal_Plane_lfbrs5fb")
    >>> # All methods are still available and don't take extra API calls
    >>> # to function, unless explicitely specified in the docs.
    >>> players = race.leaderboard()
    >>> # The gamemode property is not loaded, so Race.load_resource is called to load it.
    >>> print(race.gamemode)

In this example, when we lazy load ``race``, only the properties ``name``, ``start``, ``end``, and ``total_scores``
will be loaded right away. If we want one that isn't loaded (in this example, ``gamemode``), it will be fetched
automatically via an API call.

If you want ``race`` to be fully loaded right away, you can always set the ``eager`` parameter to ``True``.

::

    >>> # This will load the race and automatically call Race.load_resource and return a fully loaded object.
    >>> race = Client.get_race("The_Abyssal_Plane_lfbrs5fb", eager=True)
    >>> # No extra API calls are made since the property is already loaded.
    >>> print(race.gamemode)