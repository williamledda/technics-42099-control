#!/bin/bash

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. technics-42099.proto