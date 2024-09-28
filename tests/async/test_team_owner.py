import aiohttp
from bloonspy import AsyncClient


class TestTeamOwner:
    async def test_team(self) -> None:
        """
        Test getting a team's owner.
        """
        async with aiohttp.ClientSession() as cs:
            client = AsyncClient(aiohttp_client=cs)
            team_id = "9fba1683de92f9f01c4b861d5c70e326ce571db4ca448b30"#"9fbd42d98ac2faa41d40884a5b21b577cb064ebacf168e3f"
            team = await client.get_team(team_id)
            owner = await team.owner()
            assert owner is not None
