# Neural Energy - basic full inference server based on microservice-gateway architecture


# Romanian Section

## Prezentare / finantare proiect

Repository-ul de cod principal al proiectului „Mobile Neural Powerplant” – cod SMIS 156244. Acest proiect este finanțat în cadrul Programului Operational Competitivitate 2014-2020, Componenta 1: Întreprinderi inovatoare de tip start-up si spin-off - Apel 2022, Axa Prioritară: Cercetare, dezvoltare tehnologica si inovare (CDI) în sprijinul competitivitatii economice si dezvoltarii afacerilor, Operatiunea: Stimularea cererii întreprinderilor pentru inovare prin proiecte CDI derulate de întreprinderi individual sau în parteneriat cu institute de CD si universitati, în scopul inovarii de procese si de produse în sectoarele economice care prezinta potential de crestere.

> **Nota**
> In repo se regasesc parti dezvoltate de catre contractorul extern Neuroplastic Software SRL. Aceasta renunta la orice drept de proprietate intelectuala in favoarea beneficiarului proiectului, respectiv Neural Energy SRL.

## Istoric

 - 2023-10-01 - (in lucru) - Dezvoltare MVP faza 2 incluzand module de supervizare si depanare si aplicatii demonstrative
 - 2023-07-01 - 2023-09-31 - Dezvoltare MVP faza 1 incluzand integrarea submodule-ului `basic_inference_server`
 - 2023-03-01 - 2023-06-31 - Pregatirea principalelor componente la nivel de prototip nefunctional (inclusiv documentatia aferenta)

> Statusul actual se poate regasi in [TODO.md](TODO.md)
 
## Implementare si productizare

Această secțiune a documentației prezintă aspectele CI/CD, precum și definițiile de bază ale API. Informații suplimentare despre API pot fi găsite în secțiunea de API de mai jos.

> **Notă**
> În acestă documentație, veți observa diferite valori pentru `ver`, `worker_ver` și `time` în diverse exemple de răspunsuri. Acest lucru se datorează faptului că documentația a fost completată în mod progresiv.

### Aspecte generale ale CI/CD

Toate microserviciile sunt găzduite sub aceeași arhitectura distribuită, permițând procesare pe mai mulți muncitori. Fiecare microserviciu este definit de cel puțin o proprietate - de exemplu, `"SIGNATURE"`.
Imposibilitatea de a identifica microserviciul va genera o eroare. Operațiunea de `push` a repository-ului principal va declanșa construcția automată a repository-ului DockerHub.
După construcția automată, este necesară o simplă comandă `http://<server>:5002/shutdown` pentru a reporni și a actualiza containerul Docker de pe server.


Pe server, un script simplu controlează containerul prin comanda:
```bash
nohup ./run.sh &
```
Această comandă rulează scriptul în fundal. `nohup` vine de la 'no hang up', ceea ce înseamnă că scriptul va continua să ruleze chiar dacă utilizatorul se deconectează sau dacă shell-ul este închis. Operatorul `&` pune procesul în fundal.

Scriptul `run.sh` include următoarele instrucțiuni:
```bash
#!/bin/bash

while true; do
  sudo docker run --rm --name ne_ailib --env-file <path_to_env_file>/.env --pull=always -p 5002-5010:5002-5010 -v ai_vol:/aid_app/_cache neuralenergy/ai_library
  sleep 5
done
```

> **Nota **
> Din motive de securitate toate cheile secrete vor fi stocate intr-un fisier de tip .env si vor fi folosite la lansarea containerului cu ajutorul parametrului `--env-file` ca in exemplul de mai sus.

Scriptul `run.sh` se ruleaza cu `nohup ./run.sh &` si are scopul de a menține containerul Docker în funcțiune. Dacă containerul Docker se oprește dintr-un motiv oarecare, acest script asigură că o nouă instanță a containerului Docker este pornită după 5 secunde.

Rezultatul este că datele vor rămâne persistente de la o sesiune la alta în `ai_vol`, care este de obicei localizat la `/var/lib/docker/volumes/ai_vol/_data`.

Este recomandată o mașină virtuală (VM) simplă Azure sau AWS cu Ubuntu 18+. Instrucțiunile de instalare se găsesc mai jos. O VM oferă un mediu controlat și izolat, ideal pentru testarea sau implementarea unui software nou. În plus, AWS și Azure oferă resurse de calcul scalabile, ceea ce poate fi benefic dacă aveți nevoie să creșteți sau să reduceți resursele în funcție de cerere.



