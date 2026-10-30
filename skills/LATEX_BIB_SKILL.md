---
name: latex-bibliography
description: Create, fix, or check BibTeX bibliographies for LaTeX documents using the standard BibTeX entry-type templates, including building a .bib file from a folder of paper PDFs. Use when asked to write or clean up a .bib file, make a bibliography from a folder of papers, convert references to BibTeX, fix citation or bibliography errors, or set up \bibliographystyle, natbib, or biblatex in a LaTeX project.
---

# LaTeX Bibliography (BibTeX)

Write and correct `.bib` entries using the standard BibTeX templates, and make sure the LaTeX document cites and prints them correctly. These rules follow the Wikibooks *LaTeX/Bibliography Management* chapter (BibTeX section): https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management#BibTeX

## Ground rules

- **Never invent bibliographic data.** Authors, titles, journals, volumes, pages, years, publishers, DOIs and URLs come from the user, the source document, or an existing entry. If a required field is missing, ask (see "Missing information") rather than filling it with something plausible. An invented DOI or page range is worse than a gap.
- **Pick the entry type that matches the work**, not the one with the fewest required fields. A conference paper is `@inproceedings`, not `@misc`.
- **Keep fields the user already has**, even ones the style won't print (for example `abstract`, `keywords`, `note`). Only remove a field if the user asks or it is clearly wrong.
- **Match the project's system.** Check the preamble first. A project uses either BibTeX (with or without natbib) or biblatex. Do not mix commands from both (see "Document setup").

## Entry templates

Each template lists **required** fields first, then **optional** fields. BibTeX warns when a required field is missing. An entry may hold other fields too, and styles ignore fields they don't use.

Use only one of a pair like `author/editor` or `volume/number`.

### @article — a paper in a journal or magazine
Required: `author`, `title`, `journal`, `year`
Optional: `volume`, `number`, `pages`, `month`, `note`
```bibtex
@article{key,
  author  = {},
  title   = {},
  journal = {},
  year    = {},
  volume  = {},
  number  = {},
  pages   = {},
}
```

### @book — a book with a publisher
Required: `author` or `editor`, `title`, `publisher`, `year`
Optional: `volume` or `number`, `series`, `address`, `edition`, `month`, `note`
```bibtex
@book{key,
  author    = {},
  title     = {},
  publisher = {},
  year      = {},
  address   = {},
  edition   = {},
}
```

### @booklet — a printed and bound work with no named publisher
Required: `title`
Optional: `author`, `howpublished`, `address`, `month`, `year`, `note`

### @inbook — a part of a book (a chapter or page range) that has no title of its own
Required: `author` or `editor`, `title`, `chapter` and/or `pages`, `publisher`, `year`
Optional: `volume` or `number`, `series`, `type`, `address`, `edition`, `month`, `note`

### @incollection — a part of a book that has its own title (e.g., a chapter in an edited volume)
Required: `author`, `title`, `booktitle`, `publisher`, `year`
Optional: `editor`, `volume` or `number`, `series`, `type`, `chapter`, `pages`, `address`, `edition`, `month`, `note`
```bibtex
@incollection{key,
  author    = {},
  title     = {},
  booktitle = {},
  editor    = {},
  publisher = {},
  year      = {},
  pages     = {},
}
```

### @inproceedings — a paper in conference proceedings (`@conference` is the same type)
Required: `author`, `title`, `booktitle`, `year`
Optional: `editor`, `volume` or `number`, `series`, `pages`, `address`, `month`, `organization`, `publisher`, `note`
```bibtex
@inproceedings{key,
  author    = {},
  title     = {},
  booktitle = {},
  year      = {},
  pages     = {},
  publisher = {},
}
```

### @manual — technical documentation
Required: `title`
Optional: `author`, `organization`, `address`, `edition`, `month`, `year`, `note`

### @mastersthesis — a master's thesis
Required: `author`, `title`, `school`, `year`
Optional: `type` (e.g., `{Diploma thesis}`), `address`, `month`, `note`

### @phdthesis — a doctoral dissertation
Required: `author`, `title`, `school`, `year`
Optional: `address`, `month`, `keywords`, `note`

### @proceedings — an entire conference proceedings volume
Required: `title`, `year`
Optional: `editor`, `volume` or `number`, `series`, `address`, `month`, `organization`, `publisher`, `note`

### @techreport — a report from an institution, often numbered in a series
Required: `author`, `title`, `institution`, `year`
Optional: `type`, `number`, `address`, `month`, `note`

