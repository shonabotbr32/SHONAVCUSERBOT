# ONLY CHANGE: USER PHOTO BLOCK REMOVED ✅

@Command(['user', 'info'])
@disableable(['user', 'info'])
async def UserInfo(update, context):
    message = update.effective_message
    bot = context.bot
    chat = update.effective_chat
    
    user_id = await extract_user(message)
    if not user_id:
        await message.reply_text("Can't access by username, reply to the user or give their telegram id")
        return

    msg = await message.reply_text(
        font("<code>Processing User Info...</code>"),
        parse_mode=constants.ParseMode.HTML
    )

    try:
        user = await bot.get_chat(user_id)
        pyro_user = await pbot.get_users(user_id)

        dc_id = getattr(pyro_user, 'dc_id', None)
        is_premium = getattr(pyro_user, 'is_premium', False)
        is_bot = getattr(pyro_user, 'is_bot', False)
        is_restricted = getattr(pyro_user, 'is_restricted', False)

    except Exception as e:
        await msg.edit_text(f"❌ ERROR: {html.escape(str(e))}")
        return

    dc_location = DC_LOCATIONS.get(dc_id, "Unknown")
    premium_status = "Yes" if is_premium else "No"
    account_created = estimate_account_creation_date(user.id)
    account_created_str = account_created.strftime("%B %d, %Y")
    account_age = calculate_account_age(account_created)

    first_name = getattr(user, 'first_name', 'Unknown')
    last_name = getattr(user, 'last_name', '')
    full_name = f"{first_name} {last_name}".strip() if last_name else first_name
    username = getattr(user, 'username', None)

    text = (
        f"<b>🔍 User Info 📋</b>\n"
        "<b>━━━━━━━━━━━━━━━━</b>\n"
        f"<b>Name:</b> <b>{safe_escape(full_name)}</b>\n"
    )

    if username:
        text += f"<b>Username:</b> @{username}\n"

    text += f"<b>User ID:</b> <code>{user.id}</code>\n"

    if not is_bot:
        text += f"<b>Premium:</b> <b>{premium_status}</b>\n"

    text += f"<b>DC:</b> <b>{dc_location}</b>\n"

    if not is_bot:
        text += (
            f"<b>Created:</b> <b>{account_created_str}</b>\n"
            f"<b>Age:</b> <b>{account_age}</b>\n"
        )

    text += f"<b>Frozen:</b> <b>{'Yes' if is_restricted else 'No'}</b>\n"

    status = await get_status_text(user.id)
    if status:
        text += f"<b>Status:</b> {status}\n"

    text += (
        f"<b>Link:</b> <a href='tg://user?id={user.id}'>Click Here</a>\n"
        "<b>━━━━━━━━━━━━━━━━</b>\n"
        "<b>Done ✅</b>"
    )

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"📋 {full_name}", url=f"tg://user?id={user.id}")]]
    )

    # ✅ ONLY TEXT (NO PHOTO)
    try:
        await msg.edit_text(
            text=text,
            parse_mode=constants.ParseMode.HTML,
            reply_markup=keyboard
        )
    except BadRequest:
        await msg.edit_text(
            text=text,
            parse_mode=constants.ParseMode.HTML
        )