# Running Partitioned Polygenic Risk Scores on Google Vertex AI using PRSedm

This repository demonstrates how to run **partitioned polygenic risk scores (PRS)** at scale using **PRSedm** on **Google Cloud Vertex AI**.

Unlike conventional PRS pipelines that output a single aggregate score, **partitioned PRS decomposes genetic risk into biologically meaningful components**, enabling interpretation at the level of pathways and mechanisms. This tutorial shows how to operationalize such analyses in a cloud-native, reproducible way.

---

## Why Partitioned PRS?

Most common diseases, including Type 2 Diabetes (T2D), are highly polygenic. Thousands of genetic variants contribute small effects that, when aggregated, influence disease risk.

A standard PRS answers:

> *How high is an individual’s genetic risk?*

A **partitioned PRS** goes further:

> *Why is the risk high? Which biological processes contribute most?*

For T2D, partitioned PRS can attribute risk across components such as:

* beta-cell function and insulin secretion
* obesity and adiposity
* liver and lipid metabolism
* metabolic syndrome
* residual glycaemic mechanisms

This makes partitioned PRS particularly valuable for:

* mechanistic understanding of disease
* personalized prevention strategies
* moving PRS closer to clinical interpretability

---

## What This Repository Provides

By the end of this tutorial, you will have:

* A **Dockerized PRSedm runner** suitable for cloud execution
* A **Vertex AI CustomJob** that scores a VCF stored in Google Cloud Storage
* A **CSV output** containing partitioned PRS per individual
* Example **visualizations** showing:

  * pathway-level PRS decomposition
  * population-level PRS distribution

The pipeline is intentionally modular so that components can be reused in production or research environments.

---

## High-Level Architecture

1. A bgzipped, indexed VCF is stored in Google Cloud Storage
2. A custom Docker container runs PRSedm
3. Vertex AI launches the container as a CustomJob
4. PRSedm computes partitioned PRS
5. Results are written back to Cloud Storage as a CSV

This approach avoids local compute constraints and scales cleanly to larger cohorts.

---

## Repository Structure

```text
partitioned-prs-vertexai/
│
├── README.md
├── notebooks/
│   └── 01_partitioned_prs_vertexai.ipynb
│
├── docker/
│   ├── Dockerfile
│   └── runner.py
│
├── vertex/
│   └── submit_prsedm_job.py
│
├── examples/
│   └── sample_vcf_paths.md
│
└── LICENSE
```

* **`docker/`** contains the minimal PRSedm execution environment
* **`vertex/`** contains the Vertex AI job submission script
* **`notebooks/`** contains the end-to-end walkthrough and visualization examples

---

## Prerequisites

Before running this pipeline, you will need:

* A Google Cloud project with billing enabled
* `gcloud` CLI configured
* Vertex AI API enabled
* A bgzipped VCF (`.vcf.gz`) with a Tabix index (`.tbi`) stored in GCS
* Basic familiarity with VCFs, GWAS, and PRS concepts

No real genomic data is included in this repository.

---

## Core Components

### PRSedm Docker Runner

The Docker image:

* downloads a VCF (and index) from Cloud Storage
* runs PRSedm with user-specified score sets
* uploads the resulting CSV back to Cloud Storage

This design allows PRSedm to run identically across local, cloud, and CI environments.

---

### Vertex AI CustomJob

Vertex AI is used to:

* provision compute resources
* execute the container
* manage logs and failures

The job configuration allows control over:

* machine type
* parallelization inside PRSedm
* score selection

This makes the pipeline suitable for both demos and large-scale analyses.

---

## Running the Pipeline

Once configured, the pipeline can be launched with a single command:

```bash
python vertex/submit_prsedm_job.py
```

Vertex AI will:

* start the custom job
* download the input VCF
* compute partitioned PRS
* write results back to Cloud Storage

---

## Interpreting the Output

The PRSedm output CSV contains:

* one row per individual
* partition-level PRS components
* the total PRS

The provided notebook demonstrates:

* radar (spider) plots for pathway-level interpretation
* population-level PRS distributions with individual overlays

This layer is critical for translating PRS results into biologically meaningful insights.

---

## Extensions and Variations

Possible extensions include:

* enabling genotype imputation with a reference VCF
* swapping PRSedm score definitions
* ancestry-specific PRS evaluation
* cohort-scale execution using larger machine types

The pipeline is intentionally minimal to make these extensions straightforward.

---

## Disclaimer

This repository is intended for **research and educational purposes only**.
It is **not** a clinical diagnostic tool.

---

## Acknowledgements

This tutorial uses the open-source **PRSedm** framework.
All scientific credit for score construction belongs to the original PRSedm authors and underlying GWAS consortia.
