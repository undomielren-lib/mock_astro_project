---
name: dataset-readme
description: Create a README.md for a research dataset or data repository using the README template. Use when asked to write, generate, or update a README for a dataset, data package, or research repository.
---

# Template source and reuse

This skill adapts Wendy Kozlowski’s (2025) Readme Template for Data, Cornell University eCommons Repository, https://doi.org/10.7298/mhns-zm71.2. The template is shared under the Creative Commons CC0 1.0 Universal Public Domain Dedication. Attribution is appreciated when re-sharing, but not required; citation is not required when using the template to document data or software.

# Dataset README

Write a README.md that follows the author dataset README template below, section by section and in the same order. Fill in what you can verify from the repository. Ask the user for everything else, and let them skip any question.

## Ground rules

- **Never invent facts.** Names, ORCIDs, emails, addresses, institutions, funding, licenses, DOIs, citations, publication links and collection dates come from the repository or from the user. If neither supplies them, they stay as placeholders. A plausible-looking ORCID or email is worse than a blank one.
- **Facts you can check, check.** Count rows and columns by reading the files. Take variable names from the actual headers. Take software versions from requirements or environment files. Do not estimate.
- **Say where inferred content came from.** When you describe methods or variables from code, comments or a manuscript in the repo, write it as a description of what the files show, and list these inferences for the user to confirm (Step 5).
- **Flag synthetic, simulated or mock data.** If the repo shows the data are generated, fictional or for teaching, say so plainly in the opening lines of the README, under General Information, and under Methods. Do the same for fictional references.
- **Delete all template help text.** Text in asterisks (*like this*) and the template's opening "Note" are instructions to the author, not README content. Remove them from the final file.

## Step 1: Inventory the repository

Before asking anything, gather what the repo already says:

1. List every file and folder.
2. Read the text files that carry metadata: CITATION.cff, LICENSE, requirements.txt / environment.yml / pyproject.toml, .bib files, any existing README, manuscript source (.tex, .md), and code docstrings and comments.
3. For each data file (CSV, TSV, JSON, Excel, etc.), record the number of rows and columns and the column names. Look for missing-data codes (blank cells, NA, NaN, -999, flags).
4. Note what each file is for and how files relate (for example: script X generates file Y; file Z is derived from file Y).
5. For binary files you cannot read (PDF, .docx, images), describe them from their filename, folder, and any text file that refers to them. Do not guess at their contents.

## Step 2: Sort every template field

Go through every field in the template and put it in one of three groups:

- **Found:** stated in the repo. Fill it in.
- **Inferred:** worked out from code, comments or a manuscript (for example, processing methods from a pipeline script). Fill it in and mark it for confirmation in Step 5.
- **Missing:** not in the repo. Ask the user in Step 3.

Fields that are almost always missing: contact details for the PI, co-investigator and alternate contact; geographic location of data collection; funding; links to publications and other data locations; people involved; version history.

## Step 3: Ask about missing information

Ask about all missing fields in **one message**, grouped by template section, so the user can answer in a single reply. Start the message with these options:

> I filled in what I could find in the repository. I need the information below to finish the README. For each item you can:
> - **answer it**,
> - reply **skip** to leave that item as a placeholder, or
> - reply **N/A** if it doesn't apply to this dataset (I'll write "Not applicable").
>
> Or reply **bypass** to skip all of these and get the README now, with placeholders wherever information is missing.

Then list each missing field with a short note on what's needed. Group the three contacts together, and say the template asks for at least two.

If the user answers some items and says nothing about others, ask once more about only the unanswered ones and offer **bypass** again. Do not ask a third time; treat anything still unanswered as skipped.

**When you cannot ask** (for example, you are running from an assigned GitHub issue or in another non-interactive setting): do not stop. Generate the README with placeholders. Then put the full list of missing items, in the Step 3 format, in your pull request description or final message, so the user can supply them and ask you to update the README.

## Step 4: Write the README

Use this structure exactly. Replace bracketed text, delete help text, and keep the section order.

- **Opening line:** `This readme file was generated on [today's date, YYYY-MM-DD] by [name]`. Use the name of the person the user identifies as the README's author. If none is given, use the PI's name. If neither is known, use a placeholder.
- **Placeholders:** write missing values as `[NOT PROVIDED: <what is needed>]`, for example `[NOT PROVIDED: PI ORCID]`. Fields marked N/A get `Not applicable`.
- **Contacts:** include each contact block the template has. If the user skips the alternate contact entirely, keep the block with placeholders rather than deleting it.
- **File List:** list every file or folder with a one-line description. Use a nested list or a table that mirrors the folder structure.
- **Methodological Information:** include the software and versions needed to run any scripts, how raw data become processed data, and any quality-assurance steps visible in the code (for example, flagging or sigma-clipping).
- **Data-Specific Information:** repeat the section once for each data file (not for code, figures or documents, which belong in the File List). For each one give the number of variables, number of rows, missing-data codes, specialized formats and abbreviations, and a variable table:

  | Variable | Description | Units | Values / labels |
  |---|---|---|---|

  Use "unitless" or "n/a" where units don't apply. Explain codes and flags (for example, `flag: 0 = good, 1 = bad epoch`).

Template to follow:

```
This readme file was generated on [YYYY-MM-DD] by [NAME]

# GENERAL INFORMATION

* Title of Dataset:

## Author/Principal Investigator Information
Name:
ORCID:
Institution:
Address:
Email:

## Author/Associate or Co-investigator Information
Name:
ORCID:
Institution:
Address:
Email:

## Author/Alternate Contact Information
Name:
ORCID:
Institution:
Address:
Email:

* Date of data collection:
* Geographic location of data collection:
* Information about funding sources that supported the collection of the data:

# SHARING/ACCESS INFORMATION

* Licenses/restrictions placed on the data:
* Links to publications that cite or use the data:
* Links to other publicly accessible locations of the data:
* Links/relationships to ancillary data sets:
* Was data derived from another source?
	* If yes, list source(s):
* Recommended citation for this dataset:

# DATA & FILE OVERVIEW

## File List:

* Relationship between files, if important:
* Additional related data collected that was not included in the current data package:
* Are there multiple versions of the dataset?
	* If yes, name of file(s) that was updated:
	* Why was the file updated?
	* When was the file updated?

# METHODOLOGICAL INFORMATION

## Description of methods used for collection/generation of data:

## Methods for processing the data:

## Instrument- or software-specific information needed to interpret the data:

* Standards and calibration information, if appropriate:
* Environmental/experimental conditions:
* Describe any quality-assurance procedures performed on the data:
* People involved with sample collection, processing, analysis and/or submission:

# DATA-SPECIFIC INFORMATION FOR: [FILENAME]

* Number of variables:
* Number of cases/rows:
* Variable List:
* Missing data codes:
* Specialized formats or other abbreviations used:
```

## Step 5: Check and report

Before you finish:

1. Confirm every file in the repo appears in the File List, and every data file has its own Data-Specific section.
2. Re-check row and column counts against the files.
3. Search the README for leftover asterisk help text and unreplaced template brackets such as `[NAME]` or `[FILENAME]`.
4. Make sure nothing in contact, funding, license or citation fields came from anywhere but the repo or the user.

Then tell the user, briefly:

- which fields are still placeholders (if any),
- which content you inferred and they should confirm, and
- where the README was saved.
