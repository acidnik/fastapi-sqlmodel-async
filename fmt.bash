#!/bin/bash

black . --line-length 120 --skip-string-normalization
isort . --force-single-line-imports
