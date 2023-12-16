
# Consideratii 


1. **Cereri în Serie**: În metoda `test_burst_requests`, se folosește o buclă pentru a trimite mai multe cereri către endpoint. Puteți ajusta numărul de iterații conform cerințelor dvs.

2. **Colectarea Semnăturilor Unice**: Scriptul folosește un set (`self.unique_signatures`) pentru a stoca valorile unice ale câmpului "signature" din fiecare răspuns. Setul asigură că sunt păstrate doar valorile unice.

3. **Afișarea Rezultatelor**: Metoda `tearDown` este suprascrisă pentru a afișa semnăturile unice după finalizarea tuturor testelor. Această metodă este apelată automat după fiecare metodă de test din clasă.

4. **Solicitarea Endpoint-ului**: Trimiterea cererilor în serie poate pune o încărcătură semnificativă pe endpoint. Asigurați-vă că endpoint-ul dvs. poate gestiona acest lucru fără probleme, în special dacă testați într-un mediu de producție.

5. **Mediul de Testare**: Preferați întotdeauna testarea într-un mediu de dezvoltare sau staging pentru a evita impactul asupra utilizatorilor reali sau a datelor.


# Rezultate de test 1

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

# Test output 2

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


# Model call 1

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

# Model call 2

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