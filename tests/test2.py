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
        self.unique_signatures = set()
        self.unique_dummy_predicts = set()

    def test_burst_requests(self):
        """
        Test the GCP model endpoint with burst requests.

        Sends multiple POST requests and collects unique 'signature' values from the responses.
        """
        for _ in range(10):  # Example of 10 burst requests
            # Define the payload
            payload = {
              "SIGNATURE": "test_model_b",
              "INPUT_VALUE": np.random.randint(0, 10_000)
            }

            # Send POST request
            response = requests.post(self.url, json=payload)
            self.assertEqual(response.status_code, 200)

            # Parse response JSON and collect unique signatures
            response_json = response.json()
            if 'signature' in response_json:
                self.unique_signatures.add(response_json['signature'])
            if 'predict_result' in response_json:
                self.unique_dummy_predicts.add(response_json['predict_result'].get('dummy_model_predict'))
            

    def tearDown(self):
        """Display unique signatures after the test finishes."""
        print("\nUnique Signatures Collected:\n{}".format(
          json.dumps(list(self.unique_signatures), indent=4)
          )
        )
        print("\nUnique dummy predicts outputs collected:\n{}".format(
          json.dumps(list(self.unique_dummy_predicts), indent=4)
          )
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)