# A.1.1

- [x] Refacerea structurii serverului gateway si refactorizarea folosind tiparul arhitectural de  “mixin”
- [x] Refacerea structurii serverului template de microservicii si refactorizarea folosind tiparul arhitectural de “mixin”
- [x] Pregatirea unui script de tip “debug containerizat”  pentru biblioteca
- [x] Integrarea proceselor de tip suport (inceputa in perioada de referinta curenta a raportului)
- [x] Lansarea versiunii 8.5 a bibliotecii de baza integrate in “Mobile Neural Powerplant” (initial 7.0) si in final release-ul 9.0 (la finalizarea proiectului)
- [x] Realizarea unui mediu avansat de tip .devcontainer pentru replicabilitatea totala a mediului de dezvoltare
- [x] Tecerea de la Azure la GCP pentru rulare si testare in mediu specializat containerizarii cu conexiune securizata SSL
- [x] Completarea documentatiei de utilizare a bibliotecii de baza si a serverului gateway cu includerea operationalizarii si a CI/CD in GCP inclusiv `cloudbuild.yaml` si integrarea acesteia in analiza de piata impreuna cu furnizorul extern
- [x] Completarea documentatiei de utilizare a sistemului pentru utilizarea `.devcontainer` cu componetele sale aferente `Dockerfile` si `devcontainer.json` si integrarea acesteia in analiza de piata impreuna cu furnizorul extern
- [x] Endpoint demonstrativ pentru limbaj ofensiv proiectat

# A.1.2 (Extern)

- [x] Proiectare si dezvoltare experimentala sistem DevOps bazat pe Ansible pentru deployment-ul infrastructurii complete
- [x] Executia si implementarea mediului final (complet) al infrastructurii de productie (in-situ la nivelul unitatii mobile)
- [x] Revizia sistemului de monitorizare microservicii
- [x] Endpoint demonstrativ pentru limbaj ofensiv dezvoltat in baza cerintelor


# A.2.1

- [ ] Integrarea finala a sistemului de suport:
  - [ ] Baza de date interna in gateway (serii de timp cu datele de monitorizare continand metricile de performanta)
  - [ ] Sumarizare in request-ul de`system_status` a informatiilor venite din monitor
  - [ ] Alertare pentru depasire de praguri de memorie, disk si cpu
  - [ ] Adaugare/finalizare `support_update_status` pentru fiecare semnatura de tip suport
- [ ] Elemente nivel jos: adaugarea de monitorizare de procese si thread-uri la nivel de sistem
- [ ] Endpoint /support_update_status: similar cu sisteme de monitorizare care ofera puncte de verificare a sanatații, este crucial ca acest endpoint sa fie verificat si testat riguros.
- [ ] Analiza de serie de Timp: aceasta este o direcție de evoluție importanta, care poate îmbogați valoarea datelor colectate, similar cu ce ofera soluții precum InfluxDB (https://www.influxdata.com/).
- [ ] Recepționarea Listei de servere si Microservicii: aceasta permite scalarea dinamica a monitorizarii, un concept crucial în sisteme reactive.
- [ ] Monitorizare Individuala: Monitorizarea granulara a fiecarei entitați poate ajuta la diagnosticarea rapida si eficienta a problemelor, similar cu funcționalitațile oferite de Datadog (https://www.datadoghq.com/).


# A.2.2

- [x] Dezvoltarea mediului suport de verificare si asigurare a replicabiltatii bazat pe devcontainer
- [x] Proiectarea testarii si pre-testare in laborator a unui prototip demonstrator pentru analiza limbajului ofensiv in limba romana.
- [x] Integrarea testelor externalizate
- [x] Compilarea rapoartelor de testare
- [x] Convertirea raportului de analiza de piata in format markdown si integrarea in documentatia de proiect


# A.3.1

- [x] Rafinarea chatbot-ului Telegram cu capacitati neurale avansate si transformarea acestuia intr-un tipar replicabil 
- [x] Preluarea si integrarea microserviciului de analiza a limbajului ofensiv in limba romana
