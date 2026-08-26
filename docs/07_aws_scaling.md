# AWS Scaling Plan

## Goal

Run large Perturb-seq benchmarks reproducibly and cost-effectively.

The local pipeline should run on a laptop for demo data. Full datasets should run through AWS Batch when memory or runtime becomes limiting.

## Recommended Architecture

```text
S3 raw data bucket
        |
        v
Nextflow pipeline
        |
        v
AWS Batch compute environment
        |
        v
S3 results bucket
        |
        v
HTML/Markdown benchmark report
```

## AWS Services

| Service | Use |
|---|---|
| S3 | store raw datasets, processed AnnData files, reports, logs |
| AWS Batch | run method jobs in parallel |
| EC2 Spot | reduce compute cost for large datasets |
| ECR | store container images |
| CloudWatch Logs | monitor failed jobs and memory pressure |
| IAM | least-privilege access to S3, Batch, ECR |

## Cost Strategy

- Start with processed public objects instead of raw FASTQ.
- Use small demo data for CI.
- Use dataset shards for development.
- Cache standardized AnnData files.
- Run expensive methods only after baseline QC passes.
- Use Spot instances for scalable method jobs.
- Store reports and summary tables long term; archive large intermediates.

## Nextflow Profiles

Planned profiles:

- `local`: laptop or workstation
- `docker`: local containerized run
- `awsbatch`: AWS Batch execution

## Outputs

Each run writes:

- standardized AnnData object
- dataset QC table
- method result tables
- biological interpretation tables
- benchmark metrics
- runtime and memory summary
- final HTML or Markdown report

## Practical Compute Notes

SCEPTRE and genome-scale datasets can be compute-heavy. The workflow should allow:

- perturbation subsets
- gene subsets
- chromosome or pathway-focused runs
- downsampling benchmarks
- parallel jobs by dataset, method, perturbation, or gene block

The goal is not to make every method cheap. The goal is to show when a method is worth its compute cost.

