AVATARS = {

    "Google":"🟦",

    "Amazon":"🟧",

    "Microsoft":"🟩",

    "Meta":"🟦",

    "OpenAI":"🤖",

    "Startup":"🚀"

}


def get_avatar(company):

    return AVATARS.get(company,"🤖")