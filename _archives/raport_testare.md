
# Consideratii 


1. **Cereri în Serie**: În metoda `test_burst_requests`, se folosește o buclă pentru a trimite mai multe cereri către endpoint. Puteți ajusta numărul de iterații conform cerințelor dvs.

2. **Colectarea Semnăturilor Unice**: Scriptul folosește un set (`self.unique_signatures`) pentru a stoca valorile unice ale câmpului "signature" din fiecare răspuns. Setul asigură că sunt păstrate doar valorile unice.

3. **Afișarea Rezultatelor**: Metoda `tearDown` este suprascrisă pentru a afișa semnăturile unice după finalizarea tuturor testelor. Această metodă este apelată automat după fiecare metodă de test din clasă.

4. **Solicitarea Endpoint-ului**: Trimiterea cererilor în serie poate pune o încărcătură semnificativă pe endpoint. Asigurați-vă că endpoint-ul dvs. poate gestiona acest lucru fără probleme, în special dacă testați într-un mediu de producție.

5. **Mediul de Testare**: Preferați întotdeauna testarea într-un mediu de dezvoltare sau staging pentru a evita impactul asupra utilizatorilor reali sau a datelor.


# Rezultate de test 1 (unittest)

Aceasta rulare a fost generata cu script-ul de test `tests/test2.py` care a fost rulat in dev-container si a facut request-uri la endpoint-ul de test din Google Cloud Platform in regim de burst.

```bash
root@3d212eb79e72:/workspaces/501_NeuralEnergy# python tests/test2.py
test_burst_requests (__main__.TestGCPModelEndpoint)
Test the GCP model endpoint with burst requests. ... 
Unique Signatures Collected:
{
    "h25a5.test_model_b.TestModelBWorker.0": 6,
    "h25a5.test_model_b.TestModelBWorker.1": 4
}

Unique dummy predicts outputs collected:
{
    "5001*1 + 2 = 5003 PREDICTED": 1,
    "2709*1 + 2 = 2711 PREDICTED": 1,
    "8843*1 + 2 = 8845 PREDICTED": 1,
    "9000*1 + 2 = 9002 PREDICTED": 1,
    "5817*1 + 2 = 5819 PREDICTED": 1,
    "1049*1 + 2 = 1051 PREDICTED": 1,
    "5789*1 + 2 = 5791 PREDICTED": 1,
    "2656*1 + 2 = 2658 PREDICTED": 1,
    "4828*1 + 2 = 4830 PREDICTED": 1,
    "8927*1 + 2 = 8929 PREDICTED": 1
}
ok

----------------------------------------------------------------------
Ran 1 test in 2.678s

OK
```

# Rezultate unit-testing #2

Aceasta rulare a fost generata cu script-ul de test `tests/test2.py` care a fost rulat in dev-container si a facut request-uri la endpoint-ul de test din Google Cloud Platform in regim de burst.

```bash
root@3d212eb79e72:/workspaces/501_NeuralEnergy# python tests/test2.py
test_burst_requests (__main__.TestGCPModelEndpoint)
Test the GCP model endpoint with burst requests. ... 
Unique Signatures Collected:
{
    "h25a5.test_model_b.TestModelBWorker.1": 7,
    "h25a5.test_model_b.TestModelBWorker.0": 3
}

Unique dummy predicts outputs collected:
{
    "5987*1 + 2 = 5989 PREDICTED": 1,
    "181*1 + 2 = 183 PREDICTED": 1,
    "4131*1 + 2 = 4133 PREDICTED": 1,
    "8591*1 + 2 = 8593 PREDICTED": 1,
    "135*1 + 2 = 137 PREDICTED": 1,
    "590*1 + 2 = 592 PREDICTED": 1,
    "8860*1 + 2 = 8862 PREDICTED": 1,
    "5801*1 + 2 = 5803 PREDICTED": 1,
    "8312*1 + 2 = 8314 PREDICTED": 1,
    "5243*1 + 2 = 5245 PREDICTED": 1
}
ok

----------------------------------------------------------------------
Ran 1 test in 2.694s

OK
```


# Apel model 1

Aceasta rulare a fost generata cu ajutorul Postman si a fost facuta la endpoint-ul de test din Google Cloud Platform.

```json
{
    "call_id": 22,
    "gw-uptime": "0:09:25",
    "hostname": "unknown",
    "predict_result": {
        "description": "Neural Energy inference test endpoint #2",
        "dummy_model_predict": "100*1 + 2 = 102 PREDICTED"
    },
    "signature": "h25a5.test_model_b.TestModelBWorker.1",
    "time": "2023-12-15 23:59:45",
    "ver-app": "2.5.4",
    "ver-lib": "8.9.4",
    "worker_id": "h25a5:1"
}
```

# Apel model 2

Aceasta rulare a fost generata cu ajutorul Postman si a fost facuta la endpoint-ul de test din Google Cloud Platform.

