from datetime import datetime
from pytz import timezone
from . import COUNTRY_CITY
from userge import userge, Message

LOG = userge.getLogger(__name__)  # logger object


@userge.on_cmd("datetime", about={
    'header': "Get the time and date of a City/Country/Timezone.",
    'flags': {
        '-list | -l': "Gives a list of all Country/City Combos.",
        '-code | -c': "Uses Country_City code given."
    },
    'usage': {
        "{tr}dt to show the Time & Date of your predefined City.",
        "{tr}dt -l | {tr}dt -list to display all TZ Combo's for the Config.",
        "{tr}dt -c | {tr}dt -code to use a defined Country/City combo."
    },
    'examples': ['{tr}dt', '{tr}dt [Flag]']
}, del_pre=True)
async def grab_time(message: Message):
    LOG.debug("Starting Time command...")
    country_input = await flag_checks(message, LOG)
    if country_input == None:
        return
    country_code = COUNTRY_CITY if not country_input else country_input
    try:
        timezone(country_code)
    except BaseException:
        LOG.debug("date_time: Incorrect Country Code...")
        await message.err("Unable To Determine Timezone With Given"
                          + " Country Code | " + country_code +
                          "\n use -l flag to show a list of compatible codes.")
        return
    datetime_now = datetime.now(timezone(country_code))
    date_day = datetime_now.strftime("%d")
    date_time = datetime_now.strftime('%I:%M%p')
    if date_day[0] == "0":
        date_day = date_day[1:]
    if date_time[0] == "0":
        date_time = date_time[1:]
    await message.edit(" ".join(
        ["It's", date_time, "on",
         datetime_now.strftime('%A'), datetime_now.strftime('%B'), date_day +
         ordinal_suffix(int(date_day)), "in", country_code.replace("_", " ")])
    )
    LOG.debug("date_time: Command Finished Successfully")


def ordinal_suffix(day: int):
    if 3 < day < 21 or 23 < day < 31:
        return 'th'
    else:
        return {1: 'st', 2: 'nd', 3: 'rd'}[day % 10]


async def flag_checks(message: Message, log):
    default_message = (
        "<code>Below is a list of all the Timezones Avaliable</code> \n<a "
        "href=https://raw.githubusercontent.com/jaxellis/Userge_Plugins/main/"
        "plugins/tools/datetime/citylist.txt>Click Here!</a>\n<code>Enter"
        " one in your Heroku Config Under</code> (<code>COUNTRY_CITY</code>)\n"
        "<code>Ex: America/Los_Angeles</code>")
    if 'list' in message.flags or 'l' in message.flags:
        log.debug("date_time | FLAG = List: Giving TZ list...")
        await message.edit(default_message, disable_web_page_preview=True,
                           parse_mode="html", del_in=30)
        return None

    if 'code' in message.flags or 'c' in message.flags:
        log.debug("date_time | FLAG = Code: Grabbing Country_Code...")
        country_input = message.filtered_input_str.strip()
        if not country_input:
            await message.err("No Country_City code found after flag...")
            return None
        return country_input
    elif not COUNTRY_CITY:
        log.debug("date_time: No Config Set")
        await message.edit(default_message, disable_web_page_preview=True,
                           parse_mode="html", del_in=30)
        return None
    else:
        country_input = False
