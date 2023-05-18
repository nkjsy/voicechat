#!/bin/bash
sudo apt-get update
sudo apt-get install libssl-dev libasound2
uvicorn app:app --host 0.0.0.0 --port 80