```json
{
    "call_id": 1,
    "gw-uptime": "0:02:53",
    "hostname": "unknown",
    "predict_result": {
        "description": "Neural Energy inference test endpoint #2",
        "dummy_model_predict": "100.0*10 + 5 = 1005.0 PREDICTED"
    },
    "signature": "h9c2c.test_model_b.TestModelBWorker.0",
    "time": "2023-12-16 00:04:56",
    "ver-app": "2.5.5",
    "ver-lib": "8.9.4",
    "worker_id": "h9c2c:0"
}
```

# Rulare locala

In vederea analizarii functionarii locale cu mediul devcontainer a fost rulat script-ul cu `python run_gateway.py` in consola locala.

```bash
[hc528: APPv2.5.8][2023-12-17 14:19:00] Library [hc528: APPv2.5.8 v8.9.5] initialized on machine [3d212eb79e72][ Intel(R) Xeon(R) W-2133 CPU @ 3.60GHz].
[hc528: APPv2.5.8][2023-12-17 14:19:00]   Logger v8.9.5.
[hc528: APPv2.5.8][2023-12-17 14:19:00]   Python v3.10.13 (main, Sep 11 2023, 13:44:35) [GCC 11.2.0].
[hc528: APPv2.5.8][2023-12-17 14:19:00]   Logger DEBUG is enabled at Logger level 
[hc528: APPv2.5.8][2023-12-17 14:19:00]   App debug mode is enabled
[hc528: APPv2.5.8][2023-12-17 14:19:00]   Avail/Total RAM: 10.7 GB / 15.6 GB
[hc528: APPv2.5.8][2023-12-17 14:19:00] Running in normal mode (NO debug enabled)
[hc528: APPv2.5.8][2023-12-17 14:19:00] Running BaseAidApp v2.5.8 on:
  HostID: `hc528` (hostname: 3d212eb79e72)
  Path:   '/workspaces/501_NeuralEnergy'
  TZ:     Europe/Bucharest
  Py:     3.10.13
  OS:     Linux-5.15.133.1-microsoft-standard-WSL2-x86_64-with-glibc2.31
  Docker: True
[hc528: APPv2.5.8][2023-12-17 14:19:00] Show packages: Yes
[hc528: APPv2.5.8][2023-12-17 14:19:00] Packages: 
accelerate                0.24.1
aiohttp                   3.9.0
aiosignal                 1.3.1
annotated-types           0.6.0
anyio                     3.7.1
archspec                  0.2.2
argon2-cffi               21.3.0
argon2-cffi-bindings      21.2.0
asttokens                 2.0.5
astunparse                1.6.3
async-lru                 2.0.4
async-timeout             4.0.3
attrs                     23.1.0
babel                     2.11.0
backcall                  0.2.0
backoff                   1.11.1
beautifulsoup4            4.12.2
bitsandbytes              0.41.2.post2
bleach                    4.1.0
boltons                   23.0.0
bottleneck                1.3.5
brotli                    1.0.9
certifi                   2023.11.17
cffi                      1.15.1
chardet                   4.0.0
charset-normalizer        2.0.4
chromadb                  0.3.25
click                     8.1.7
clickhouse-connect        0.6.21
cloudpickle               2.2.1
coloredlogs               15.0.1
comm                      0.1.2
conda                     23.9.0
conda-build               3.27.0
conda-content-trust       0.2.0
conda-index               0.3.0
conda-libmamba-solver     23.7.0
conda-package-handling    2.2.0
conda-package-streaming   0.9.0
contourpy                 1.2.0
cryptography              41.0.3
cycler                    0.11.0
cytoolz                   0.12.0
dask                      2023.6.0
dataclasses               0.8
dataclasses-json          0.6.2
datasets                  2.14.7
debugpy                   1.6.7
decorator                 5.1.1
defusedxml                0.7.1
dill                      0.3.7
distro                    1.8.0
dnspython                 2.4.2
duckdb                    0.9.2
exceptiongroup            1.0.4
executing                 0.8.3
expecttest                0.1.6
fastapi                   0.103.2
fastjsonschema            2.16.2
filelock                  3.9.0
flask                     2.2.2
flatbuffers               23.5.26
fonttools                 4.25.0
frozenlist                1.4.0
fsspec                    2023.10.0
gensim                    4.3.0
gmpy2                     2.1.2
greenlet                  3.0.1
h11                       0.14.0
h5py                      3.9.0
hnswlib                   0.7.0
httpcore                  1.0.2
httpx                     0.25.2
huggingface-hub           0.16.4
humanfriendly             10.0
hypothesis                6.88.4
idna                      3.4
imagecodecs               2023.1.23
imageio                   2.31.4
importlib-metadata        6.8.0
ipykernel                 6.25.0
ipython                   8.15.0
ipywidgets                8.0.4
itsdangerous              2.0.1
jedi                      0.18.1
jinja2                    3.1.2
joblib                    1.3.2
json5                     0.9.6
jsonpatch                 1.33
jsonpointer               2.1
jsonschema                4.19.2
jsonschema-specifications 2023.7.1
jupyter                   1.0.0
jupyter-client            8.6.0
jupyter-console           6.6.3
jupyter-core              5.5.0
jupyter-events            0.8.0
jupyter-lsp               2.2.0
jupyter-server            2.10.0
jupyter-server-terminals  0.4.4
jupyterlab                4.0.8
jupyterlab-pygments       0.1.2
jupyterlab-server         2.25.1
jupyterlab-widgets        3.0.9
kiwisolver                1.4.4
langchain                 0.0.340
langsmith                 0.0.66
lark                      1.1.8
lazy-loader               0.3
libarchive-c              2.9
libmambapy                1.5.1
locket                    1.0.0
lz4                       4.3.2
markupsafe                2.1.1
marshmallow               3.20.1
matplotlib                3.8.0
matplotlib-inline         0.1.6
mistune                   2.0.4
mkl-fft                   1.3.8
mkl-random                1.2.4
mkl-service               2.4.0
monotonic                 1.5
more-itertools            8.12.0
mpmath                    1.3.0
multidict                 6.0.4
multiprocess              0.70.15
munkres                   1.1.4
mutagen                   1.47.0
mypy-extensions           1.0.0
nbclient                  0.8.0
nbconvert                 7.10.0
nbformat                  5.9.2
nest-asyncio              1.5.6
networkx                  3.1
notebook                  7.0.6
notebook-shim             0.2.3
numexpr                   2.8.7
numpy                     1.26.0
onnxruntime               1.16.3
openai                    1.3.5
overrides                 7.4.0
packaging                 23.1
pandas                    2.1.1
pandocfilters             1.5.0
parso                     0.8.3
partd                     1.4.1
peft                      0.6.2
pexpect                   4.8.0
pickleshare               0.7.5
pillow                    10.0.1
pip                       23.3
pkginfo                   1.9.6
platformdirs              3.10.0
pluggy                    1.0.0
ply                       3.11
posthog                   3.0.2
prometheus-client         0.14.1
prompt-toolkit            3.0.36
protobuf                  3.20.3
psutil                    5.9.0
ptyprocess                0.7.0
pure-eval                 0.2.2
pyarrow                   11.0.0
pyarrow-hotfix            0.6
pycosat                   0.6.6
pycparser                 2.21
pycryptodomex             3.19.0
pydantic                  2.5.2
pydantic-core             2.14.5
pydub                     0.25.1
pygments                  2.15.1
pymssql                   2.2.5
pyopenssl                 23.2.0
pyparsing                 3.0.9
pypdf                     3.17.1
pyqt5                     5.15.10
pyqt5-sip                 12.13.0
pysocks                   1.7.1
python-dateutil           2.8.2
python-dotenv             1.0.0
python-etcd               0.4.5
python-json-logger        2.0.7
python-telegram-bot       20.6
pytz                      2023.3.post1
pywavelets                1.4.1
pyyaml                    6.0.1
pyzmq                     25.1.0
qtconsole                 5.5.0
qtpy                      2.4.1
referencing               0.30.2
regex                     2023.10.3
requests                  2.31.0
rfc3339-validator         0.1.4
rfc3986-validator         0.1.1
rpds-py                   0.10.6
ruamel.yaml               0.17.21
ruamel.yaml.clib          0.2.6
sacremoses                0.0.53
safetensors               0.3.3
scikit-image              0.20.0
scikit-learn              1.3.0
scipy                     1.11.3
seaborn                   0.12.2
send2trash                1.8.2
sentencepiece             0.1.99
setuptools                68.0.0
sip                       6.7.12
six                       1.16.0
smart-open                5.2.1
sniffio                   1.3.0
sortedcontainers          2.4.0
soupsieve                 2.5
sqlalchemy                2.0.23
stack-data                0.2.0
starlette                 0.27.0
sympy                     1.11.1
tenacity                  8.2.3
terminado                 0.17.1
threadpoolctl             2.2.0
tifffile                  2023.4.12
tiktoken                  0.5.1
tinycss2                  1.2.1
tokenizers                0.14.1
tomli                     2.0.1
toolz                     0.12.0
torch                     2.1.1
torchaudio                2.1.1
torchelastic              0.2.2
torchvision               0.16.1
tornado                   6.3.3
tqdm                      4.65.0
traitlets                 5.7.1
transformers              4.35.0
triton                    2.1.0
truststore                0.8.0
types-dataclasses         0.6.6
typing-extensions         4.7.1
typing-inspect            0.9.0
typing-utils              0.1.0
tzdata                    2023.3
unidecode                 1.2.0
urllib3                   1.26.18
uvicorn                   0.24.0
wcwidth                   0.2.5
webencodings              0.5.1
websocket-client          0.58.0
websockets                12.0
werkzeug                  2.2.2
wheel                     0.41.2
widgetsnbextension        4.0.5
xxhash                    3.4.1
yarl                      1.9.2
yt-dlp                    2023.11.16
zipp                      3.17.0
zstandard                 0.19.0
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] NEAIL_TELEGRAM_TOKEN: 608****************************************MsE
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] AID_APP_ENV: v1.2
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] AID_APP_SHOW_PACKS: Yes
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] AID_APP_DOCKER: Yes
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] NEAIL_GPT_KEY: sk-*********************************************W3F
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] NEAIL_MOTION_TOKEN: 609****************************************W44
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] AID_APP_ID: BaseAidApp
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] NEAIL_HF_TOKEN: hf_*******************************tZE
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] NEAIL_VERSION: 1.0.2
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] AID_APP_DEBUG: Yes
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] AID_APP_FORCE_CPU: No
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Loading gateway state history from: ./_cache/_data/gw_state_history.json
[hc528: APPv2.5.8][2023-12-17 14:19:04] Loading json 'gw_state_history.json' from 'data'
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Loaded gateway state history:
{
  "CURRENT_STARTUP": "2023-12-15 23:54:15",
  "LAST_RUNTIME_HOURS": "0:01:23",
  "LAST_SHUTDOWN": "2023-12-15 23:55:38",
  "PREVIOUS_STARTUP": "2023-12-15 23:30:24"
}
[hc528: APPv2.5.8][2023-12-17 14:19:04] 
                                          ===================================================
                                          |                                                 |
                                          |  FlaskGateway v8.9.5 started on '0.0.0.0:5002'  |
                                          |                                                 |
                                          ===================================================

[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Registering /start_server on `_view_func_start_server`
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Registering /kill_server on `_view_func_kill_server`
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Registering /list_servers on `_view_list_servers`
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Registering /system_status on `_view_system_status`
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Registering /support_update_status on `_view_support_status`
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Registering /shutdown on `_view_shutdown`
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW]   Starting microservice server 'test_model_a' ...
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Attempting to start server with "SIGNATURE" : "test_model_a"
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW]   Description: "Test server #1"
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Creating server `test_model_a <test_model_a>` at 127.0.0.1:5003/run
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Running ['python', 'basic_inference_server/basic_inference_server/model_server/run_server.py', '--base_folder', '.', '--app_folder', '_cache', '--config_endpoint', '{"NR_WORKERS": 2, "HOST": "127.0.0.1", "DESCRIPTION": "Test server #1"}', '--host', '127.0.0.1', '--port', '5003', '--execution_path', '/run', '--workers_location', 'endpoints', '--worker_name', 'test_model_a', '--worker_suffix', 'Worker', '--microservice_name', 'test_model_a', '--nr_workers', '2', '--host_id', 'hc528', '--use_tf']
[hc528: APPv2.5.8][2023-12-17 14:19:04] [GW] Waiting for process to 62783 warmup...
run_server cwd: /workspaces/501_NeuralEnergy
BASE: ./_cache
[hc528: TMA][2023-12-17 14:19:06] ./_cache/_logs/hc528: TMA.txt log changed to ./_cache/_logs/20231217_141906_TMA_001_log.txt...
[hc528: TMA][2023-12-17 14:19:06] Library [hc528: TMA v8.9.5] initialized on machine [3d212eb79e72][ Intel(R) Xeon(R) W-2133 CPU @ 3.60GHz].
[hc528: TMA][2023-12-17 14:19:06]   Logger v8.9.5.
[hc528: TMA][2023-12-17 14:19:06]   Python v3.10.13 (main, Sep 11 2023, 13:44:35) [GCC 11.2.0].
[hc528: TMA][2023-12-17 14:19:06]   Logger DEBUG is enabled at Logger level 
[hc528: TMA][2023-12-17 14:19:06]   App debug mode is enabled
[hc528: TMA][2023-12-17 14:19:06]   Avail/Total RAM: 10.7 GB / 15.6 GB
[hc528: APPv2.5.8][2023-12-17 14:19:06] [GW] Successfully created server 'test_model_a' with PID=62783
[hc528: APPv2.5.8][2023-12-17 14:19:06] [GW]   Starting microservice server 'test_model_a-bis' ...
[hc528: APPv2.5.8][2023-12-17 14:19:06] [GW] Attempting to start server with "SIGNATURE" : "test_model_a-bis"
[hc528: APPv2.5.8][2023-12-17 14:19:06] [GW]   Description: "test_model_a server #2. Redundancy server for test_model_a"
[hc528: APPv2.5.8][2023-12-17 14:19:06] [GW] WARNING: Skipping server 'test_model_a-bis' due to its DISABLED status:
 {
    "SERVER_CLASS": "test_model_a",
    "NR_WORKERS": 2,
    "HOST": "127.0.0.1",
    "DISABLED": true,
    "DESCRIPTION": "test_model_a server #2. Redundancy server for test_model_a"
}
[hc528: APPv2.5.8][2023-12-17 14:19:06] [GW]   Starting microservice server 'test_model_b' ...
[hc528: APPv2.5.8][2023-12-17 14:19:07] [GW] Attempting to start server with "SIGNATURE" : "test_model_b"
[hc528: APPv2.5.8][2023-12-17 14:19:07] [GW]   Description: "test_model_b server #1"
[hc528: APPv2.5.8][2023-12-17 14:19:07] [GW] Creating server `test_model_b <test_model_b>` at 127.0.0.1:5004/run
[hc528: APPv2.5.8][2023-12-17 14:19:07] [GW] Running ['python', 'basic_inference_server/basic_inference_server/model_server/run_server.py', '--base_folder', '.', '--app_folder', '_cache', '--config_endpoint', '{"NR_WORKERS": 2, "HOST": "127.0.0.1", "DESCRIPTION": "test_model_b server #1"}', '--host', '127.0.0.1', '--port', '5004', '--execution_path', '/run', '--workers_location', 'endpoints', '--worker_name', 'test_model_b', '--worker_suffix', 'Worker', '--microservice_name', 'test_model_b', '--nr_workers', '2', '--host_id', 'hc528', '--use_tf']
[hc528: APPv2.5.8][2023-12-17 14:19:07] [GW] Waiting for process to 62818 warmup...
[hc528: TMA][2023-12-17 14:19:07] [FSKSVR] Creating 2 workers for server 'test_model_a'
[hc528: TMA][2023-12-17 14:19:07] [FSKSVR] FlaskModelServer found "USER" plugin 'test_model_a'
[hc528: TMA][2023-12-17 14:19:07] [FSKSVR]   Plugin 'test_model_a' loaded from 'endpoints'
[hc528: TMA][2023-12-17 14:19:07] [DUMA] Updating TestModelAWorker configuration...
[hc528: TMA][2023-12-17 14:19:07] [DUMA]   BIAS=0
[hc528: TMA][2023-12-17 14:19:07] [DUMA]   PLACEHOLDER_MODEL=True
[hc528: TMA][2023-12-17 14:19:07] [DUMA]   NR_WORKERS=2 [NEW]
[hc528: TMA][2023-12-17 14:19:07] [DUMA]   WEIGHT=0
[hc528: TMA][2023-12-17 14:19:07] [DUMA]   DESCRIPTION=Test server #1 [NEW]
[hc528: TMA][2023-12-17 14:19:07] [DUMA]   HOST=127.0.0.1 [NEW]
[hc528: TMA][2023-12-17 14:19:07] [DUMA] Resetting config_data ...
[hc528: TMA][2023-12-17 14:19:07] [DUMA] Running config handler creation...
[hc528: TMA][2023-12-17 14:19:07] [DUMA] Created 'TestModelAWorker' config_data handlers: ['cfg_weight', 'cfg_bias', 'cfg_placeholder_model', 'cfg_nr_workers', 'cfg_description', 'cfg_host']
[hc528: TMA][2023-12-17 14:19:07] [DUMA] Running validation...
[hc528: TMA][2023-12-17 14:19:07] [DUMA] Validating configuration for 'TestModelAWorker'...
[hc528: TMA][2023-12-17 14:19:07] [DUMA]   No validation configuration for 'TestModelAWorker'
[hc528: TMA][2023-12-17 14:19:07] ******** Using a model placeholder *********
[hc528: TMA][2023-12-17 14:19:07] Simulating a SLOW loading model
run_server cwd: /workspaces/501_NeuralEnergy
BASE: ./_cache
[hc528: TMB][2023-12-17 14:19:08] ./_cache/_logs/hc528: TMB.txt log changed to ./_cache/_logs/20231217_141908_TMB_001_log.txt...
[hc528: TMB][2023-12-17 14:19:08] Library [hc528: TMB v8.9.5] initialized on machine [3d212eb79e72][ Intel(R) Xeon(R) W-2133 CPU @ 3.60GHz].
[hc528: TMB][2023-12-17 14:19:08]   Logger v8.9.5.
[hc528: TMB][2023-12-17 14:19:08]   Python v3.10.13 (main, Sep 11 2023, 13:44:35) [GCC 11.2.0].
[hc528: TMB][2023-12-17 14:19:08]   Logger DEBUG is enabled at Logger level 
[hc528: TMB][2023-12-17 14:19:08]   App debug mode is enabled
[hc528: TMB][2023-12-17 14:19:08]   Avail/Total RAM: 10.6 GB / 15.6 GB
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Successfully created server 'test_model_b' with PID=62818
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Starting microservice server 'test_model_b-bis' ...
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Attempting to start server with "SIGNATURE" : "test_model_b-bis"
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Description: "test_model_b server #2. Redundancy server for test_model_b"
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] WARNING: Skipping server 'test_model_b-bis' due to its DISABLED status:
 {
    "SERVER_CLASS": "test_model_b",
    "NR_WORKERS": 2,
    "HOST": "127.0.0.1",
    "DISABLED": true,
    "DESCRIPTION": "test_model_b server #2. Redundancy server for test_model_b"
}
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Fast startup enabled, using default paths: ['/run', '/notifications', '/update_workers']
[hc528: TMB][2023-12-17 14:19:09] [FSKSVR] Creating 2 workers for server 'test_model_b'
[hc528: TMB][2023-12-17 14:19:09] [FSKSVR] FlaskModelServer found "USER" plugin 'test_model_b'
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Registering /run on `partial_view_func_run`
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Registering /notifications on `partial_view_func_notifications`
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Registering /update_workers on `partial_view_func_update_workers`
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Starting gateway server after all endpoints have been defined...
[hc528: TMB][2023-12-17 14:19:09] [FSKSVR]   Plugin 'test_model_b' loaded from 'endpoints'
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Updating TestModelBWorker configuration...
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Information for server 'NeuralEnergy':
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   NR_WORKERS=2 [NEW]
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   DESCRIPTION=test_model_b server #1 [NEW]
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Total server memory:     15.6 GB
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   HOST=127.0.0.1 [NEW]
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Total server avail mem:  10.6 GB
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   BIAS=2
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Total allocated mem:      0.4 GB
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   WEIGHT=1
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   System allocated mem:     4.7 GB
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Resetting config_data ...
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Disk free:   151.5 GB
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Running config handler creation...
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Disk total:  250.9 GB
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Created 'TestModelBWorker' config_data handlers: ['cfg_weight', 'cfg_bias', 'cfg_nr_workers', 'cfg_description', 'cfg_host']
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Starting support processes...
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Running validation...
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Starting support server 'nee' ...
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Validating configuration for 'TestModelBWorker'...
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Attempting to start server with "SIGNATURE" : "nee"
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   No validation configuration for 'TestModelBWorker'
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Description: "None"
[hc528: TMB][2023-12-17 14:19:09] [FSKSVR] FlaskModelServer found "USER" plugin 'test_model_b'
[hc528: TMB][2023-12-17 14:19:09] [FSKSVR]   Plugin 'test_model_b' loaded from 'endpoints'
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] *********************************************
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Updating TestModelBWorker configuration...
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW]   Creating SUPPORT process endpoints/nee.py  
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   NR_WORKERS=2 [NEW]
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] *********************************************
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   DESCRIPTION=test_model_b server #1 [NEW]
[hc528: APPv2.5.8][2023-12-17 14:19:09] [GW] Waiting for process to 62840 warmup...
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   HOST=127.0.0.1 [NEW]
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   BIAS=2
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   WEIGHT=1
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Resetting config_data ...
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Running config handler creation...
/workspaces/501_NeuralEnergy/endpoints/nee.py running from: /workspaces/501_NeuralEnergy
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Running validation...
[hc528: TMB][2023-12-17 14:19:09] [DUMB] Validating configuration for 'TestModelBWorker'...
[hc528: TMB][2023-12-17 14:19:09] [DUMB]   No validation configuration for 'TestModelBWorker'
[hc528: TMB][2023-12-17 14:19:09] 
        =============================================================================================================
        |                                                                                                           |
        |  FlaskModelServer v8.9.5 'test_model_b' <test_model_b code=TestModelBWorker> started on '127.0.0.1:5004'  |
        |                                                                                                           |
        =============================================================================================================

[hc528: TMB][2023-12-17 14:19:09] Given full config:
{
    "NR_WORKERS": 2,
    "HOST": "127.0.0.1",
    "DESCRIPTION": "test_model_b server #1"
}
 * Serving Flask app 'FlaskModelServer'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5004
Press CTRL+C to quit
BASE: ./_cache
[hc528: NEE][2023-12-17 14:19:11] ./_cache/_logs/hc528: NEE.txt log changed to ./_cache/_logs/20231217_141911_NEE_001_log.txt...
[hc528: NEE][2023-12-17 14:19:11] Library [hc528: NEE v8.9.5] initialized on machine [3d212eb79e72][ Intel(R) Xeon(R) W-2133 CPU @ 3.60GHz].
[hc528: NEE][2023-12-17 14:19:11]   Logger v8.9.5.
[hc528: NEE][2023-12-17 14:19:11]   Python v3.10.13 (main, Sep 11 2023, 13:44:35) [GCC 11.2.0].
[hc528: NEE][2023-12-17 14:19:11]   Logger DEBUG is enabled at Logger level 
[hc528: NEE][2023-12-17 14:19:11]   App debug mode is enabled
[hc528: NEE][2023-12-17 14:19:11]   Avail/Total RAM: 10.6 GB / 15.6 GB
[hc528: NEE][2023-12-17 14:19:11] 
                                    =====================================================
                                    |                                                   |
                                    |  App is running in debug mode - chatbot disabled  |
                                    |                                                   |
                                    =====================================================

[hc528: APPv2.5.8][2023-12-17 14:19:11] [GW] **************** Process failed for ['python', 'endpoints/nee.py', '--config_endpoint', '{"DISABLED": false, "HOST": "NO_HOST", "SERVER": "127.0.0.1", "SERVER_PORT": 5002, "SERVER_PATH": "/support_update_status", "SUPPORT_NAME": "nee"}', '--host_id', 'hc528']:NO_HOST:None *******************
[hc528: APPv2.5.8][2023-12-17 14:19:11] [GW]   Starting support server 'motion' ...
[hc528: APPv2.5.8][2023-12-17 14:19:11] [GW] Attempting to start server with "SIGNATURE" : "motion"
[hc528: APPv2.5.8][2023-12-17 14:19:11] [GW]   Description: "None"
[hc528: APPv2.5.8][2023-12-17 14:19:11] [GW] ************************************************
[hc528: APPv2.5.8][2023-12-17 14:19:11] [GW]   Creating SUPPORT process endpoints/motion.py  
[hc528: APPv2.5.8][2023-12-17 14:19:11] [GW] ************************************************
[hc528: APPv2.5.8][2023-12-17 14:19:11] [GW] Waiting for process to 62862 warmup...
/workspaces/501_NeuralEnergy/endpoints/motion.py running from: /workspaces/501_NeuralEnergy
BASE: ./_cache
[hc528: MO][2023-12-17 14:19:13] ./_cache/_logs/hc528: MO.txt log changed to ./_cache/_logs/20231217_141913_MO_001_log.txt...
[hc528: MO][2023-12-17 14:19:13] Library [hc528: MO v8.9.5] initialized on machine [3d212eb79e72][ Intel(R) Xeon(R) W-2133 CPU @ 3.60GHz].
[hc528: MO][2023-12-17 14:19:13]   Logger v8.9.5.
[hc528: MO][2023-12-17 14:19:13]   Python v3.10.13 (main, Sep 11 2023, 13:44:35) [GCC 11.2.0].
[hc528: MO][2023-12-17 14:19:13]   Logger DEBUG is enabled at Logger level 
[hc528: MO][2023-12-17 14:19:13]   App debug mode is enabled
[hc528: MO][2023-12-17 14:19:13]   Avail/Total RAM: 10.6 GB / 15.6 GB
[hc528: MO][2023-12-17 14:19:13] 
                                   =====================================================
                                   |                                                   |
                                   |  App is running in debug mode - chatbot disabled  |
                                   |                                                   |
                                   =====================================================

[hc528: APPv2.5.8][2023-12-17 14:19:13] [GW] **************** Process failed for ['python', 'endpoints/motion.py', '--config_endpoint', '{"DISABLED": false, "HOST": "NO_HOST", "SERVER": "127.0.0.1", "SERVER_PORT": 5002, "SERVER_PATH": "/support_update_status", "SUPPORT_NAME": "motion"}', '--host_id', 'hc528']:NO_HOST:None *******************
[hc528: APPv2.5.8][2023-12-17 14:19:13] [GW]   Starting support server 'ne_support' ...
[hc528: APPv2.5.8][2023-12-17 14:19:13] [GW] Attempting to start server with "SIGNATURE" : "ne_support"
[hc528: APPv2.5.8][2023-12-17 14:19:13] [GW]   Description: "Neural Energy base cluster support process."
[hc528: APPv2.5.8][2023-12-17 14:19:13] [GW] ****************************************************
[hc528: APPv2.5.8][2023-12-17 14:19:13] [GW]   Creating SUPPORT process endpoints/ne_support.py  
[hc528: APPv2.5.8][2023-12-17 14:19:13] [GW] ****************************************************
[hc528: APPv2.5.8][2023-12-17 14:19:13] [GW] Waiting for process to 62880 warmup...
/workspaces/501_NeuralEnergy/endpoints/ne_support.py running from: /workspaces/501_NeuralEnergy
Using --config_endpoint: {"HOST": "NO_HOST", "PING_INTERVAL": 600, "DESCRIPTION": "Neural Energy base cluster support process.", "SERVER": "127.0.0.1", "SERVER_PORT": 5002, "SERVER_PATH": "/support_update_status", "SUPPORT_NAME": "ne_support"}
BASE: ./_cache
[hc528: SPRC][2023-12-17 14:19:14] ./_cache/_logs/hc528: SPRC.txt log changed to ./_cache/_logs/20231217_141914_SPRC_001_log.txt...
[hc528: SPRC][2023-12-17 14:19:14] Library [hc528: SPRC v8.9.5] initialized on machine [3d212eb79e72][ Intel(R) Xeon(R) W-2133 CPU @ 3.60GHz].
[hc528: SPRC][2023-12-17 14:19:14]   Logger v8.9.5.
[hc528: SPRC][2023-12-17 14:19:14]   Python v3.10.13 (main, Sep 11 2023, 13:44:35) [GCC 11.2.0].
[hc528: SPRC][2023-12-17 14:19:14]   Logger DEBUG is enabled at Logger level 
[hc528: SPRC][2023-12-17 14:19:14]   App debug mode is enabled
[hc528: SPRC][2023-12-17 14:19:14]   Avail/Total RAM: 10.6 GB / 15.6 GB
[hc528: SPRC][2023-12-17 14:19:14] Using config_data: 
{
  "BASE_FOLDER": ".",
  "APP_FOLDER": "_cache",
  "HOST": "NO_HOST",
  "PING_INTERVAL": 600,
  "DESCRIPTION": "Neural Energy base cluster support process.",
  "SERVER": "127.0.0.1",
  "SERVER_PORT": 5002,
  "SERVER_PATH": "/support_update_status",
  "SUPPORT_NAME": "ne_support"
}
[hc528: SPRC][2023-12-17 14:19:15] 
        ===============================================================================================
        |                                                                                             |
        |  ServerMonitor v0.0.0 initialized on 127.0.0.1:5002/support_update_status at 600s interval  |
        |                                                                                             |
        ===============================================================================================

[hc528: APPv2.5.8][2023-12-17 14:19:15] [GW] Successfully created SUPPORT process 'ne_support' with PID=62880
[hc528: APPv2.5.8][2023-12-17 14:19:15] [GW] Fast startup enabled, using default paths: ['/run', '/notifications', '/update_workers']
[hc528: APPv2.5.8][2023-12-17 14:19:15] Saving data json: ./_cache/_data/gw_state_history.json
[hc528: APPv2.5.8][2023-12-17 14:19:15] [GW] Registering signal handler 2 ...
[hc528: APPv2.5.8][2023-12-17 14:19:15] [GW] Registering signal handler 15 ...
[hc528: APPv2.5.8][2023-12-17 14:19:15] [GW] Done registering signal handlers.
 * Serving Flask app 'FlaskGateway'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5002
 * Running on http://172.17.0.2:5002
Press CTRL+C to quit
[hc528: TMA][2023-12-17 14:19:37] [FSKSVR] FlaskModelServer found "USER" plugin 'test_model_a'
[hc528: TMA][2023-12-17 14:19:37] [FSKSVR]   Plugin 'test_model_a' loaded from 'endpoints'
[hc528: TMA][2023-12-17 14:19:37] [DUMA] Updating TestModelAWorker configuration...
[hc528: TMA][2023-12-17 14:19:37] [DUMA]   BIAS=0
[hc528: TMA][2023-12-17 14:19:37] [DUMA]   PLACEHOLDER_MODEL=True
[hc528: TMA][2023-12-17 14:19:37] [DUMA]   NR_WORKERS=2 [NEW]
[hc528: TMA][2023-12-17 14:19:37] [DUMA]   WEIGHT=0
[hc528: TMA][2023-12-17 14:19:37] [DUMA]   DESCRIPTION=Test server #1 [NEW]
[hc528: TMA][2023-12-17 14:19:37] [DUMA]   HOST=127.0.0.1 [NEW]
[hc528: TMA][2023-12-17 14:19:37] [DUMA] Resetting config_data ...
[hc528: TMA][2023-12-17 14:19:37] [DUMA] Running config handler creation...
[hc528: TMA][2023-12-17 14:19:37] [DUMA] Running validation...
[hc528: TMA][2023-12-17 14:19:37] [DUMA] Validating configuration for 'TestModelAWorker'...
[hc528: TMA][2023-12-17 14:19:37] [DUMA]   No validation configuration for 'TestModelAWorker'
[hc528: TMA][2023-12-17 14:19:37] ******** Using a model placeholder *********
[hc528: TMA][2023-12-17 14:19:37] Simulating a SLOW loading model
[hc528: TMA][2023-12-17 14:20:07] 
        =============================================================================================================
        |                                                                                                           |
        |  FlaskModelServer v8.9.5 'test_model_a' <test_model_a code=TestModelAWorker> started on '127.0.0.1:5003'  |
        |                                                                                                           |
        =============================================================================================================

[hc528: TMA][2023-12-17 14:20:07] Given full config:
{
    "NR_WORKERS": 2,
    "HOST": "127.0.0.1",
    "DESCRIPTION": "Test server #1"
}
 * Serving Flask app 'FlaskModelServer'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5003
Press CTRL+C to quit
^CTraceback (most recent call last):
[hc528: APPv2.5.8][2023-12-17 14:20:40] [GW] Signal received: 2. Performing safe shutdown...
  File "/workspaces/501_NeuralEnergy/endpoints/ne_support.py", line 64, in <module>
    engine.run()
  File "/workspaces/501_NeuralEnergy/models/support/base.py", line 87, in run
[hc528: APPv2.5.8][2023-12-17 14:20:40] [GW] Running gateway v2.5.8/8.9.5 shutdown...
    sleep(0.1)
KeyboardInterrupt
[hc528: APPv2.5.8][2023-12-17 14:20:40] [GW] Terminating server 'test_model_a' ...
[hc528: APPv2.5.8][2023-12-17 14:20:40] [GW]   'test_model_a' terminated with code: -15
[hc528: APPv2.5.8][2023-12-17 14:20:42] [GW]   Server 'test_model_a' deallocated.
[hc528: APPv2.5.8][2023-12-17 14:20:42] [GW] Terminating server 'test_model_b' ...
[hc528: APPv2.5.8][2023-12-17 14:20:42] [GW]   'test_model_b' terminated with code: 0
[hc528: APPv2.5.8][2023-12-17 14:20:44] [GW]   Server 'test_model_b' deallocated.
[hc528: APPv2.5.8][2023-12-17 14:20:44] [GW] Terminating server 'ne_support' ...
[hc528: APPv2.5.8][2023-12-17 14:20:44] [GW]   'ne_support' terminated with code: -2
[hc528: APPv2.5.8][2023-12-17 14:20:46] [GW]   Server 'ne_support' deallocated.
[hc528: APPv2.5.8][2023-12-17 14:20:46] Saving data json: ./_cache/_data/gw_state_history.json
[hc528: APPv2.5.8][2023-12-17 14:20:46] [GW] Terminating gateway server v2.5.8/8.9.5 with pid 62725 with signal 9...
Killed
```