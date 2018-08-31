import subprocess
import sys
import re
import os

path_to_pdftotext = "bin/pdftotext.exe"
path_to_pypdfocr = "bin/pypdfocr.exe"


def get_summary(parent_path, pdf_path, output_path):
    tmp_output_path = "%s_tmp.txt" % pdf_path.rstrip(".pdf")
    pdf_path_ocr = "%s_ocr.pdf" % pdf_path.rstrip(".pdf")
    out = subprocess.call([path_to_pypdfocr, pdf_path])

    if out != 0:
        for aux in os.listdir(parent_path):
            if os.path.join(parent_path, aux) != pdf_path:
                os.remove(os.path.join(parent_path, aux))

        out = subprocess.call([path_to_pdftotext, pdf_path, tmp_output_path])
    else:
        out = subprocess.call([path_to_pdftotext, pdf_path_ocr, tmp_output_path])

    with open(tmp_output_path, "r") as output:
        content = output.read()
        paragraphs_with_date = re.findall(r"[^\n]*([0-9]{1,2}.[0-9]{1,2}\.[0-9]{2,4})[^\n]*\n", content)
        paragraphs_with_date.extend(re.findall(r"[^\n]*([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{2,4})[^\n]*\n",
                                              content))
        paragraphs_with_date.extend(re.findall(r"[^\n]*([A-Z][a-z]{2}\s\d{2},\s\d{4})[^\n]*\n", content))
        paragraphs_with_date.extend(re.findall(r"[^\n]*([A-Z][a-z]{9}\s\d{2},\s\d{4})[^\n]*\n", content))
        keywords = ["rebuild", "rejuvenation", "reshape", "reshaping", "streamlining", "rationalization",
                        "specialization",
                        "refocusing", "asset restructuring", "restructuring", "reengineering", "cost cutting",
                        "cost reduction",
                        "cost savings", "reconstruction", "repositioning", "shake-up", "consolidation", "disposal",
                        "spin off", "step down", "management change"]

        paragraphs_with_keywords = []
        for keyword in keywords:
            paragraphs_with_keywords.extend(re.findall(r"(?i)[^\n]*%s[^\n]*\n" % keyword, content))

        has_information = False
        if len(paragraphs_with_keywords) > 0:
            has_information = True
            # Try and delete duplicates
            for paragraph in paragraphs_with_keywords:
                while paragraphs_with_keywords.count(paragraph) > 1:
                    paragraphs_with_keywords.remove(paragraph)

            with open(output_path, "w") as summary:
                summary.write("DATES\n")
                for date in paragraphs_with_date:
                    summary.write("%s\n" % date)

                summary.write("PARAGRAPHS WITH KEYWORDS\n")
                for paragraph in paragraphs_with_keywords:
                    summary.write("%s\n" % paragraph)
    os.remove(tmp_output_path)
    return has_information


if len(sys.argv) == 2:
    for f in os.listdir(sys.argv[1]):
        get_summary(os.path.join(sys.argv[1], f),
                    os.path.join(os.path.join(sys.argv[1], f), "%s.pdf" % f),
                    os.path.join(os.path.join(sys.argv[1], f), "%s_summary.txt" % f))
