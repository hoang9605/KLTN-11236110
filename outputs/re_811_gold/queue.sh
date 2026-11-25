#!/bin/bash
# Chạy nối tiếp sau ViHealthBERT (GPU 4 GB chỉ chạy được một mô hình mỗi lúc)
cd /c/Users/ASUS/dev/Code_Study/AI-KLTN
O=outputs/re_811_gold
while ! grep -aq "tổng\|Traceback" $O/log_vihealthbert.txt; do sleep 60; done
PY=.venv-gpu/Scripts/python.exe
$PY -X utf8 scripts/re_dataset/train_811_gold.py bert --base demdecuong/vihealthbert-base-syllable --tag vihealthbert_synth --extra $O/synth_validated_no_leak.jsonl --out $O </dev/null > $O/log_vihealthbert_synth.txt 2>&1
$PY -X utf8 scripts/re_dataset/train_811_gold.py bert --base Model/base/phobert-base --tag phobert --out $O </dev/null > $O/log_phobert.txt 2>&1
$PY -X utf8 scripts/re_dataset/train_811_gold.py bert --base Model/base/xlm-roberta-base --tag xlmr --out $O </dev/null > $O/log_xlmr.txt 2>&1
echo QUEUE_DONE
