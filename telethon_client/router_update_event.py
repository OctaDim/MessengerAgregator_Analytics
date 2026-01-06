from telethon import events


@tg_client.on(events.NewMessage())
async def my_event_handler(event):
    print("event: ", event)
    print("event.raw_text: ", event.raw_text)
    print("event.raw_text: ", event.raw_text)

    user_id = event.message.from_id.user_id
    user = await event.client.get_entity(user_id)
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    print(f"ID: {user_id}")
    print(f"Username: @{username}")
    print(f"Имя: {first_name} {last_name}")
