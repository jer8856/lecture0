# Socket io to retrieve messages for a chat room
@socketio.on("submit message")
def message(data):
    selection = data["selection"]
    time = datetime.now().strftime("%Y-%m-%d %H:%M")  # Retrieving current datetime

    if "https://www.youtube.com/watch?v=" in selection:
        selection = selection.replace("https://www.youtube.com/watch?v=","https://www.youtube.com/embed/")
    # Dictionary to save with messages
    response_dict = {"selection": selection, "time": time, "user_name": session["user_name"]}
    messagelist = messagedict[chatlist[session["chat_id"] - 1]]

    # When messages reaches 100 delete start deleting first ones
    if len(messagelist) == 100:
        del messagelist[0]

    # Add message to the messages of the current channel
    messagelist.append(response_dict)
    emit("cast message", {**response_dict, **{"chat_id": str(session["chat_id"])}}, broadcast=True)
