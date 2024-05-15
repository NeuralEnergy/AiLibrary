"""
Torch version:  2.1.2
MPS is available.
Running benchmark...
Loading CPU model...
Downloading: "https://download.pytorch.org/models/mobilenet_v3_large-5c1a4163.pth" to /Users/andreidamian/.cache/torch/hub/checkpoints/mobilenet_v3_large-5c1a4163.pth
100.0%
Loading MPS model...
Loading data...
Current folder:  /Users/andreidamian/work/AiLibrary
Warming iteration 1
Warming iteration 2
Warming iteration 3
Warming iteration 4
Running iteration 0
Running iteration 10
Running iteration 20
Running iteration 30
Running iteration 40
Average CPU Inference Time: 0.2413 seconds
Average MPS Inference Time: 0.0233 seconds  
"""

import os
import torch as th
import torchvision as tv
import json

import time
import numpy as np

if __name__ == '__main__':
  print('Torch version: ', th.__version__)

  if not th.backends.mps.is_available():
    if not th.backends.mps.is_built():
      print("MPS not available because the current PyTorch install was not "
            "built with MPS enabled.")
    else:
      print("MPS not available because the current MacOS version is not 12.3+ "
            "and/or you do not have an MPS-enabled device on this machine.")
  else:
    print("MPS is available.")
    dev = th.device('mps')
    print("Running benchmark...")
    
    weights = tv.models.MobileNet_V3_Large_Weights.DEFAULT
    labels = weights.meta['categories']

    print("Loading CPU model...")
    model_cpu = tv.models.mobilenet_v3_large(
      weights=weights
    )
    print("Loading MPS model...")
    model_mps = tv.models.mobilenet_v3_large(
      weights=weights
    )
    model_mps = model_mps.to(dev)  # Apply 'to(dev)' to MPS model

    model_cpu.eval()
    model_mps.eval()

    print("Loading data...")
    print("Current folder: ", os.getcwd())
    FILES = [
      './apple_mps/img/img1.jpeg',
      './apple_mps/img/img2.jpeg',
      './apple_mps/img/img3.jpeg',
    ]
    imgs = [tv.io.read_image(f) / 255. for f in FILES]

    num_iterations = 20  # You can adjust the number of iterations as needed

    # Warm-up models
    for i in range(1, 5):
      print("Warming iteration {}".format(i), flush=True)
      with th.no_grad():
        model_mps(imgs[0].unsqueeze(0).to(dev))
        model_cpu(imgs[0].unsqueeze(0))

    cpu_timings = []
    mps_timings = []
    
    results = {}

    for i in range(num_iterations):
      img_id = i % len(imgs)
      if i % 10 == 0:
        print("Running iteration {}".format(i), flush=True)
      with th.no_grad():
        # CPU Inference
        start_time = time.time()
        result_cpu = model_cpu(imgs[img_id].unsqueeze(0))
        end_time = time.time()
        cpu_timings.append(end_time - start_time)

        # MPS Inference
        start_time = time.time()
        th_img_mps = imgs[img_id].to(dev)  # Apply 'to(dev)' only at forward time
        result_mps = model_mps(th_img_mps.unsqueeze(0))
        end_time = time.time()
        mps_timings.append(end_time - start_time)
        
        
        results['image_{}'.format(img_id)] = {
          'cpu': labels[result_cpu.argmax(-1).item()],
          'mps': labels[result_mps.argmax(-1).item()]
        }

    print("Results: ", json.dumps(results, indent=2))
  
    # Calculate averages using NumPy
    cpu_avg_time = np.mean(cpu_timings)
    mps_avg_time = np.mean(mps_timings)

    print(f"Average CPU Inference Time: {cpu_avg_time:.4f} seconds")
    print(f"Average MPS Inference Time: {mps_avg_time:.4f} seconds")
