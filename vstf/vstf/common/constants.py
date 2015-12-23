slave_project_path = "/opt/esp-atf"
VSTFCPATH = "/opt/vstf"
sockaddr = VSTFCPATH + "/vstf.socket"
vstf_pid = VSTFCPATH + "/vstf-server.pid"
buff_size = 1024

# the message's len must be < 9999999999
MSG_FLAG_LEN = 10
MSG_FLAG = "%010d"

# all command run timeout
TIMEOUT = 20
# timmer SECOND
TICK = 3

HW_INFO = "HW_INFO"
CPU_INFO = "CPU INFO"
MEMORY_INFO = "MEMORY INFO"
OS_INFO = "OS INFO"

TOOLS = ["pktgen", "netperf", "qperf", "netmap"]
OPERATIONS = ["start", "stop", "restart"]
ACTIONS = ["send", "receive"]
PROTOCOLS = ["tcp_lat", "udp_lat", "tcp_bw", "udp_bw"]
TPROTOCOLS = ["tcp", "udp"]
PROFILES = ["rdp", "fastlink", "l2switch"]
TTYPES = ["throughput", "latency", "frameloss"]
SCENARIOS = ["Ti", "Tn", "Tnv", "Tu"]
SOCKET_BUF = 102400
WAIT_BALANCE = 2
CPU_USAGE_ROUND = 2
PKTLOSS_ROUND = 2
RATEP_ROUND = 3
TIME_ROUND = 3
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
TIME_STR = "%Y%m%d_%H%M%S"
REPORT_DEFAULTS = "/tmp"

CASE_ACTOR_MAP = {
    # unidirection
    "Tn-1": {"senders": [0], "receivers": [-1], "flows": 1},
    "Tn-2": {"senders": [0, -1], "receivers": [-1, 0], "flows": 2},
    # unidirection with vxlan
    "Tn-3": {"senders": [0], "receivers": [-1], "flows": 1},
    "Tn-4": {"senders": [0, -1], "receivers": [-1, 0], "flows": 2},
    # unidirection
    "Tnv-1": {"senders": [0], "receivers": [-1], "flows": 1},
    "Tnv-2": {"senders": [0, -1], "receivers": [-1, 0], "flows": 2},
    # unidirection with vxlan
    "Tnv-3": {"senders": [0], "receivers": [-1], "flows": 1},
    "Tnv-4": {"senders": [0, -1], "receivers": [-1, 0], "flows": 2},

    "Ti-1": {"senders": [0], "receivers": [-1], "flows": 1},
    "Ti-2": {"senders": [-1], "receivers": [0], "flows": 1},
    "Ti-3": {"senders": [0, -1], "receivers": [-1, 0], "flows": 2},
    "Ti-4": {"senders": [0], "receivers": [-1], "flows": 1},
    "Ti-5": {"senders": [-1], "receivers": [0], "flows": 1},
    "Ti-6": {"senders": [0, -1], "receivers": [-1, 0], "flows": 2},

    "Tu-1": {"senders": [0], "receivers": [-1], "flows": 1},
    "Tu-2": {"senders": [-1], "receivers": [0], "flows": 1},
    "Tu-3": {"senders": [0, -1], "receivers": [-1, 0], "flows": 2},
    "Tu-4": {"senders": [0], "receivers": [-1], "flows": 1},
    "Tu-5": {"senders": [-1], "receivers": [0], "flows": 1},
    "Tu-6": {"senders": [0, -1], "receivers": [-1, 0], "flows": 2}
}