### @unpublished — a work with an author and title that was not formally published
Required: `author`, `title`, `note`
Optional: `month`, `year`
Use `note` to say what it is, e.g., `note = {Manuscript in preparation}`.

### @misc — anything that fits no other type (websites, software, datasets, preprints in plain BibTeX)
Required: none
Optional: `author`, `title`, `howpublished`, `month`, `year`, `note`
```bibtex
@misc{key,
  author       = {},
  title        = {},
  howpublished = {\url{}},
  year         = {},
  note         = {Accessed: YYYY-MM-DD},
}
```

## Field formatting rules

### Citation keys
- Use a short, unique key with no spaces, such as `surnameYEARword` (e.g., `lomb1976`, `greenwade1993latex`).
- Keys are case-sensitive in practice. Keep the key in `\cite{...}` identical to the key in the `.bib` file.
- Never change an existing key without updating every `\cite` that uses it.

### Delimiters
- Use either braces `{...}` or double quotes `"..."` around field values, and be consistent within a file. Braces are safer, because a quote inside a quoted value (for example the umlaut command `\"o`) ends the field early.
- A purely numeric `year` may be left bare: `year = 2023`.
- End every field with a comma. A trailing comma after the last field is allowed.

### Authors and editors
- Separate every name with ` and `, never with commas or `&`. BibTeX inserts the commas and the final "and" itself.
  `author = {Lomb, N. R. and Scargle, J. D.}`
- Write each name as either `Forename Surname` or `Surname, Forename`. Prefer `Surname, Forename`; it is unambiguous.
- With `Forename Surname`, BibTeX treats the last word as the surname, so brace multi-word surnames: `John {von Neumann}`. With `Surname, Forename` the comma already marks the split: `von Neumann, John`.
- For a suffix, use `Surname, Jr., Forename`.
- Brace corporate or organizational authors so they are treated as a single name: `author = {{Fermentas Inc.}}`, `author = {{NASA Goddard Space Flight Center}}`.
- For long author lists, `and others` produces "et al." in most styles. Use it only if the user wants a truncated list or the source gives one.

### Titles and capitalization
- Many styles change title case (often to sentence case). To keep a word's capitalization, put braces around **that word**: `title = {The {LaTeX} Companion}`, `title = {RR {Lyrae} Stars in {Kestrel-7}}`.
- Protect proper nouns, acronyms, chemical formulas and anything else whose case must not change.
- Do **not** wrap the whole title in braces. That blocks the style's capitalization rules entirely. Double braces (`{{...}}`) are a last resort for one stubborn entry, not a default.
- Brace whole words, not single letters (`{NASA}`, not `{N}{A}{S}{A}`). Braced single letters can disturb kerning.
- Math in titles goes in `$...$` as usual.

### Special characters and accents
- If the document is compiled with UTF-8 support (pdfLaTeX with `\usepackage[utf8]{inputenc}`, which is the default in modern LaTeX, or with XeLaTeX/LuaLaTeX), accented characters may be written directly: `Sørensen`, `Müller`.
- Otherwise, use LaTeX accent commands inside braces so sorting and parsing work: `S{\o}rensen`, `M{\"u}ller`, `Fran{\c{c}}ois`.
- Escape LaTeX special characters in field text: `\&`, `\%`, `\_`, `\#`. URLs inside `\url{}` are the exception.

### Pages
- Use a double hyphen for ranges: `pages = {447--462}`. A single page needs no hyphen.

### Month
- Prefer BibTeX's built-in abbreviations, written **without** braces or quotes: `month = jan`, `month = oct`. The style then prints the month in its own format.
- A full name in braces (`month = {November}`) also works, but prints exactly as written.

### URLs and DOIs
- Standard styles (`plain`, `unsrt`, `abbrv`, `alpha`) ignore `url` and `doi` fields. For those styles, put the link in `howpublished = {\url{...}}` (in `@misc`) or in `note`, and load `\usepackage{url}` or `\usepackage{hyperref}`.
- The natbib styles (`plainnat`, `abbrvnat`, `unsrtnat`) print `url` and `doi` fields directly. Load `url` or `hyperref`.
- Write a DOI without the resolver prefix: `doi = {10.1086/160554}`, not `https://doi.org/...`.
- For web pages, add an access date in `note`, e.g., `note = {Accessed: 2026-10-30}`.

