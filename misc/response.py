import logging


async def get_response(session, url, params=None):
    logging.debug(f"get_response: CALLED     url:{url} params:{params}")
    if params is None:
        params = {}

    async with session.get(url, params=params) as response:
        status = response.status
        text = await response.text()
        logging.debug(f"get_response: SUCCESS     status:{status} data:{text}")
        return status, text
