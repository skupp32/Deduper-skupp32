This is the first line and will always be included.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA 16    2    8    36   2S1M1I1M    *    0    0    AAAAA    EEEEE
```
This line will be included as the UMI is different from the first line.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAT 16    2    8    36   2S1M1I1M    *    0    0    AAAAT    EEEEE
```
This line will not be included because the position is adjusted by POS and the difference in cigar string.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA 16    2    7    36   2S3M    *    0    0    AAAAA    EEEEE
```
This line will not be included because of the difference in POS and cigar string.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA 16    2    6    36   2S1D3M    *    0    0    AAAAA    EEEEE
```
This line will be included as it is the first line on the + strand.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA 0    2    8    36   2S1M1I1M    *    0    0    AAAAA    EEEEE
```
This line will not be included because of the difference in POS and cigar string.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA 0    2    6    36   3M1I1M    *    0    0    AAAAA    EEEEE
```
This line will not be included as its UMI in not in the list of given UMIs.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:ACG 0    2    8    36   2S1M1I1M    *    0    0    ACGAA    EEEEE
```
This line will be included as it is the first on chromosome 1.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA 0    1    8    36   2S1M1I1M    *    0    0    AAAAA    EEEEE
```
This line will not be included as it is a direct duplicate of a preceding line.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAA 0    2    8    36   2S1M1I1M    *    0    0    AAAAA    EEEEE
```
This line will not be included as the UMI in the QNAME does not appear in the sequence.
```
NS500451:154:HWKTMBGXX:1:11101:15364:1139:AAT 0    2    8    36   2S1M1I1M    *    0    0    AAAAA    EEEEE
```
