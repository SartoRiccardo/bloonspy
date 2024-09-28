Usage in an asynchronous environment
------------------------------------

``bloonspy`` offers the asynchronous :class:`bloonspy.AsyncClient` API which you can use in asynchronous environments.
Returned objects and models are exactly the same as its synchronous counterpart, with a few important differences:

- :class:`bloonspy.AsyncClient` has to be instanced, none of its methods are static.
- Function calls have to be awaited
- Trying to access a property that hasn't been loaded of any model will raise :class:`bloonspy.exceptions.NotLoaded`

::

    from bloonspy import AsyncClient
    import asyncio


    async def main():
        async with aiohttp.ClientSession() as session:
            client = AsyncClient(aiohttp_client=session)
            await get_race_summary(client)
            await get_race_summary_wrong(client)


    async def get_race_summary(client: AsyncClient):
        """Print general information about the latest race events."""
        races = await client.races()

        # Load all Race objects concurrently
        await asyncio.gather(*[race.load_resource() for race in races])

        for race in races:
            print(f"Race {race.name} went from {race.start} to {race.end}. "
                  f"It was on {race.gamemode.difficulty.value} difficulty and "
                  f"ended at round {race.end_round}.")


    async def get_race_summary(client: AsyncClient):
        """This is how you DON'T do it."""
        races = await client.races()

        for race in races:
            # Raises bloonspy.exceptions.NotLoaded, because you tried to access
            # Race.start on a Race object which wasn't loaded. The synchronous client
            # would have fetched it for you under the hood, but the async one doesnt.
            # You should load the resource first and then access what you need.
            print(f"Race {race.name} started at round {race.start}.")


    if __name__ == "__main__":
        asyncio.run(main())


Since all objects are lazy loaded by default, it's important to call the :func:`bloonspy.model.Loadable.load_resource`
or :func:`bloonspy.model.Event.load_event` explicitely at times, or set the ``eager`` parameter to ``True`` on methods
that support it.

Note that not all properties are lazily loaded. Some can be loaded right away, in the example below, ``Race.name`` is
already loaded when a result of :func:`bloonspy.Client.races`, so no need to load the whole resource.
This is lined out in the documentation for the function.

::

    async def print_race_difficulty_bad(client: AsyncClient):
        race = await client.races()[0]

        # Bad! Since Race.gamemode is not currently loaded,
        # bloonspy.exceptions.NotLoaded will be raised.
        print(race.gamemode.difficulty.value)


    async def print_race_difficulty_good(client: AsyncClient):
        race = await client.races()[0]

        # Good! Load the resource and await it before accessing lazy loaded properties.
        await race.load_resource()
        print(race.gamemode.difficulty.value)

        race = await client.races(eager=True)[1]

        # Also good! The races were loaded thanks to eager=True.
        print(race.gamemode.difficulty.value)


    async def print_race_name(client: AsyncClient):
        race = await client.races()[0]

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