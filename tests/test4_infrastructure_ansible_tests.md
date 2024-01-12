

```bash
root@50af5a306d71:/workspaces/501_NeuralEnergy/ansible# ./run.sh 

PLAY [Deploy on GPU Workers] ************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************
ok: [ne4]
ok: [ne2]
ok: [ne3]
ok: [ne1]

TASK [stage01_gpu : Check if NVIDIA-SMI is available and working] ***********************************************************************************************
changed: [ne2]
changed: [ne3]
changed: [ne4]
changed: [ne1]

TASK [stage01_gpu : Cleanup existing NVIDIA drivers] ************************************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Reboot the system] **************************************************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Wait for system to come back online after reboot] *******************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Update package lists] ***********************************************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Install NTP] ********************************************************************************************************************************
ok: [ne4]
ok: [ne3]
ok: [ne1]
ok: [ne2]

TASK [stage01_gpu : List GPGPU drivers] *************************************************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Output GPGPU drivers list] ******************************************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Install NVIDIA driver] **********************************************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Output NVIDIA driver installation result] ***************************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Reboot the system] **************************************************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Wait for system to come back online after reboot] *******************************************************************************************
skipping: [ne1]
skipping: [ne2]
skipping: [ne3]
skipping: [ne4]

TASK [stage01_gpu : Check NVIDIA-SMI] ***************************************************************************************************************************
changed: [ne1]
changed: [ne4]
changed: [ne3]
changed: [ne2]

TASK [stage01_gpu : Extract Driver version] *********************************************************************************************************************
ok: [ne1]
ok: [ne2]
ok: [ne3]
ok: [ne4]

TASK [stage01_gpu : Extract GPU name] ***************************************************************************************************************************
ok: [ne1]
ok: [ne2]
ok: [ne3]
ok: [ne4]

TASK [stage01_gpu : Output GPU Name and Driver Version] *********************************************************************************************************
ok: [ne1] => {
    "msg": "GPU: 0  NVIDIA RTX A5000               Off, NVIDIA Driver Version: 535.146.02"
}
ok: [ne2] => {
    "msg": "GPU: 0  NVIDIA RTX A5000               Off, NVIDIA Driver Version: 535.146.02"
}
ok: [ne3] => {
    "msg": "GPU: 0  NVIDIA RTX A5000               Off, NVIDIA Driver Version: 535.146.02"
}
ok: [ne4] => {
    "msg": "GPU: 0  NVIDIA RTX A5000               Off, NVIDIA Driver Version: 535.146.02"
}

TASK [stage01_gpu : Install nvtop] ******************************************************************************************************************************
ok: [ne4]
ok: [ne1]
ok: [ne3]
ok: [ne2]

TASK [stage02_docker : Update apt cache] ************************************************************************************************************************
ok: [ne4]
ok: [ne3]
ok: [ne1]
ok: [ne2]

TASK [stage02_docker : Install required packages] ***************************************************************************************************************
ok: [ne3] => (item=apt-transport-https)
ok: [ne2] => (item=apt-transport-https)
ok: [ne4] => (item=apt-transport-https)
ok: [ne1] => (item=apt-transport-https)
ok: [ne3] => (item=ca-certificates)
ok: [ne4] => (item=ca-certificates)
ok: [ne2] => (item=ca-certificates)
ok: [ne1] => (item=ca-certificates)
ok: [ne3] => (item=curl)
ok: [ne4] => (item=curl)
ok: [ne2] => (item=curl)
ok: [ne1] => (item=curl)
ok: [ne3] => (item=gnupg-agent)
ok: [ne4] => (item=gnupg-agent)
ok: [ne2] => (item=gnupg-agent)
ok: [ne1] => (item=gnupg-agent)
ok: [ne3] => (item=software-properties-common)
ok: [ne4] => (item=software-properties-common)
ok: [ne1] => (item=software-properties-common)
ok: [ne2] => (item=software-properties-common)

TASK [stage02_docker : Docker | Install repo key] ***************************************************************************************************************
ok: [ne4]
ok: [ne3]
ok: [ne2]
ok: [ne1]

TASK [stage02_docker : Docker | Add repo] ***********************************************************************************************************************
ok: [ne1]
ok: [ne2]
ok: [ne4]
ok: [ne3]

TASK [stage02_docker : Update apt cache after adding Docker repository] *****************************************************************************************
changed: [ne4]
changed: [ne3]
changed: [ne1]
changed: [ne2]

TASK [stage02_docker : Install Docker] **************************************************************************************************************************
ok: [ne2]
ok: [ne1]
ok: [ne4]
ok: [ne3]

TASK [stage02_docker : Enable and start Docker service] *********************************************************************************************************
ok: [ne4]
ok: [ne3]
ok: [ne1]
ok: [ne2]

TASK [stage02_docker : Verify Docker Installation] **************************************************************************************************************
ok: [ne1]
ok: [ne4]
ok: [ne2]
ok: [ne3]

TASK [stage02_docker : Display Docker version] ******************************************************************************************************************
ok: [ne1] => {
    "msg": "Docker version 24.0.7, build afdd53b"
}
ok: [ne2] => {
    "msg": "Docker version 24.0.7, build afdd53b"
}
ok: [ne3] => {
    "msg": "Docker version 24.0.7, build afdd53b"
}
ok: [ne4] => {
    "msg": "Docker version 24.0.7, build afdd53b"
}

TASK [stage02_docker : Check Docker Service Status] *************************************************************************************************************
ok: [ne1]
ok: [ne4]
ok: [ne2]
ok: [ne3]

TASK [stage03_nvidia : Update apt cache] ************************************************************************************************************************
ok: [ne4]
ok: [ne3]
ok: [ne1]
ok: [ne2]

TASK [stage03_nvidia : Add NVIDIA repo gpg key] *****************************************************************************************************************
ok: [ne4]
ok: [ne3]
ok: [ne1]
ok: [ne2]

TASK [stage03_nvidia : Add NVIDIA apt repo] *********************************************************************************************************************
ok: [ne1]
ok: [ne4]
ok: [ne2]
ok: [ne3]

TASK [stage03_nvidia : Update apt cache after adding NVIDIA Docker repository] **********************************************************************************
changed: [ne1]
changed: [ne3]
changed: [ne4]
changed: [ne2]

TASK [stage03_nvidia : Install NVIDIA Container Toolkit] ********************************************************************************************************
ok: [ne1]
ok: [ne4]
ok: [ne3]
ok: [ne2]

TASK [stage03_nvidia : Restart Docker service to apply NVIDIA changes] ******************************************************************************************
changed: [ne1]
changed: [ne3]
changed: [ne4]
changed: [ne2]

TASK [stage03_nvidia : Run a temporary Docker container with NVIDIA GPU support] ********************************************************************************
changed: [ne4]
changed: [ne1]
changed: [ne3]
changed: [ne2]

TASK [stage03_nvidia : Display container nvidia-smi output] *****************************************************************************************************
ok: [ne1] => {
    "msg": {
        "changed": true,
        "container": {
            "Output": "name, memory.total [MiB], driver_version, pci.device_id\nNVIDIA RTX A5000, 24564 MiB, 535.146.02, 0x223110DE\n"
        },
        "failed": false,
        "status": 0
    }
}
ok: [ne2] => {
    "msg": {
        "changed": true,
        "container": {
            "Output": "name, memory.total [MiB], driver_version, pci.device_id\nNVIDIA RTX A5000, 24564 MiB, 535.146.02, 0x223110DE\n"
        },
        "failed": false,
        "status": 0
    }
}
ok: [ne3] => {
    "msg": {
        "changed": true,
        "container": {
            "Output": "name, memory.total [MiB], driver_version, pci.device_id\nNVIDIA RTX A5000, 24564 MiB, 535.146.02, 0x223110DE\n"
        },
        "failed": false,
        "status": 0
    }
}
ok: [ne4] => {
    "msg": {
        "changed": true,
        "container": {
            "Output": "name, memory.total [MiB], driver_version, pci.device_id\nNVIDIA RTX A5000, 24564 MiB, 535.146.02, 0x223110DE\n"
        },
        "failed": false,
        "status": 0
    }
}

TASK [stage03_nvidia : Verify NVIDIA Toolkit Installation] ******************************************************************************************************
ok: [ne4]
ok: [ne1]
ok: [ne3]
ok: [ne2]

TASK [stage03_nvidia : Check NVIDIA Docker Service Status] ******************************************************************************************************
ok: [ne1]
ok: [ne2]
ok: [ne4]
ok: [ne3]

TASK [stage09_test : Run Docker container with GPU support] *****************************************************************************************************
changed: [ne1]
changed: [ne4]
changed: [ne3]
changed: [ne2]

TASK [stage09_test : Wait for container to be ready] ************************************************************************************************************
ok: [ne1]
ok: [ne2]
ok: [ne3]
ok: [ne4]

TASK [stage09_test : Check if API is working] *******************************************************************************************************************
ok: [ne4]
ok: [ne3]
ok: [ne2]
ok: [ne1]

TASK [stage09_test : Display API response] **********************************************************************************************************************
ok: [ne1] => {
    "msg": {
        "changed": false,
        "connection": "close",
        "content": "{\"prediction\":\"Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)\",\"metadata\":{\"version\":\"0.1.1\",\"worker\":\"bfc7204b\",\"model\":\"readerbench/ro-offense\",\"device\":\"cuda\",\"packages\":[\"fastapi                   0.108.0\",\"tokenizers                0.15.0\",\"torch                     2.1.2\",\"transformers              4.36.2\"],\"elapsed_time\":0.0149,\"average_time\":0.0149}}",
        "content_length": "373",
        "content_type": "application/json",
        "cookies": {},
        "cookies_string": "",
        "date": "Fri, 12 Jan 2024 07:25:44 GMT",
        "elapsed": 0,
        "failed": false,
        "json": {
            "metadata": {
                "average_time": 0.0149,
                "device": "cuda",
                "elapsed_time": 0.0149,
                "model": "readerbench/ro-offense",
                "packages": [
                    "fastapi                   0.108.0",
                    "tokenizers                0.15.0",
                    "torch                     2.1.2",
                    "transformers              4.36.2"
                ],
                "version": "0.1.1",
                "worker": "bfc7204b"
            },
            "prediction": "Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)"
        },
        "msg": "OK (373 bytes)",
        "redirected": false,
        "server": "uvicorn",
        "status": 200,
        "url": "http://localhost:5050/predict/"
    }
}
ok: [ne2] => {
    "msg": {
        "changed": false,
        "connection": "close",
        "content": "{\"prediction\":\"Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)\",\"metadata\":{\"version\":\"0.1.1\",\"worker\":\"cc6d5feb\",\"model\":\"readerbench/ro-offense\",\"device\":\"cuda\",\"packages\":[\"fastapi                   0.108.0\",\"tokenizers                0.15.0\",\"torch                     2.1.2\",\"transformers              4.36.2\"],\"elapsed_time\":0.0179,\"average_time\":0.0179}}",
        "content_length": "373",
        "content_type": "application/json",
        "cookies": {},
        "cookies_string": "",
        "date": "Fri, 12 Jan 2024 07:25:43 GMT",
        "elapsed": 0,
        "failed": false,
        "json": {
            "metadata": {
                "average_time": 0.0179,
                "device": "cuda",
                "elapsed_time": 0.0179,
                "model": "readerbench/ro-offense",
                "packages": [
                    "fastapi                   0.108.0",
                    "tokenizers                0.15.0",
                    "torch                     2.1.2",
                    "transformers              4.36.2"
                ],
                "version": "0.1.1",
                "worker": "cc6d5feb"
            },
            "prediction": "Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)"
        },
        "msg": "OK (373 bytes)",
        "redirected": false,
        "server": "uvicorn",
        "status": 200,
        "url": "http://localhost:5050/predict/"
    }
}
ok: [ne3] => {
    "msg": {
        "changed": false,
        "connection": "close",
        "content": "{\"prediction\":\"Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)\",\"metadata\":{\"version\":\"0.1.1\",\"worker\":\"047aa652\",\"model\":\"readerbench/ro-offense\",\"device\":\"cuda\",\"packages\":[\"fastapi                   0.108.0\",\"tokenizers                0.15.0\",\"torch                     2.1.2\",\"transformers              4.36.2\"],\"elapsed_time\":0.0165,\"average_time\":0.0165}}",
        "content_length": "373",
        "content_type": "application/json",
        "cookies": {},
        "cookies_string": "",
        "date": "Fri, 12 Jan 2024 07:25:44 GMT",
        "elapsed": 0,
        "failed": false,
        "json": {
            "metadata": {
                "average_time": 0.0165,
                "device": "cuda",
                "elapsed_time": 0.0165,
                "model": "readerbench/ro-offense",
                "packages": [
                    "fastapi                   0.108.0",
                    "tokenizers                0.15.0",
                    "torch                     2.1.2",
                    "transformers              4.36.2"
                ],
                "version": "0.1.1",
                "worker": "047aa652"
            },
            "prediction": "Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)"
        },
        "msg": "OK (373 bytes)",
        "redirected": false,
        "server": "uvicorn",
        "status": 200,
        "url": "http://localhost:5050/predict/"
    }
}
ok: [ne4] => {
    "msg": {
        "changed": false,
        "connection": "close",
        "content": "{\"prediction\":\"Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)\",\"metadata\":{\"version\":\"0.1.1\",\"worker\":\"d28f714f\",\"model\":\"readerbench/ro-offense\",\"device\":\"cuda\",\"packages\":[\"fastapi                   0.108.0\",\"tokenizers                0.15.0\",\"torch                     2.1.2\",\"transformers              4.36.2\"],\"elapsed_time\":0.0137,\"average_time\":0.0137}}",
        "content_length": "373",
        "content_type": "application/json",
        "cookies": {},
        "cookies_string": "",
        "date": "Fri, 12 Jan 2024 07:25:44 GMT",
        "elapsed": 0,
        "failed": false,
        "json": {
            "metadata": {
                "average_time": 0.0137,
                "device": "cuda",
                "elapsed_time": 0.0137,
                "model": "readerbench/ro-offense",
                "packages": [
                    "fastapi                   0.108.0",
                    "tokenizers                0.15.0",
                    "torch                     2.1.2",
                    "transformers              4.36.2"
                ],
                "version": "0.1.1",
                "worker": "d28f714f"
            },
            "prediction": "Abuz (limbaj ofensiv direct, nivel ridicat de ofensivitate)"
        },
        "msg": "OK (373 bytes)",
        "redirected": false,
        "server": "uvicorn",
        "status": 200,
        "url": "http://localhost:5050/predict/"
    }
}

TASK [stage09_test : Assert that CUDA is used] ******************************************************************************************************************
ok: [ne1] => {
    "changed": false,
    "msg": "CUDA is being used"
}
ok: [ne2] => {
    "changed": false,
    "msg": "CUDA is being used"
}
ok: [ne3] => {
    "changed": false,
    "msg": "CUDA is being used"
}
ok: [ne4] => {
    "changed": false,
    "msg": "CUDA is being used"
}

PLAY [Deploy on Kubernetes Master] ******************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************
ok: [ne5]

TASK [stage02_docker : Update apt cache] ************************************************************************************************************************
ok: [ne5]

TASK [stage02_docker : Install required packages] ***************************************************************************************************************
ok: [ne5] => (item=apt-transport-https)
ok: [ne5] => (item=ca-certificates)
ok: [ne5] => (item=curl)
ok: [ne5] => (item=gnupg-agent)
ok: [ne5] => (item=software-properties-common)

TASK [stage02_docker : Docker | Install repo key] ***************************************************************************************************************
ok: [ne5]

TASK [stage02_docker : Docker | Add repo] ***********************************************************************************************************************
ok: [ne5]

TASK [stage02_docker : Update apt cache after adding Docker repository] *****************************************************************************************
changed: [ne5]

TASK [stage02_docker : Install Docker] **************************************************************************************************************************
ok: [ne5]

TASK [stage02_docker : Enable and start Docker service] *********************************************************************************************************
ok: [ne5]

TASK [stage02_docker : Verify Docker Installation] **************************************************************************************************************
ok: [ne5]

TASK [stage02_docker : Display Docker version] ******************************************************************************************************************
ok: [ne5] => {
    "msg": "Docker version 24.0.7, build afdd53b"
}

TASK [stage02_docker : Check Docker Service Status] *************************************************************************************************************
ok: [ne5]

PLAY RECAP ******************************************************************************************************************************************************
ne1                        : ok=33   changed=7    unreachable=0    failed=0    skipped=10   rescued=0    ignored=0   
ne2                        : ok=33   changed=7    unreachable=0    failed=0    skipped=10   rescued=0    ignored=0   
ne3                        : ok=33   changed=7    unreachable=0    failed=0    skipped=10   rescued=0    ignored=0   
ne4                        : ok=33   changed=7    unreachable=0    failed=0    skipped=10   rescued=0    ignored=0   
ne5                        : ok=11   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```