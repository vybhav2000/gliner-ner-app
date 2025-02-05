import logging

# Adding basic config
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S,%f"
)

# getting the uvicorn logger
logger = logging.getLogger("uvicorn")
