import pandas as pd
from pathlib import Path
import subprocess


data = pd.read_excel("./data/contact_with_mail_content_cv.xlsx")


class LATEXCompiler:

    def __init__(self, template_path, output_dir="output"):

        self.template_path = template_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        with open(template_path, "r", encoding="utf-8") as file:

            self.template = file.read()

    def compile_latex(self, tex_path):

        try:
            for _ in range(2):
                result = subprocess.run(
                    [
                        "pdflatex",
                        "-interaction=nonstopmode",
                        f"-output-directory={self.output_dir}",
                        tex_path.name,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )

        except Exception as e:

            print(e)

    def clean_auxiliary_files(self):

        extensions = [
            ".aux",
            ".log",
            ".out",
            ".toc",
            ".lof",
            ".lot",
            ".fls",
            ".fdb_latexmk",
            ".synctex.gz",
            ".tex",
        ]
        for ext in extensions:
            for file in self.output_dir.glob(f"*{ext}"):
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Erreur: {e}")

    def generate(self):

        placeholder = "{{HEADER}}"

        for idx, row in data.iterrows():

            content = self.template
            # value = "CentraleSupélec engineering student with strong skills in Python, data science, and quantitative finance, eager to join Citi's Quant Algo Trading team to contribute to algorithmic strategy development, quantitative modeling, and systematic trading research."
            value = str(row["cv_header"])
            content = content.replace(placeholder, value)
            output_name = f"CV_Amin_Belfkira_v{idx}"
            tex_path = self.output_dir / f"{output_name}.tex"

            with open(tex_path, "w", encoding="utf-8") as f:

                f.write(content)

            success = self.compile_latex(tex_path)


l = LATEXCompiler("./template/cv_base.tex")
l.generate()
l.clean_auxiliary_files()
