# Historical versus reconciled checksums

The original v9 package had 112 manifest entries: 110 matched, while two referenced bibliography `.bbl` files were absent. All included files covered by those manifests matched their expected digests. The embedded earlier v2 manifest had seven mismatches among 124 entries, including its selector and manuscript files. The outer ZIP digest and CRC checks do not authenticate those conflicting internal historical assertions. The mismatch history cannot be inferred from hashes alone.

The reconciliation preserves the original v9 directory and archive inputs. It does not overwrite their historical checksum records or claim they retroactively passed. Matching final OOF evidence is authenticated separately through restored byte-identical copies and their original authoritative-manifest digests. This also avoids using a newly generated manifest as proof of historical correctness.

The current release's checksum manifest is regenerated after correction and validation and names only existing selected release files. It includes source data, code, parameter/protocol evidence, figures and documents. It excludes the manifest itself, mutable verification output, build logs/caches and historical bulk. The complete original v9 cohort digest remains unchanged.
