# https://www.youtube.com/watch?v=AU9pI0yIEWw&list=PL7yh-TELLS1F3KytMVZRFO-xIo_S2_Jg1&index=11

import logging

logging.basicConfig(level=logging.INFO)

logging.info("you have too many emails unread")
logging.critical("boom!!!")

handler = logging.FileHandler("myLog.log")
handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(levelname)s - %(asctime)s: %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger("Test Logger")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info("the best logger ever")
logger.critical("boom ba ya!!!")
logger.error("now what?")
