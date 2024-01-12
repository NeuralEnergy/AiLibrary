"""

Unit tester for the Neural Energy AiLibrary GCP model endpoint.

@module: TEST 1
@author: DIGITIZE TECH SRL
@description: 
  This test sends a POST request to the GCP model endpoint and verifies the response.

@example run:

```bash
root@3d212eb79e72:/workspaces/501_NeuralEnergy/tests# python test1.py 
test_model_endpoint (__main__.TestGCPModelEndpoint)
Test the GCP model endpoint. ... ok

----------------------------------------------------------------------
Ran 1 test in 0.250s

OK
```

"""

import requests
import unittest
import json
import numpy as np

class TestGCPModelEndpoint(unittest.TestCase):
    """
    Test class for GCP model endpoint.

    Attributes
    ----------
    url : str
        The URL of the GCP endpoint.

    Methods
    -------
    test_model_endpoint()
        Tests the GCP model endpoint by sending a POST request and verifying the response.
    """

    def setUp(self):
        """Set up test parameters."""
        self.url = "https://ne-ailib-service-zyqocudmla-uc.a.run.app/run"

    def test_model_endpoint(self):
        """
        Test the GCP model endpoint.

        Sends a POST request with a specific JSON payload and checks whether the response
        matches the expected format and contains expected fields.
        """

        # Define the payload
        payload = {
            "SIGNATURE": "test_model_b",
            "INPUT_VALUE": np.random.randint(0, 10_000)
        }

        # Send POST request
        response = requests.post(self.url, json=payload)

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Parse response JSON
        response_json = response.json()

        # Validate the structure and content of the response
        self.assertIn('call_id', response_json)
        self.assertIn('gw-uptime', response_json)
        self.assertIn('hostname', response_json)
        self.assertIn('predict_result', response_json)
        self.assertIn('signature', response_json)
        self.assertIn('time', response_json)
        self.assertIn('ver-app', response_json)
        self.assertIn('ver-lib', response_json)
        self.assertIn('worker_id', response_json)

        # Check specific fields if necessary
        # Example: self.assertEqual(response_json['predict_result']['dummy_model_predict'], "100*1 + 2 = 102 PREDICTED")

if __name__ == '__main__':
    unittest.main(verbosity=2)
