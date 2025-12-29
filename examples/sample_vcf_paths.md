# Example VCF paths and expected format

This document provides example Google Cloud Storage paths and file requirements
for running the partitioned PRS pipeline in this repository.

No genomic data are included.

---

## Required input files

The pipeline expects a **bgzipped VCF** and a corresponding **Tabix index**:

- Variant file: `.vcf.gz`
- Index file: `.vcf.gz.tbi`

Both files must be accessible from Google Cloud Storage.

---

## Example Cloud Storage layout

Below is an example directory structure in a GCS bucket:

```text
gs://sample_vcf1/
├── input/
│   ├── t2dp_suzuki_synthetic.vcf.gz
│   └── t2dp_suzuki_synthetic.vcf.gz.tbi
│
└── prsedm_output/
    └── synthetic_results.csv