### Comments
- `%` does **not** comment out a line inside a BibTeX entry. Anything outside an `@type{...}` entry is ignored, so to disable a field or entry, move it outside the entry. Or rename the field to something no style uses (e.g., `OPTvolume`), which BibTeX ignores.

## Document setup

### Plain BibTeX
```latex
\bibliographystyle{plain}       % no .bst extension
\bibliography{references}       % no .bib extension; several files: {refs1,refs2} with no spaces
```
Put these where the reference list should appear, usually just before `\end{document}`.

Standard styles:
- `plain`: numbered, sorted alphabetically
- `unsrt`: numbered, in order of first citation
- `abbrv`: like `plain` with abbreviated first names
- `alpha`: labels built from author and year, e.g., `[Sim95]`

Cite with `\cite{key}`, or `\cite{key1,key2}` for several.

### natbib (author–year or numerical)
```latex
\usepackage[round,authoryear]{natbib}   % or [square,numbers], [super], add sort&compress
...
\bibliographystyle{plainnat}            % or abbrvnat, unsrtnat
\bibliography{references}
```
Citation commands:
- `\citet{key}` gives a textual citation: Lomb (1976)
- `\citep{key}` gives a parenthetical one: (Lomb, 1976)
- `\citet*` and `\citep*` give the full author list
- `\citeauthor{key}`, `\citeyear{key}`, `\citeyearpar{key}`
- `\citealt` and `\citealp` drop the parentheses
- `\citep[p.~5]{key}` adds a page note; `\citep[see][]{key}` adds a prefix

Use `\citet` when the citation is part of the sentence ("as shown by \citet{x}") and `\citep` when it is a parenthetical reference at the end of a claim. Journal classes often bring their own natbib-compatible styles (e.g., AASTeX, REVTeX's `apsrev`, `IEEEtranN`). Use the class's style when one is present.

### biblatex (only if the project already uses it, or the user asks)
biblatex reads the same `.bib` syntax but supports more entry types and fields (`@online`, `@report`, `date`, `journaltitle`, `doi`, `eprint`).
```latex
\usepackage[style=authoryear,backend=biber]{biblatex}
\addbibresource{references.bib}   % extension required here
...
\printbibliography
```
With biblatex, do not use `\bibliographystyle` or `\bibliography`, and do not load natbib.

### Compiling
BibTeX needs this sequence: `pdflatex main`, then `bibtex main`, then `pdflatex main` twice. With biblatex and biber, run `biber main` in place of `bibtex main`. Overleaf and `latexmk` run the sequence automatically.

## Building a bibliography from a folder of papers

Use this when the user points to a folder of papers (usually PDFs) and wants a `.bib` file made from them. Every field must come from the paper itself, or from a DOI lookup if one is available. Never fill a field from the filename alone or from what the paper is "probably" about.

### 1. List the papers
- Find every PDF in the folder, including subfolders unless the user says otherwise.
- Note any other files that may hold references (`.bib`, `.ris`, `.enw`, `.nbib`, `.txt`) and ask whether to include them.
- If there is already a `.bib` file in the folder or project, read it first. Update matching entries instead of creating duplicates, and keep their citation keys.

### 2. Extract text from each PDF
Try these in order and stop at the first that works:
1. `pdftotext -l 2 -layout paper.pdf -` (from Poppler) to get the first two pages.
2. A Python library: `pypdf` (`PdfReader(path).pages[0].extract_text()`) or `pdfplumber`.
3. The PDF's embedded metadata (`pdfinfo paper.pdf`, or `PdfReader(path).metadata`). Treat embedded metadata as a hint only, because it is often wrong or empty (titles like "Microsoft Word - draft3.docx"). The printed text wins when they disagree.

If a tool isn't installed, install it if you can (`pip install pypdf`, or the system's Poppler package). If you can't install anything, say so and continue with what you have.

If a PDF has little or no extractable text, it is probably a scan. Note it as **needs OCR**, don't guess its contents, and move on. Run OCR only if the user asks and a tool such as `ocrmypdf` or `tesseract` is available.

### 3. Pull out the reference details
Read the title page and header or footer, where publication details usually appear:
- **Title:** the main heading on page 1.
- **Authors:** the name list under the title, in printed order. Drop affiliation markers (superscript numbers, symbols, asterisks).
- **Venue:** the journal name, proceedings title, or publisher, often in the header, footer or first-page banner. Also note whether it's a preprint (an arXiv ID, "submitted to", "preprint").
- **Year, volume, issue and pages:** usually in a citation line such as "Journal Name, 12, 101–118 (2023)". Convert en dashes to `--`.
- **DOI:** search the text for `10.\d{4,9}/[^\s]+`. Also look for arXiv IDs (`arXiv:2401.01234`).
- **Thesis or report details:** the institution or school, the degree type, and the report number.

