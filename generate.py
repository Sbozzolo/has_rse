#!/usr/bin/env python3

import os
import json
import has_rse

def main():
    if not os.path.isdir("build"):
        os.mkdir("build")
    out_json = "build/universities.json"
    has_rse.generate_json(out_json)
    with open(out_json, "r") as f:
        university_data = json.load(f)
    has_rse.generate_html(university_data, "build/index.html")

if __name__ == "__main__":
    main()
