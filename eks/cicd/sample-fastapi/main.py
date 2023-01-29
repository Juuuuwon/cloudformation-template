import uvicorn
from uvicorn.config import LOGGING_CONFIG

LOGGING_CONFIG["formatters"]["default"][
    "fmt"
] = "%(asctime)s [%(name)s] %(levelprefix)s %(message)s"
LOGGING_CONFIG["formatters"]["access"][
    "fmt"
] = '%(asctime)s [%(name)s] %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=80, log_config=LOGGING_CONFIG, reload=True)