Do **not** take details from the paper's own reference list. Those belong to other works.

### 4. Choose the type and build the entry
- Pick the entry type from the templates above, based on what the paper is: a journal article is `@article`, a conference paper is `@inproceedings`, a thesis is `@phdthesis` or `@mastersthesis`, and a report is `@techreport`.
- Use `@misc` for a preprint with no journal yet. Add `howpublished = {arXiv:XXXX.XXXXX}` or an eprint note, plus the URL.
- Make the citation key `firstauthorsurnameYEARfirsttitleword`, lowercased with accents removed (e.g., `okafor2023iband`). Add `a`, `b` and so on if two keys collide.
- Apply all the field formatting rules above: authors joined with `and`, protected capitals in titles, `--` for pages, escaped special characters.
- Add a `file` field with the PDF's path relative to the `.bib` file (e.g., `file = {papers/Okafor_2023.pdf}`). Styles ignore this field, but it lets anyone trace each entry back to its source.

### 5. Optional DOI lookup
If a DOI was found **and** the environment has internet access, you may fetch the official metadata from `https://api.crossref.org/works/<DOI>` or `https://doi.org/<DOI>` (with the header `Accept: application/x-bibtex`).
- Use the lookup to fill gaps and correct extraction errors. It does not replace what the paper says. If the lookup returns a different title or authors, the DOI may be wrong; flag it rather than overwriting.
- If there's no internet access or the lookup fails, continue without it. This step is optional.
- Never search the web by title to "find" a paper that has no DOI in its text, unless the user asks. Similar titles return the wrong paper too often.

### 6. Flag uncertainty
Keep track of each field you were not sure about: text that extracted garbled, a year you inferred from a copyright line, an author list that may be cut off, a type you chose between two options. Report these in the summary along with any missing required fields, and ask about them as described in "Missing information".

If a paper appears to be fictional, a mock or a sample (for example, it carries a banner saying so), keep that clear in the entry with a `note` field such as `note = {Fictional paper for training use}`.

### 7. Write and check the file
- Write the entries to the `.bib` file the user names. If they don't name one, write `references.bib` in the folder's parent directory, and say where it is.
- Order entries alphabetically by citation key unless the user prefers otherwise.
- Check the result with the Workflow steps below: balanced braces, unique keys, required fields. If you can, compile a short test document that cites every entry with `\nocite{*}`.
- In your summary, include a table with one row per paper: the PDF filename, the citation key, the entry type, and the status (complete, has gaps, needs OCR, or skipped).

## Missing information

When a required field is missing and cannot be found in the material provided, ask the user. Put all the gaps in **one message**, listed by citation key, with these options:

> Some entries are missing required fields. For each you can **answer**, reply **skip** to leave the field out (BibTeX will warn about it), or reply **bypass** to finish now with every gap left as is. I'll list what's still missing at the end.

If you can't ask (for example, you're running non-interactively), do not invent values. Leave the fields out and list them in your final message or pull request description.

## Workflow

1. **Read the setup.** Find the `.bib` file(s) and the LaTeX preamble. Note whether the project uses plain BibTeX, natbib or biblatex, and which style.
2. **Check every entry:**
   - Is the entry type right for the work?
   - Are the required fields present?
   - Are authors separated with `and`?
   - Are proper nouns and acronyms in titles protected with braces?
   - Do page ranges use `--`?
   - Do months use the bare abbreviations?
   - Are special characters escaped?
   - Are the braces balanced?
   - Are delimiters consistent?
3. **Check the citations in the document:**
   - Every `\cite`-family key exists in the `.bib` file.
   - No key is defined twice in the `.bib` file.
   - Note entries that are never cited. Leave them in place; only bibliography styles that list all entries print them.
4. **Fix and report.** Make the corrections, keeping the existing order of entries and fields where possible. Ask about missing required data as described above.
5. **Compile if you can.** Run the compile sequence and read the `.blg` log. Clear warnings such as `empty journal in ...`, `I didn't find a database entry for ...` and `Repeated entry`. Also check the `.log` for `Citation ... undefined`.
6. **Summarize briefly:** what you changed, any fields still missing, and anything the user should confirm (for example, an entry type you changed or a name split you were unsure of).
