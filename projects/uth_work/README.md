# Clinical trial response classifier and Excel scoring

Scripts that ask a MedGemma model, through Ollama, to force a short JSON label, and (in two drivers) score those labels against columns of an annotated workbook.

## Context

I wrote this as a Paid Research Intern at UTHealth Houston (The University of Texas Health Science Center at Houston), Jun 2026 to Aug 2026.

The classifier is part of a clinical trial prescreening chatbot with a multi-agent, multi-model architecture. It routes patient responses to specialized agents for eligibility screening. MedGemma models were run and benchmarked with Ollama on a remote Linux server with an NVIDIA A100 GPU. The full chatbot, written in TypeScript and Next.js, is not in this repository.

Some of the code here is what I actually ran. A good portion has been sanitized to remove proprietary data and details.

<!-- TODO(Travis): Mark which files are as-run versus sanitized. -->

**[TODO: Mark which files are as-run versus sanitized.]**

The homepage lists a clinical-trial LLM classifier and a separate Excel annotation utility. Both sets of files live here, in `projects/uth_work`. The Excel code loads a workbook, asks the model to label each non-empty answer cell, and writes a count table. That is the scoring side of the classifier.

The classifier prompt calls the cell text a patient response. The workbook, any patient records, and any scored results are absent. The root `.gitignore` ignores `*.xlsx`.

## What I built

- `classify.py` sends one question and one answer to Ollama and parses the reply into a single label. The allowed labels are `"less than -1"`, `"-1"`, `"0"`, `"1"`, and `"more than 1"`. The system-instruction string is empty.
- `useClassify.py` and `identifyClassify.py` walk a workbook named `sharedAnnotationsQA.xlsx` (six columns: a question, then five answer columns). Each non-blank answer is labeled with `classify_response`. Counts are stored in a 5×5 table and written with `toExcel5x5Headers.py`.
- Those two drivers expect different labels than the current `classify.py` schema. See Notes.
- `identifyClassify.py` also copies the workbook into `info<id>/`, colors the header and each labeled cell, and prints the label in a matching terminal color.
- `ioChatbot.py` is a terminal chat that sends only the latest line. `memoryChatbot.py` prepends earlier turns into that same user message. `llmForcingTut.py` is a small structured-output example that must return `"0"`, `"1"`, or `"2"`. `ollamaMedgemmaTest.py` sends one fixed prompt and prints Ollama timing fields.
- `colorFont.py` wraps text in a 24-bit ANSI color from a hex string.

## Tech stack

Only what these files import or call:

