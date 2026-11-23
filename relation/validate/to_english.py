"""Step 2: map every entity string of the synthetic pool to an English term (and a code when there is one).

  CONDITION -> ICD-10 code via normalization.ICD10Normalizer; English name from the DISEASE NAME column of the MoH
               ICD-10 file. That column is wrong for some 3-character categories (I10 is given the name of I09,
               I48 the name of I47), so an English name shared by two different 3-character codes is not trusted.
  DRUG      -> RxCUI via normalization.RxNormNormalizer (RxNav, cached).
  all types -> English term from en_terms_manual.json (written by Claude, to be checked by the user).
               'generic' marks a vague / noise mention, which cannot be checked.

Output: relation/data/synth/validate/en_terms.json  {"LABEL|text": {"en": ..., "code": ..., "code_name_en": ...}}
Run: .venv\\Scripts\\python.exe -X utf8 -m relation.validate.to_english
"""
import json
from collections import defaultdict

import pandas as pd

from normalization.icd10 import ICD10Normalizer
from normalization.rxnorm import RxNormNormalizer

from .units import OUT, SYNTH, load

ICD_FILE = "ICD-10/phu-lu-c-1-danh-mu-c-icd-10-thay-the-dmdc-phie-n-ba-n-6.xlsx"


def icd_english():
    d = pd.read_excel(ICD_FILE, sheet_name="ICD10", header=2, usecols=["MÃ BỆNH", "DISEASE NAME", "TÊN BỆNH"])
    names, codes_of = {}, defaultdict(set)
    for code, en, vi in zip(d["MÃ BỆNH"], d["DISEASE NAME"], d["TÊN BỆNH"]):
        code, en = str(code).strip(), str(en).strip()
        names[code] = {"en": en, "vi": str(vi).strip()}
        if len(code) == 3:
            codes_of[en.lower()].add(code)
    for code, n in names.items():
        n["trusted"] = not (len(code) == 3 and len(codes_of[n["en"].lower()]) > 1)
    return names


def main():
    manual = json.loads((OUT / "en_terms_manual.json").read_text(encoding="utf-8"))
    pool = load(SYNTH / "pool.jsonl")
    ents = sorted({(e["label"], e["text"].lower()) for r in pool for e in r["entities"]})
    icd, rx, icd_names = ICD10Normalizer(), RxNormNormalizer(), icd_english()
    out, missing = {}, []
    for label, text in ents:
        en = manual.get(label, {}).get(text)
        if en is None:
            missing.append(f"{label}|{text}")
        item = {"label": label, "vi": text, "en": None if en in (None, "generic") else en,
                "generic": en == "generic", "code": None, "code_system": None, "code_name_en": None}
        res = icd.normalize(text) if label == "CONDITION" else rx.normalize(text) if label == "DRUG" else None
        if res:
            item["code"], item["code_system"] = res.code, res.ontology
            if label == "CONDITION":
                n = icd_names.get(res.code, {})
                item["code_name_en"] = n.get("en") if n.get("trusted") else None
                item["code_name_vi"] = n.get("vi")
            else:
                item["code_name_en"] = res.label_standard
        out[f"{label}|{text}"] = item
    (OUT / "en_terms.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"entities": len(out), "missing_manual": missing,
                      "generic": sum(v["generic"] for v in out.values()),
                      "with_code": sum(v["code"] is not None for v in out.values()),
                      "icd_name_untrusted": sorted(k for k, v in out.items()
                                                   if v["code_system"] == "ICD-10" and not v["code_name_en"])},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