# English Section

## General information

This section of documentation presents CI/CD aspects as well as basic API definitions. Extended API information can be found in below API section.

> **Note**
> Within this documentation you will see different `ver`, `worker_ver` and `time` in various example responses. This is due to the fact that the documentation has been completed gradually.

### Overall CI/CD aspects

All microservices are hosted under the same distributed gateway enabling multi-worker processing. Each microservice is defined by at least one property - i.e.`"SIGNATURE"`.
Failure to identify the microservice will yield an error. Main repo `push` operation will trigger autobuild of DockerHub repo.
Following automatic build a simple `http://<server>:5002/shutdown` command is required to restart and update the Docker container on the server.


On server a simple script is running the container with 
```
nohup ./run.sh &
```

The `run.sh` contains the following script:
```
#!/bin/bash

while true; do
  sudo docker run --rm --name ne_ailib --env-file <path_to_env_file>/.env --pull=always -p 5002-5010:5002-5010 -v ai_vol/aid_app/_cache NeuralEnergy/ai_library
  sleep 5
done
```

As a result the data will be persistent from one session to another in the `ai_vol` usually found in `/var/lib/docker/volumes/ai_vol/_data`

A simple Azure or AWS Ubuntu 18+ VM is recommanded. See below the installation instructions.

### Development

#### Docker build

```
docker build -t org/repo .
```

...or a dev local build

```
docker build -t localsw .
```

> **Note**
> Place make sure env is prepared. Currently the env contains a couple neural word embeddings bundled within the env layer.

#### Docker run

```
docker run --rm --name ne_ailib --env-file <path_to_env_file>/.env --pull=always -p 5002-5010:5002-5010 -v ai_vol:/aid_app/_cache org/repo
```

or run locally

```
docker run --rm --name ne_ailib --env-file <path_to_env_file>/.env -p 5002-5010:5002-5010 localsw
```

> **Note**
> Always include volume `-v` and port forwarding `-p`.

### Usage

The engine itself works as a microservice gateway with multiple servers running their parallel workers. The list of active servers can be queried by running a `POST` on `<address>:5002/list_servers` resulting in a response similar with this 
```
{
    "AVAIL_SERVERS": [
        "dummy_model_a",
        "test_01"
    ]
}
```

#### Restart/update all servers within automated container

Run `POST` on `<address>:5002/shutdown` with the following JSON:

```
{
    "SIGNATURE" : "SAFE_KILL_SERVER_CMD"
}
```


#### Querying a microservice

Run a `POST` on `<address>:5002/run` with the following JSON:

```
{
    "SIGNATURE" : "test_01",
    ...
}
```

While `SIGNATURE` is mandatory for any microservice the other fields are dependent of the particular endpoint.


For more information please see API section below.

#### Azure VM install

To install Docker on an Azure VM with Ubuntu, follow these steps:

1. Update the packages list:
```
sudo apt-get update
```
2. Install prerequisite packages:
```
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```

3. Add Docker's official GPG key:
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

4. Set up the Docker repository:
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5. Update the packages list again:
```
sudo apt-get update
```

6. Install Docker:
```
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

7. Verify the installation by checking the Docker version:
```
docker --version
```

8. Start the Docker service and enable it to start on boot:
```
sudo systemctl enable docker
sudo systemctl start docker
```

9. Create inbound rule with `*` as source and `5002-5010` as destination then make sure you `sudo docker login` on the VM


## Neural Energy AI Library API information

In this section specific information about various microservices is provided.


### API definition for utility features

Most of the endpoints have the following utility features

#### Get system health status

Getting system status requires a simple API call `POST <address>:5002/run`:

```
{
    "SYSTEM_STATUS": {
        "info": "Memory Size is in GB. Total and avail mem may be reported inconsistently in containers.",
        "mem_avail": 22.88,
        "mem_gateway": 0.13,
        "mem_servers": {
            "basic_quiz_model": 0.56,
            "dummy_model_a": 0.14
        },
        "mem_sys": 1.14,
        "mem_total": 24.85,
        "mem_used": 0.83
    },
    "time": "2023-05-02 07:46:45",
    "ver": "2.3.2"
}
```

# Citation / citare

Please use the following bibtex entry / In situatia utilizarii bibliotecii va rugam citati in urmatorul mod:

```bibtex
@article{aid2023neuralenergy,
  title={Mobile Neural Powerplant},
  author={Damian, Andrei Ionut and Cristea, Mihai and Nemes, Ovidiu},
  year={2023}
}
``````
