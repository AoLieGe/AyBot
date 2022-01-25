async def get_response(session, url, params=None):
    if params is None:
        params = {}

    async with session.get(url, params=params) as response:
        return response.status, await response.text()
