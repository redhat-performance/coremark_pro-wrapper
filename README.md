# CoreMark-PRO Benchmark Wrapper

## Description

This wrapper facilitates the automated execution of the EEMBC CoreMark-PRO benchmark. CoreMark-PRO is a comprehensive, advanced processor benchmark that tests the entire processor with multicore support, a combination of integer and floating-point workloads, and data sets for utilizing larger memory subsystems. It measures performance across nine distinct workloads and produces multi-core, single-core, and scaling metrics.

The wrapper provides:
- Automated CoreMark-PRO download, build, and execution.
- Automatic CPU core detection and multi-core execution.
- Configurable workload iteration tuning for single-core and multi-core runs.
- Support for specifying a particular CoreMark-PRO version or commit.
- Result collection, processing, and verification.
- CSV and JSON output formats.
- System configuration metadata capture.
- Integration with test_tools framework.
- Optional Performance Co-Pilot (PCP) integration.

## Command-Line Options

```
CoreMark-PRO Options:
  --commit <n>: Commit or tag to use from coremark-pro repository.
      If not designated, will use tag v1.1.2743.
  --no-overrides: If present, skip workload iteration tuning.
      By default, the script modifies iteration counts in workload .opt files
      for optimized single-core and multi-core execution.
  --test_iterations <n>: Number of times to run the full test suite.
      Overrides --iterations if both are specified.

General test_tools options:
  --home_parent <value>: Parent home directory. If not set, defaults to current working directory.
  --host_config <value>: Host configuration name, defaults to current hostname.
  --iterations <value>: Number of times to run the test, defaults to 1.
  --run_user: User that is actually running the test on the test system. Defaults to current user.
  --sys_type: Type of system working with (aws, azure, hostname). Defaults to hostname.
  --sysname: Name of the system running, used in determining config files. Defaults to hostname.
  --tuned_setting: Used in naming the results directory. For RHEL, defaults to current active tuned profile.
      For non-RHEL systems, defaults to 'none'.
  --use_pcp: Enable Performance Co-Pilot monitoring during test execution.
  --tools_git <value>: Git repo to retrieve the required tools from.
      Default: https://github.com/redhat-performance/test_tools-wrappers
  --usage: Display this usage message.
```

## What the Script Does

The `coremark_pro_run` script performs the following workflow:

1. **Environment Setup**:
   - Clones the test_tools-wrappers repository if not present (default: ~/test_tools).
   - Acquisition is attempted via wget, then curl, then git clone.
   - Sources error codes and general setup utilities.
   - Gathers hardware information using the `gather_data` tool.

2. **Package Installation**:
   - Installs required dependencies via package_tool (gcc, make, bc, git).
   - Dependencies are defined in coremark_pro-packages.json for different OS variants (RHEL, Ubuntu, SLES, Amazon Linux).

3. **CoreMark-PRO Download**:
   - Clones the coremark-pro repository from https://github.com/eembc/coremark-pro.
   - By default, uses tag v1.1.2743 (shallow clone for faster download).
   - If `--commit` is specified, clones the full repo and checks out the specified commit.

4. **Workload Tuning** (unless `--no-overrides` is specified):
   - Modifies iteration counts in workload `.opt` files for optimized execution.
   - Each workload has separate iteration counts for single-core and multi-core modes:
     - cjpeg-rose7-preset: 2,000 / 50,000
     - core: 1,000 / 1,000
     - linear_alg-mid-100x100-sp: 3,000 / 100,000
     - loops-all-mid-10k-sp: 1,000 / 2,000
     - nnet_test: 1,000 / 3,000
     - parser-125k: 1,000 / 1,000
     - radix2-big-64k: 10,000 / 200,000
     - sha-test: 3,000 / 100,000
     - zip-test: 2,000 / 40,000
   - Original `.opt` files are preserved with an `_old` suffix.

5. **Build**:
   - Compiles CoreMark-PRO with `make TARGET=linux64 build`.
   - If the build fails silently, it reruns without suppressing output for debugging.

6. **Test Execution**:
   - Detects number of CPU cores from `/proc/cpuinfo`.
   - Runs `make TARGET=linux64 XCMD=-c<numb_cpus> certify-all` for each iteration.
   - Each iteration's output is saved to `coremark_pro_run_<N>` (zero-padded for 10+ iterations).
   - Captures start and end timestamps for each run.
   - Optionally records PCP performance data per iteration.

7. **Data Collection**:
   - Captures system configuration via `gather_data` (CPU, memory, kernel version).
   - Records timestamps for test run start and end.
   - Optionally records PCP performance data for both single-core and multi-core metrics.

8. **Result Processing**:
   - Aggregates results across all iterations by averaging per-workload metrics.
   - Produces a summary report with averaged multi-core, single-core, and scaling values.
   - Generates CSV file with configuration and performance data.
   - Calculates overall CoreMark-PRO Score from the summary.
   - Creates JSON output via `csv_to_json`.

9. **Verification**:
   - Validates results against Pydantic schema (results_schema.py).
   - Ensures all required fields are present, positive, and non-NaN/infinite.
   - Uses `verify_results` from test_tools.

10. **Output**:
    - Saves all raw output files, processed CSV/JSON, and system metadata.
    - Archives results to configured storage location via `save_results`.
    - Optionally includes PCP performance data in the archive.

