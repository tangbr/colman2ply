#!/bin/bash

# Feature Extraction
colmap feature_extractor \
  --database_path /app/output/database.db \
  --image_path /app/output/images \
  --SiftExtraction.max_num_features 20000

# Feature Matching
colmap exhaustive_matcher \
  --database_path /app/output/database.db

# Sparse Reconstruction (Mapping)
colmap mapper \
  --database_path /app/output/database.db \
  --image_path /app/output/images \
  --output_path /app/output/sparse
