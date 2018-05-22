import os

# Directories
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(PROJECT_DIR, "resources")

# Proxy settings
PROXY_URL = "socks5://185.246.153.31:443/"
PROXY_USER = "guest"
PROXY_PASS = "rnk_go_away"

# Word2Vec settings
MODEL_NAME = "word2vec-ruscorpora-300"
TOPICS_FILE = os.path.join(RESOURCES_DIR, 'topics.txt')