## Dependencies

Location of underlying workload: https://github.com/eembc/coremark-pro

**Packages required by distribution**:
- **RHEL**: bc, gcc, git, make
- **Ubuntu**: bc, gcc, git, make
- **SLES**: bc, gcc, git, make
- **Amazon Linux**: bc, gcc, git, perl-Data-Dumper, make

To run:
```bash
git clone https://github.com/redhat-performance/coremark_pro-wrapper
cd coremark_pro-wrapper/coremark_pro
./coremark_pro_run
```

The script will automatically detect the number of CPU cores and configure execution accordingly.

## The CoreMark-PRO Benchmark

CoreMark-PRO is a comprehensive processor benchmark developed by EEMBC that extends the original CoreMark benchmark with support for multicore technology, floating-point workloads, and larger memory subsystems.

### Workloads

CoreMark-PRO executes nine distinct workloads covering a range of computational domains:

| Workload | Domain |
|----------|--------|
| cjpeg-rose7-preset | Image compression (JPEG encoding) |
| core | CPU core operations |
| linear_alg-mid-100x100-sp | Linear algebra (single-precision) |
| loops-all-mid-10k-sp | Loop performance (single-precision) |
| nnet_test | Neural network inference |
| parser-125k | Text parsing/tokenization |
| radix2-big-64k | Radix-2 sorting |
| sha-test | Cryptographic hashing (SHA) |
| zip-test | Data compression |

### Metrics

For each workload, CoreMark-PRO reports:
- **Multi-core iterations**: Performance with all CPU cores active.
- **Single-core iterations**: Performance on a single core.
- **Scaling**: The ratio of multi-core to single-core performance, indicating how well the workload parallelizes.

The overall **CoreMark-PRO Score** is the aggregate of all workload results.

## Output Files

The results directory contains:

- **results_coremark_pro.csv**: CSV file with per-workload metrics (Test, Multi_iterations, Single_iterations, Scaling, Start_Date, End_Date) and overall Score.
- **results_coremark_pro.json**: JSON representation of the CSV data.
- **coremark_pro.summary**: Human-readable summary report with averaged metrics across iterations.
- **coremark_pro_run_\<N\>**: Raw output files from each iteration.
- **test_results_report**: System and test metadata.
- **PCP data** (if --use_pcp option used): Performance Co-Pilot monitoring data in `/tmp/pcp_coremark-pro_<TIMESTAMP>/`.

## Examples

### Basic run with defaults
```bash
./coremark_pro_run
```
This runs with:
- CoreMark-PRO tag v1.1.2743
- Workload iteration tuning enabled
- 1 iteration
- Automatic CPU core detection

### Run multiple iterations
```bash
./coremark_pro_run --iterations 3
```
Runs the full benchmark suite 3 times and averages results.

### Use a specific CoreMark-PRO version
```bash
./coremark_pro_run --commit v1.2.0
```
Clones the full repository and checks out the specified commit or tag.

### Skip workload tuning
```bash
./coremark_pro_run --no-overrides
```
Uses the original upstream iteration counts without modification.

### Run with PCP monitoring
```bash
./coremark_pro_run --use_pcp
```
Collects Performance Co-Pilot data during the run.

### Combination example
```bash
./coremark_pro_run --iterations 5 --use_pcp --commit v1.1.2743
```
Runs 5 iterations with PCP monitoring using a specific CoreMark-PRO version.

## How Workload Tuning Works

By default, the wrapper modifies the iteration counts in each workload's `.opt` file to optimize benchmark execution. The first value is used for single-core runs and the second for multi-core runs. Multi-core runs typically use higher iteration counts to ensure meaningful measurement across all cores.

This tuning can be disabled with the `--no-overrides` flag, which preserves the original upstream iteration counts.

Original `.opt` files are backed up with an `_old` suffix to allow restoration.

## Return Codes

The script uses standardized error codes from test_tools error_codes:
- **0**: Success
- **101**: Failed to acquire test_tools-wrappers via wget, curl, or git clone
- **E_GENERAL**: General execution errors (package installation failure, clone failure, build failure, test execution failure, invalid options).
- **E_USAGE**: Usage/help display requested

Exit codes indicate specific failure points for automated testing workflows.

## Notes

### Architecture Support
- Hardcoded for 64-bit Linux (`TARGET=linux64`).
- CPU core count is auto-detected from `/proc/cpuinfo`.
- Works on any Linux system with GCC and make available.

### Iteration Count Tuning
- Multi-core workloads use higher iteration counts by default for more accurate measurement.
- Single-core workloads use lower iteration counts to reduce overall test time.
- Use `--no-overrides` to run with upstream defaults.

### Performance Tips
- Run multiple iterations to verify consistency.
- Ensure system is idle (no other workloads) for best results.
- Disable CPU frequency scaling (use performance governor) for reproducible results.
- Consider the active tuned profile on RHEL systems.

### Troubleshooting
- If the build fails, verify that gcc and make are installed.
- If test_tools acquisition fails (exit code 101), check network connectivity.
- If performance is unexpectedly low, check CPU frequency and system load.
- Use `--use_pcp` to collect detailed performance counters for analysis.
