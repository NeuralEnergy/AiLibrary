"""

Unit tester for the Neural Energy AiLibrary GCP model endpoint.

@module: TEST 2
@author: DIGITIZE TECH SRL
@description: 
  This test sends multiple POST requests to the GCP model endpoint and 
  collects unique signatures. The collected signatures are displayed at the 
  end of the test.
  
@example run:

```bash

  # RUN 1
  
  root@3d212eb79e72:/workspaces/501_NeuralEnergy/tests# python test2.py 
  test_burst_requests (__main__.TestGCPModelEndpoint)
  Test the GCP model endpoint with burst requests. ... 
  Unique Signatures Collected:
  [
      "test_model_b:TestModelBWorker:0",
      "test_model_b:TestModelBWorker:1"
  ]

  Unique dummy predicts outputs collected:
  [
      "5495*1 + 2 = 5497 PREDICTED",
      "4500*1 + 2 = 4502 PREDICTED",
      "6501*1 + 2 = 6503 PREDICTED",
      "3968*1 + 2 = 3970 PREDICTED",
      "4299*1 + 2 = 4301 PREDICTED",
      "7111*1 + 2 = 7113 PREDICTED",
      "9851*1 + 2 = 9853 PREDICTED",
      "6770*1 + 2 = 6772 PREDICTED",
      "6844*1 + 2 = 6846 PREDICTED",
      "2588*1 + 2 = 2590 PREDICTED"
  ]
  ok

  ----------------------------------------------------------------------
  Ran 1 test in 2.571s

  OK
  
  # RUN 2

  root@3d212eb79e72:/workspaces/501_NeuralEnergy/tests# python test2.py 
  test_burst_requests (__main__.TestGCPModelEndpoint)
  Test the GCP model endpoint with burst requests. ... 
  Unique Signatures Collected:
  [
      "h21b4.test_model_b.TestModelBWorker.0",
      "h21b4.test_model_b.TestModelBWorker.1"
  ]

  Unique dummy predicts outputs collected:
  [
      "1360*1 + 2 = 1362 PREDICTED",
      "8558*1 + 2 = 8560 PREDICTED",
      "8198*1 + 2 = 8200 PREDICTED",
      "341*1 + 2 = 343 PREDICTED",
      "8060*1 + 2 = 8062 PREDICTED",
      "4494*1 + 2 = 4496 PREDICTED",
      "2765*1 + 2 = 2767 PREDICTED",
      "5620*1 + 2 = 5622 PREDICTED",
      "4537*1 + 2 = 4539 PREDICTED",
      "7759*1 + 2 = 7761 PREDICTED"
  ]
  ok

  ----------------------------------------------------------------------
  Ran 1 test in 2.617s

  OK  
```

"""

import requests
import unittest
import json
import numpy as np

from collections import defaultdict

class TestGCPModelEndpoint(unittest.TestCase):
    """
    Test class for GCP model endpoint.

    Attributes
    ----------
    url : str
        The URL of the GCP endpoint.
    unique_signatures : set
        A set to store unique signature values from the responses.

    Methods
    -------
    test_burst_requests()
        Tests the GCP model endpoint by sending multiple POST requests and collecting unique signatures.
    """

    def setUp(self):
        """Set up test parameters."""
        self.url = "https://ne-ailib-service-zyqocudmla-uc.a.run.app/run"
        self.unique_signatures = defaultdict(int)
        self.unique_dummy_predicts = defaultdict(int)

    def test_burst_requests(self):
        """
        Test the GCP model endpoint with burst requests.

        Sends multiple POST requests and collects unique 'signature' values from the responses.
        """
        for _ in range(10):  # Example of 10 burst requests
            # Define the payload
            payload = {
              "SIGNATURE": "test_model_b",
              "INPUT_VALUE": np.random.randint(0, 10_000),
              "WEIGHT": np.random.randint(0, 1_000),
              "BIAS": np.random.randint(0, 100),
            }

            # Send POST request
            response = requests.post(self.url, json=payload)
            self.assertEqual(response.status_code, 200)

            # Parse response JSON and collect unique signatures
            response_json = response.json()
            if 'signature' in response_json:
                self.unique_signatures[response_json['signature']] += 1
            if 'predict_result' in response_json:
                self.unique_dummy_predicts[response_json['predict_result'].get('dummy_model_predict')] += 1
            

    def tearDown(self):
        """Display unique signatures after the test finishes."""
        print("\nUnique Signatures Collected:\n{}".format(
          json.dumps(self.unique_signatures, indent=4)
          )
        )
        print("\nUnique dummy predicts outputs collected:\n{}".format(
          json.dumps(self.unique_dummy_predicts, indent=4)
          )
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
