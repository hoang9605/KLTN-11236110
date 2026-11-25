| Phương pháp | Dev P | Dev R | Dev F1 | Test P | Test R | Test F1 [CI95] |
|---|---:|---:|---:|---:|---:|---|
| majority | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 [0.0–0.0] |
| cooccur | 0.671 | 1.0 | 0.803 | 0.642 | 1.0 | 0.782 [0.709–0.847] |
| nearest | 0.703 | 0.542 | 0.612 | 0.706 | 0.529 | 0.605 [0.543–0.673] |
| rules | 0.864 | 0.198 | 0.322 | 0.865 | 0.235 | 0.37 [0.288–0.457] |
| feat_lr | 0.725 | 0.688 | 0.706 | 0.75 | 0.728 | 0.739 [0.659–0.805] |
| tfidf_svm | 0.844 | 0.792 | 0.817 | 0.841 | 0.853 | 0.847 [0.781–0.898] |
| tfidf_lr | 0.757 | 0.812 | 0.784 | 0.803 | 0.868 | 0.834 [0.768–0.888] |
| vihealthbert | 0.809 | 0.792 | 0.8 | 0.873 | 0.86 | 0.867 [0.805–0.918] |

{
 "train": {
  "pairs": 1632,
  "labels": {
   "NO_RELATION": 766,
   "located_at": 714,
   "treated_by": 44,
   "diagnosed_by": 26,
   "treated_by_procedure": 69,
   "has_dosage": 13
  }
 },
 "dev": {
  "pairs": 143,
  "labels": {
   "located_at": 83,
   "treated_by_procedure": 11,
   "NO_RELATION": 47,
   "treated_by": 2
  }
 },
 "test": {
  "pairs": 212,
  "labels": {
   "NO_RELATION": 76,
   "located_at": 115,
   "has_dosage": 3,
   "diagnosed_by": 3,
   "treated_by_procedure": 9,
   "treated_by": 6
  }
 }
}
