from datetime import datetime
from pytz import timezone
from .. import datetime as plugin_env
from userge import userge, Message

LOG = userge.getLogger(__name__)  # logger object


@userge.on_cmd("dt", about={
    'header': "Get the time and date of a City/Country/Timezone.",
    'flags': {
        '-l': "Gives list of all Country/City Combos for Heroku Config"},
    'usage': "Use {tr}dt to show the Time & Date of your predefined City\n"
             "Use {tr}dt -l to display all TZ Combo's for the Config\n",
    'examples': ['{tr}dt', '{tr}dt [Flag]']},
    del_pre=True)
async def grab_time(message: Message):
    LOG.debug("Starting Time command...")
    default_message = (
        "<code>Below is a list of all the Timezones Avaliable</code> \n<a "
        "href=https://raw.githubusercontent.com/jaxellis/Userge_Plugins/main/plugins/tools/datetime/citylist.txt>"
        "Click Here!</a>\n<code>Enter"
        " one in your Heroku Config Under</code> (<code>COUNTRY_CITY</code>)\n"
        "<code>Ex: America/Los_Angeles</code>")

    if 'l' in message.flags:
        LOG.debug("date_time | FLAG = List: Giving TZ list...")
        await message.edit(default_message, disable_web_page_preview=True,
                           parse_mode="html", del_in=30)
        return

    if not plugin_env.COUNTRY_CITY:
        LOG.debug("date_time: No Config Set")
        await message.edit(default_message, disable_web_page_preview=True,
                           parse_mode="html", del_in=30)
        return

    datetime_now = datetime.now(timezone(plugin_env.COUNTRY_CITY))
    date_day_int = datetime_now.strftime('%d')
    await message.edit(" ".join(["It's", datetime_now.strftime('%I:%M %p'), "on", datetime_now.strftime('%A'), "the", date_day_int, ordinal_suffix(
        date_day_int), "of", datetime_now.strftime('%B'), "in", plugin_env.COUNTRY_CITY.replace("_", " ")]))
    LOG.debug("Time: Command Finished Successfully")


def ordinal_suffix(day):
    if 3 < day < 21 or 23 < day < 31:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}[day % 10]
