import os
import sys

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

try:
    print("Starting full evaluation on all 2,229 samples of VietMed-NER test split...", flush=True)
    from eval.run_eval import main
    sys.argv = ["run_eval.py"]
    main()
    print("\nALL DONE: EVALUATION SUITE COMPLETED SUCCESSFULLY!", flush=True)
except Exception as e:
    import traceback
    traceback.print_exc()

