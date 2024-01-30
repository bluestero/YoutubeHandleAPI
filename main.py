import googleapiclient.discovery


#-Function to get the channel using Channel ID-#
def fetch_channel_by_id(youtube: googleapiclient.discovery.Resource, channel_id: str) -> dict:
    """
    Fetch channel data using YouTube Channel ID.

    Parameters
    ----------
    `youtube: googleapiclient.discovery.Resource`
        Your initialized youtube service to be used for querying the search.
    `channel_id: str`
        The channel id you want to extract data snippet for.

    Returns
    -------
    `response: dict`
        Returns a dict (snippet) containing information about the channel.
    """

    #-Creating a request object to fetch snippet for the given channel id-#
    request = youtube.channels().list(
        part = "snippet",
        id = channel_id
    )

    #-Exceuting the query to get a response dict-#
    response = request.execute()

    #-Returning the response dict-#
    return response


#-Function to query youtube search for results-#
def search_youtube_channel(youtube: googleapiclient.discovery.Resource, handle: str) -> list:
    """
    Fetches list of channels using relevant keywords.

    Parameters
    ----------
    `youtube: googleapiclient.discovery.Resource`
        Your initialized youtube service to be used for querying the search.
    `handle: str`
        The handle name you want to search for.

    Returns
    -------
    `response: list`
        If channel is found, returns a dict (snippet) containing information about the channel.
    """

    #-Creating a request object to fetch channels and snippets for the given handle name-#
    request = youtube.search().list(
        part = "snippet",
        type = "channel",
        q = handle
    )

    #-Exceuting the query to get a response list-#
    response = request.execute()

    #-Returning the response list-#
    return response


#-Function to fetch channel snippet and compare its custom url against given handle-#
def is_channel(youtube: googleapiclient.discovery.Resource, channel_id: str, handle: str) -> bool:
    """
    Fetches snippet of given channel id and checks its custom url against given handle.

    Parameters
    ----------
    `youtube: googleapiclient.discovery.Resource`
        Your initialized youtube service to be used for querying the search.
    `channel_id: str`
        The channel id you want to extract data snippet for.
    `handle: str`
        The handle name you want to match the custom url against.

    Returns
    -------
    `response: dict`
        If handle matches, returns the channel snippet dict.
    """

    #-Fetches the snippet of the given channel-#
    channel_snippet = fetch_channel_by_id(youtube, channel_id)

    #-Extracts and formats the custom url-#
    custom_url = channel_snippet["items"][0]["snippet"]["customUrl"].split("/")[-1]

    #-Formatting the given handle-#
    handle = "@" + handle if handle[0] != "@" else handle

    #-Returning the channel snippet if true else None-#
    if handle == custom_url:
        return channel_snippet


#-Function to fetch youtube channel using handle-#
def fetch_channel_by_handle(youtube: googleapiclient.discovery.Resource, handle: str) -> dict:
    """
    Fetch channel data using YouTube @handle.

    Parameters
    ----------
    `youtube: googleapiclient.discovery.Resource`
        Your initialized youtube service to be used for querying the search.
    `handle: str`
        The @handle you want to extract data snippet for.

    Returns
    -------
    `response: dict`
        Returns a dict (snippet) containing information about the channel if get any.
    """

    #-Searching the handle and getting the list of results-#
    channels = search_youtube_channel(youtube, handle)

    #-Iterating the searched channels-#
    for channel in channels["items"]:

        #-Getting the channel id of the searched channel-#
        channel_id = channel["snippet"]["channelId"]

        #-Getting the channel snippet for the extracted id if handle matches-#
        channel_snippet = is_channel(youtube, channel_id, handle)

        #-Returning the snippet if get any-#
        if channel_snippet:
            return channel_snippet


#-Safeguarding the code-#
if __name__ == "__main__":

    #-Creating the youtube api service using your API key-#
    api_key = "Your API Key goes here." #-Can implement using load env, I did not do it here for keeping code short and simple-#
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = api_key)

    #-Base objects-#
    handle_to_search = "@google"

    #-Fetching the channel snippet using @google handle-#
    channel_snippet_using_handle = fetch_channel_by_handle(youtube, handle_to_search)