- Python standard library: `time`, `subprocess`, `typing`
- [`ollama`](https://github.com/ollama/ollama-python) Python client (`chat`)
- [Pydantic](https://docs.pydantic.dev/) `BaseModel` for the JSON schema passed as `format`
- [openpyxl](https://openpyxl.readthedocs.io/) (`load_workbook`, `Workbook`, `PatternFill`)

Model tags hardcoded in the files: `medgemma:27b` in `classify.py`, and `medgemma1.5:4b` in the chat, tutorial, and timing scripts. Classification calls set `temperature` to 0 and `num_predict` to 20.

## How it works

`classify_response` builds a system message from the empty instruction string and a user message that quotes the question and the answer. Ollama is asked to match the `BucketChoice` schema. The reply is validated with Pydantic and the `choice` field is returned.

`useClassify.py` treats column 0 as the question and columns 1–5 as answers. A dictionary maps each header string onto an expected category (`negative`, `zero`, `one`, `more than one`). Rows 50–59 are skipped. Every other non-blank answer is classified, and the 5×5 table counts predicted labels. Labels outside that dictionary are counted as `other`. The table is written to `mistakes_output.xlsx`, with a fixed set of cells filled green.

`identifyClassify.py` does the same walk with a different expected-category map (`valid`, `illogical`, `clarify`, `skip`). It asks for an identifier on stdin, copies the source workbook to `info<id>/sharedAnnotationsQA<id>.xlsx`, colors cells from the predicted label, and writes `info<id>/mistakes_output<id>.xlsx`. It then copies that directory to `~/port`. A returned label of `nonresponsive` is rewritten to `illogical` before counting.

## How to run

These entry points run only when an Ollama server is up and the named model is already pulled. In the internship the models were served on the remote A100 machine described above. These scripts call the Ollama client with a model name and do not set a host. `classify.py` defines `classify_response` and does not call it (the sample calls at the bottom are commented out).

```bash
pip install ollama pydantic openpyxl
# ollama pull medgemma1.5:4b
python llmForcingTut.py
python ollamaMedgemmaTest.py
python ioChatbot.py
python memoryChatbot.py
```

`useClassify.py` and `identifyClassify.py` are not runnable from this repository. They open `sharedAnnotationsQA.xlsx` in the working directory, and that file is not checked in. `identifyClassify.py` also runs `mkdir` and `cp` through the shell with the identifier typed at the prompt, then copies the output folder to `~/port`.

`toExcel5x5Headers.py` and `colorFont.py` are imported by the drivers. Running them as scripts does not start a job.

## Repo contents

| File | What it does |
|---|---|
| `classify.py` | Forces one Ollama reply into the five numeric-bucket labels. System prompt is an empty string. Model tag is `medgemma:27b`. |
| `useClassify.py` | Reads `sharedAnnotationsQA.xlsx`, labels answer cells, skips rows 50–59, and writes a 5×5 count workbook. Expected categories are `negative` / `zero` / `one` / `more than one`. |
| `identifyClassify.py` | Copies that workbook into `info<id>/`, labels cells, colors them, writes the count workbook, and copies the folder to `~/port`. Expected categories are `valid` / `illogical` / `clarify` / `skip`. |
| `toExcel5x5Headers.py` | Writes a 5×5 table to Excel with row and column headers and greens five hardcoded cells. |
| `colorFont.py` | Returns the given text wrapped in an ANSI 24-bit foreground color. |
| `llmForcingTut.py` | Tutorial: force the model to return JSON `{"choice": "0"\|"1"\|"2"}` for one example sentence. |
| `ioChatbot.py` | Terminal chat. Each turn is a single user message, then the model is unloaded. |
| `memoryChatbot.py` | Same chat loop, with earlier turns concatenated into the next user message. |
| `ollamaMedgemmaTest.py` | One chat call, then prints total, load, prompt, and generation time plus token counts from the response object. |

## Notes / limitations

The three labeling files do not share one label set. `classify.py` can only return the five numeric buckets. `useClassify.py` counts `negative`, `zero`, `one`, `more than one`, and `other`, so a successful call to the current `classify_response` lands in `other` unless the model string happens to match those names. `identifyClassify.py` counts `valid`, `illogical`, `clarify`, `skip`, and `other`, and its count-table row headers are `yes`, `no`, `illogical`, `clarify`, `skip`. A commented line in that file refers to a header beginning `INCLUDE (falls under logical answer category)`. Nothing in the repo says which label set was the one used for a real review.

`to5x5` always paints the same five cells green: table positions `(0,0)`, `(1,0)`, `(2,1)`, `(3,2)`, and `(4,3)`. That pattern matches a layout where the first two source columns share one expected label. It is hardcoded, not computed from the headers.

No accuracy, agreement, or dataset description is stored in this folder. The count table is produced only when the missing workbook is present.

`identifyClassify.py` interpolates the typed identifier into shell commands (`mkdir` and `cp`). The copy to `~/port` runs on every successful pass.

`memoryChatbot.py` comments say each response is stateless. The code still prepends a growing transcript to the next user message, as one message, not as separate chat roles.

<!-- TODO(Travis): What was the annotation task (the numeric buckets versus valid/illogical/clarify/skip)? Which file matches the version you want to show? Was `sharedAnnotationsQA.xlsx` real, synthetic, or left out on purpose? What should a recruiter be told about results? -->

**[TODO: Fill in the task definition, which label set is current, what the spreadsheet was, and any result you want stated.]**
