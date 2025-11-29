import logging

logging.basicConfig(
    filename="logger.log",
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filemode="w"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


