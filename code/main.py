import flask


def buy(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    request_args = request.args

    if request_args and "nft" in request_args and "buyer" in request_args:
        nft = request_args["nft"]
        buyer = request_args["buyer"]
    else:
        nft = "666"
        buyer = "Rui"
        
    return "Buy NFT {} for {}".format(flask.escape(nft), flask.escape(buyer))
