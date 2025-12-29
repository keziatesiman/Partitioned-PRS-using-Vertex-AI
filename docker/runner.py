# runner.py (patched to download .tbi index and optional ref index)
import argparse, subprocess, os, sys
from google.cloud import storage

parser = argparse.ArgumentParser()
parser.add_argument("--gcs_vcf", required=True, help="gs://.../file.vcf.gz")
parser.add_argument("--gcs_out", required=True, help="gs://.../out.csv")
parser.add_argument("--scores", required=True, help="comma-separated PRS flags")
# optional passthroughs
parser.add_argument("--col", default="GT", help="genotype column (GT or GP)")
parser.add_argument("--impute", action="store_true", help="enable imputation (requires --refvcf)")
parser.add_argument("--refvcf", default=None, help="gs://.../ref.vcf.gz")
parser.add_argument("--parallel", action="store_true", help="enable parallel")
parser.add_argument("--ntasks", type=int, default=None, help="ntasks for parallel")
parser.add_argument("--batch_size", type=int, default=None, help="variant batch size")
parser.add_argument("--norm", action="store_true", help="perform MinMax normalization")
args = parser.parse_args()

LOCAL_VCF = "/data/input.vcf.gz"
LOCAL_OUT = "/output/results.csv"
LOCAL_REF = "/data/ref.vcf.gz"

def download_from_gcs(gcs_path, local_path):
    client = storage.Client()
    bucket_name = gcs_path.split('/')[2]
    blob_path = '/'.join(gcs_path.split('/')[3:])
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    print(f"[runner] Downloading {gcs_path} -> {local_path}")
    blob.download_to_filename(local_path)

def upload_to_gcs(local_path, gcs_path):
    client = storage.Client()
    bucket_name = gcs_path.split('/')[2]
    blob_path = '/'.join(gcs_path.split('/')[3:])
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)
    print(f"[runner] Uploading {local_path} -> {gcs_path}")
    blob.upload_from_filename(local_path)

def try_download_index(gcs_vcf_path, local_vcf_path):
    # try to download .tbi index adjacent to the vcf path
    idx_gcs = gcs_vcf_path + ".tbi"
    local_idx = local_vcf_path + ".tbi"
    try:
        download_from_gcs(idx_gcs, local_idx)
        print(f"[runner] Downloaded index: {idx_gcs}")
    except Exception as e:
        print(f"[runner] WARNING: failed to download index {idx_gcs}: {e}")

def run_prsedm(vcf_local, out_local):
    cmd = ["prsedm","--vcf", vcf_local, "--scores", args.scores, "--output", out_local, "--col", args.col]
    if args.impute:
        cmd += ["--impute"]
        if args.refvcf:
            cmd += ["--refvcf", LOCAL_REF]
    if args.parallel:
        cmd += ["--parallel"]
    if args.ntasks:
        cmd += ["--ntasks", str(args.ntasks)]
    if args.batch_size:
        cmd += ["--batch-size", str(args.batch_size)]
    if args.norm:
        cmd += ["--norm"]
    print("[runner] Running command:", " ".join(cmd))
    subprocess.check_call(cmd)

if __name__ == "__main__":
    # download vcf
    download_from_gcs(args.gcs_vcf, LOCAL_VCF)

    # attempt to download .tbi index next to the VCF
    try_download_index(args.gcs_vcf, LOCAL_VCF)

    # optional ref vcf + index
    if args.refvcf:
        download_from_gcs(args.refvcf, LOCAL_REF)
        try:
            download_from_gcs(args.refvcf + ".tbi", LOCAL_REF + ".tbi")
            print("[runner] Ref index downloaded.")
        except Exception as e:
            print("[runner] WARNING: ref index download failed:", e)

    # final run
    try:
        run_prsedm(LOCAL_VCF, LOCAL_OUT)
    except subprocess.CalledProcessError as e:
        print("[runner] ERROR: prsedm failed with exit code", e.returncode, file=sys.stderr)
        raise
    upload_to_gcs(LOCAL_OUT, args.gcs_out)
    print("[runner] Done.")
