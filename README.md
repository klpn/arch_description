# arch_description
This program is intended to be used to manage simple archival descriptions. To be sure, there are already sophisticated free tools like [ICA Atom](https://wiki.ica-atom.org/Main_Page) available to this aim; however, to my knowledge, they suffer from a lack of ability to easily generate reports adapted to local conditions, and as a result, archivists and other people who are working with smaller archives and who lack access to proprietary multi-user tools are often stuck with awkward word-processing or spreadsheet templates.

The user and database interfaces are based on [Camelot](http://www.python-camelot.com/) and use SQLite as a database backend. Reports are generated using easily customizable [Jinja2](https://github.com/mitsuhiko/jinja2) templates and [Pandoc](https://github.com/jgm/pandoc) (for full archival descriptions in DOCX, TeX or PDF format) or the basic version of [ReportLab](http://www.reportlab.com/) (for box labels). [Pypandoc](https://github.com/bebraw/pypandoc) is used to connect with Pandoc: this package can be installed on a Mac OS X or Windows system from [prebuilt binaries](https://pypi.python.org/pypi/pypandoc/) which include Pandoc.

To run the program, execute `main.py` in the package root with a Python 2 interpreter. If `setup.py build` is executed on a Windows system, [cx_Freeze](http://cx-freeze.sourceforge.net/) is used to create a directory `build` with a subdirectory `exe.win32-2.7` which contains a Windows executable `main.exe` along with all required libraries and templates. You should be able to run this program on any modern Windows system without any further installation. However, if you want to generate descriptions (but not box labels) in PDF format directly from the program, a LaTeX distribution has to be available on the system.

Note that [EAC-CPF](http://eac.staatsbibliothek-berlin.de/) or [EAD](http://www.loc.gov/ead/) import/export are not yet implemented. The included report templates are also still rather primitive.

##Data model and reports
The data model is organized in five levels: creators, archives, series and volumes, with a 1:N relation between each level (series may also be related with adjacency list relationships to support multiple levels of subseries). The `description` column in the `archives` table should be used to refer to a file containing a longer, verbose description of the archive. The contents of this file will be inserted in the Markdown template `description.md` in the report (see below), and should thus be written in Markdown. A standard text editor can be used for this. For more information about the supported Markdown format, see [Pandoc User's Guide](http://pandoc.org/README.html). 

Reports can be generated at the archive level, by opening an archive and choosing the relevant option. The different reports are generted from the database and different templates in `arch_description/templates`:

If you choose to print a description (*Spara förteckning*), the report will be generated from the following templates:

* The Markdown template `description.md`, which renders the different database columns.
* The DOCX document `description.docx` (for DOCX output) or the LaTeX template `description.tex` (for LaTeX or PDF output). These files define header and footer and document styles.

If you choose to print box labels (*Spara etiketter*), you will be presented with a dialog where you can choose paper and label size, number of labels on each sheet and other options. The default options are read from the file `labeloptions.json`, and the labels themselves are defined in the plain text template `label.txt`.
