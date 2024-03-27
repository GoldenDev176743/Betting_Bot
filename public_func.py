import resend
from info_account import resend_api_key, gmail_address

resend.api_key = resend_api_key
def send_mail(message: str) -> str:
    params = {
        "from": "MBF HarryPorter <onboarding@resend.dev>",
        "to": ["{}".format(gmail_address)],
        "subject": "Notification",
        "html": "<strong>{}</strong>".format(message),
    }
    resend.Emails.send(params)        

def find_matching_event(winner : str, loser : str, players : list[str]) -> int:
    winner_name = str(winner).split(' ')
    loser_name = str(loser).split(' ')

    index = 2
    matched_count = 0
    for subname in winner_name:
        if subname in players[0]:
            matched_count += 1
    for subname in loser_name:
        if subname in players[1]:
            matched_count += 1
    if matched_count >= 3:
        index = 0

    if index == 2:
        matched_count = 0
        for subname in winner_name:
            if subname in players[1]:
                matched_count += 1
        for subname in loser_name:
            if subname in players[0]:
                matched_count += 1
        if matched_count >= 3:
            index = 1
    return index