## Setup
- Sample Rate: 44100
- Block Size: 2048
- Power Trheshold: 800

## 25-35 Db
- File: `data_dir/dtmf_test_sequence_25-35_db.wav`
- Guesed Sequence: [2, 1, 7, 4, 7, 3, 0, 6, 0, *, 4, 3, 1, 0, 0, 8, 6, 6, 8, 7, 8, 3, 7, 1, 1]
- Original Sequence: [2, 1, 7, 7, 3, 0, 6, 0, 4, 3, 1, 0, 8, 6, 6, 8, 7, 8, 3, 7]
- Accuracy = $\frac{20}{25} \times 100\% = 80.00\%$

## 35-45 Db
- File: `ddata_dir/dtmf_test_sequence_35-45_db.wav`
- Guesed Sequence: [2, 1, 7, 7, 3, 0, 6, 0, 4, 3, 1, 0, 8, 6, 6, 8, 7, 8, 3, 7, 4, 1, *]
- Original Sequence: [2, 1, 7, 7, 3, 0, 6, 0, 4, 3, 1, 0, 8, 6, 6, 8, 7, 8, 3, 7]
- Accuracy = $\frac{20}{23} \times 100\% = 86.96\%$

## 45-55 Db
- File: `data_dir/dtmf_test_sequence_45-55_db.wav`
Guesed Sequence: [2, 1, 7, 7, 5, 3, 0, 6, 0, 4, 5, 3, 1, 0, 8, 6, 6, 8, 2, 7, 5, 8, 5, 3, 7, *]

- Original Sequence: [2, 1, 7, 7, 3, 0, 6, 0, 4, 3, 1, 0, 8, 6, 6, 8, 7, 8, 3, 7]
- Accuracy = $\frac{20}{26} \times 100\% = 76.92\%$

## 65-75 Db
- File: `data_dir/dtmf_test_sequence_65-75_db.wav`
- Guesed Sequence: [2, 1, 7, 8, 7, 3, 0, 8, 6, 0, 4, 3, 1, 2, 0, 8, 9, 5, 6, 6, 8, 7, 4, 8, 3, 7, 3, 1, 5, *]
- Original Sequence: [2, 1, 7, 7, 3, 0, 6, 0, 4, 3, 1, 0, 8, 6, 6, 8, 7, 8, 3, 7]
- Accuracy = $\frac{20}{30} \times 100\% = 66.67\%$
