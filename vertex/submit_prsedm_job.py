from google.cloud import aiplatform
import os

# ==== CONFIGURABLE SETTINGS ====

PROJECT_ID = "melodic-agent-478708-d2"
REGION = "us-central1"
STAGING_BUCKET = f"gs://{PROJECT_ID}-vertex-staging"

IMAGE_URI = "us-central1-docker.pkg.dev/melodic-agent-478708-d2/prs-demo-repo/prsedm:v2"


# ---- Synthetic VCF you uploaded ----
VCF_PATH = "gs://sample_vcf1/input/t2dp_suzuki_synthetic.vcf.gz"

# ---- Output PRS file ----  
OUTPUT_PATH = "gs://sample_vcf1/prsedm_output/synthetic_results.csv"

# ---- PRSedm score flag ----
PRS_SCORE = "t2dp-suzuki24-ma"

# ---- Performance / parallelism (optional) ----
PARALLEL = True        # set True to enable --parallel
NTASKS = 4             # number of tasks for PRSedm --ntasks (match machine vCPUs ideally)
MACHINE_TYPE = "n1-standard-8"  # choose bigger machine if using imputation/parallel

# ====================================

def build_args():
    args = [
        "--gcs_vcf", VCF_PATH,
        "--gcs_out", OUTPUT_PATH,
        "--scores", PRS_SCORE
    ]
    if PARALLEL:
        args.append("--parallel")
    if NTASKS:
        args += ["--ntasks", str(NTASKS)]
    return args

def main():
    print("Initializing Vertex AI…")
    aiplatform.init(
        project=PROJECT_ID,
        location=REGION,
        staging_bucket=STAGING_BUCKET
    )

    container_spec = {
        "image_uri": IMAGE_URI,
        "args": build_args()
    }

    worker_pool_specs = [
        {
            "machine_spec": {"machine_type": MACHINE_TYPE},
            "replica_count": 1,
            "container_spec": container_spec
        }
    ]

    job = aiplatform.CustomJob(
        display_name="prsedm-synthetic-impute-demo",
        worker_pool_specs=worker_pool_specs
    )

    print("Submitting PRSedm job to Vertex AI…")
    job.run(sync=True)

    print("\n🎉 Job completed (or errored).")
    print("Check results at:", OUTPUT_PATH)

if __name__ == "__main__":
    main()