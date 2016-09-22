# Monitoring jobs and resuming tasks
Keeping track of the tasks already completed, succesfully or not, or tasks
still pending can be somewhat annoying.  Resuming tasks that were not
completed, or that failed requires a level of bookkeeping you may prefer
to avoid.  `arange`  is designed to help with both issues.

Note that for this to work, your job should do logging using
[`alog`](alog.md).

## Monitoring a running job
Given either the CSV file or the task identifier range for a job, and its
log file as generated by `alog`, `arange` will provide statistics on the
progress of a running job, or a summary on a completed job.

If the log file's name is `bootstrap.pbs.log10493`, and the job was based
on an CSV data file `data.csv`, a summary can be obtained by
```bash
$ arange  --data data.csv  --log bootstrap.pbs.log10493  --summary
```
In case a job has been resumed, you should list all log files relevant to
the job to get correct results.

Since `arange` parses the data file, it also has the `--sniff` option to
specify the number of bytes to use to determine the dialect of the CSV
file.
```bash
$ arange  -t 1-250  --log bootstrap.pbs.log10493  --summary
```

Of course, `arange` works independently of `aenv`, so it also supports
keeping track of general job arrays using the `-t` flag, e.g.,

Sometimes it is useful to explicitly list the task identifiers of either
failed or completed jobs as task identifier ranges, this can be done by
adding the `--list_failed` or `--list_completed` flags respectively.

## Resuming jobs
`arange` primary purpose is in fact helping to determine which task
identifiers should be redone when an array job did not complete, or when
some of its tasks failed.  To get an identifier range of tasks that were
not completed, use
```bash
$ arange  --data data.csv  --log bootstrap.pbs.log10493`
```
or, when not using `aenv`
```bash
$ arange  -t 1-250  --log bootstrap.pbs.log10493`
```

If you want to include the tasks that failed, for instance when a bug that
caused this was fixed, simply add the `--redo` flag when invoking `arange`.

Help on the command is printed using the `--help` flag.