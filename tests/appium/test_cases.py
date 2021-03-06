# doing one action using the webdriver

import instappium
from instappium import FSMSession
from instappium import Settings


# session = instappium.InstAppium(
#     username="acc", password="mdp", device="emulator-5554", show_logs=True
# )

session = instappium.InstAppium(
    username="acc", password="mdp", device="33008e3439f514d9", show_logs=True
)

# returns logged if not logged
# print(session._webdriver._web_driver_instance.page_source)
session._webdriver.go_search("robin", "accounts")

# Basic settings to do some testings
Settings.set_action_delays(
    enabled=True,
    like=150,
    follow=150,
    unfollow=150,
    story=150,
    randomize=True,
    random_range=[70, 110],
)

Settings.set_quota_supervisor(
    peak_likes=(40, 300),
    peak_follows=(25, 150),
    peak_unfollows=(60, 200),
    peak_server_calls=(300, 2500),
)

# doing one action using the FSM
fsm = FSMSession(session._webdriver)

# should respond idle
print(fsm.state)

# let's go to the home page
fsm.go_homepage()
