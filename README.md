Automation wrapper for coremark_pro

Description: CoreMark®-PRO is a comprehensive, advanced processor benchmark that
    works with and enhances the market-proven industry-standard EEMBC CoreMark®
    benchmark. While CoreMark stresses the CPU pipeline, CoreMark-PRO tests the
    entire processor, adding comprehensive support for multicore technology, a
    combination of integer and floating-point workloads, and data sets for
    utilizing larger memory subsystems. Together, EEMBC CoreMark and CoreMark-PRO
    provide a standard benchmark covering the spectrum from low-end microcontrollers
    to high-performance computing processors.
    For more information see: https://github.com/eembc/coremark-pro/blob/main/README.md
  
Location of underlying workload: https://github.com/eembc/coremark-pro

Packages required: bc,numactl

To run:
[root@hawkeye ~]# git clone https://github.com/redhat-performance/coremark_pro-wrapper
[root@hawkeye ~]# coremark_pro-wrapper/coremark_pro/coremark_pro_run

```
Options
  --commit <n>: Commit to use.  If not designated, will use tag v1.1.2743
  --no-overrides: If present we will not tune the make files
  --test_iterations n: number of times to run the test.
General options
  --home_parent <value>: Our parent home directory.  If not set, defaults to current working directory.
  --host_config <value>: default is the current host name.
  --iterations <value>: Number of times to run the test, defaults to 1.
  --run_user: user that is actually running the test on the test system. Defaults to user running wrapper.
  --sys_type: Type of system working with, aws, azure, hostname.  Defaults to hostname.
  --sysname: name of the system running, used in determing config files.  Defaults to hostname.
  --tuned_setting: used in naming the tar file, default for RHEL is the current active tuned.  For non
    RHEL systems, default is none.
  --usage: this usage message.
  --use_pcp: Enables use of Performance Co-Pilot in wrappers, defaults to 0 (disabled).
```

