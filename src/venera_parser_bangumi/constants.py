DATABASE_ENTRIES = ("history.db", "local_favorite.db", "cookie.db")
COLLECTION_STATES = ("wish", "done", "doing", "on_hold", "dropped")
STATE_TO_BANGUMI_TYPE = {
    "wish": 1,
    "done": 2,
    "doing": 3,
    "on_hold": 4,
    "dropped": 5,
}
DEFAULT_BANGUMI_API_BASE_URL = "https://api.bgm.tv/v0"
DEFAULT_USER_AGENT = (
    "bgzo/venera-parser-bangumi "
    "(https://github.com/bGZo/playground)"
)