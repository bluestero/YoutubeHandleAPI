import googleapiclient.discovery


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
    channels = channels["items"]

    #-Adding customUrl key value to the result to mimick the potential solution-#
    dummy_handle = "https://www.youtube.com/" + handle
    for index in range(len(channels)):

        channels[index]["snippet"]["customUrl"] = dummy_handle

        #-Changing the value of customUrl to avoid duplicates-#
        dummy_handle = dummy_handle + "test"

    #-Iterating the searched channels-#
    for channel in channels:

        #-Extracting the handle of the searched channel-#
        customUrl = channel["snippet"]["customUrl"].split("/")[-1]

        #-Returning the snippet if handle matches-#
        if customUrl == handle:
            return channel


#-Safeguarding the code-#
if __name__ == "__main__":

    #-Creating the youtube api service using your API key-#
    api_key = "Your API Key goes here." #-Can implement using load env, I did not do it here for keeping code short and simple-#
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey = api_key)

    #-Base objects-#
    handle_to_search = "@google"

    #-Fetching the channel snippet using @google handle-#
    channel_snippet_using_handle = fetch_channel_by_handle(youtube, handle_to_search)
    print(channel_snippet_using_handle)