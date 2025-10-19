---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 1.2 Jupyter Notebook

## What is a Jupyter Notebook (`.ipynb`)?

A Jupyter Notebook file (`.ipynb`) is an interactive document used primarily for programming in Python and data science. It combines **code**, **text (Markdown)**, **mathematical equations (LaTeX)**, **visualizations**, and **outputs** all in one place.

These notebooks are great for:
- **Exploration**: test ideas, run code step by step, and immediately see results.
- **Documentation**: include explanations, titles, and images to make your code understandable.
- **Teaching and Learning**: ideal for walking through programming concepts interactively.
- **Creating Reports**: Great for sharing blocks of code with clear documentation and replicable results, as the Jupiter notebook stores the output in its metadata, which can then be seen when opening the shared notebook.

## Key Features

- **Code Cells**: Run Python code and see outputs directly below the cell.
- **Markdown Cells**: Write formatted text using Markdown to explain the code or results.
- **Interactive Outputs**: Include plots, tables, and images inline.
- **Kernel-based Execution**: The notebook uses a kernel (e.g., our *psy126* virtual environmant) that keeps track of the code you run. 
- **Cell Execution Order**: You can run cells in any order—helpful but requires attention to variable state.

## Google Colab vs VS Code

Both Google Colab and Visual Studio Code support Jupyter Notebooks, but they offer different workflows, strengths, and limitations depending on your needs and environment.

### Google Colab

[Google Colab](https://colab.research.google.com/) is a free cloud-based platform developed by Google for running Python notebooks.

**Pros**:
- ✅ **No installation required**: Everything runs in your browser.
- ✅ **Free GPU and TPU access**: Great for machine learning and deep learning.
- ✅ **Integrated with Google Drive**: Easy to save, share, and collaborate.
- ✅ **Pre-installed packages**: Most common data science libraries are already installed.

**Cons**:
- ❌ **Limited session time**: Colab will disconnect after ~12 hours (shorter for idle sessions).
- ❌ **Restricted environment**: You can't fully control the OS, system packages, or GPU drivers.
- ❌ **Dependency conflicts**: You may hit issues when trying to install custom libraries.
- ❌ **Privacy and data handling**: Data must be uploaded to Google's servers.

**Technical Details**:
- Runs on virtualized Ubuntu containers.
- Uses a managed IPython kernel in the backend.
- Supports multiple backends (CPU, GPU, TPU), selectable per notebook.
- File system is ephemeral unless mounted to Drive or external storage.

---

### VS Code + Jupyter (Local)

Visual Studio Code provides local and customizable access to Jupyter environments via its extensions.

**Pros**:
- ✅ **Full environment control**: You can use Conda, virtualenv, or Docker.
- ✅ **Persistent state**: You decide when to restart, save, or clean environments.
- ✅ **Advanced tooling**: Integrate Git, linters, debuggers, and profilers.
- ✅ **Custom hardware support**: Leverage your machine’s CPU, GPU, or RAM.
- ✅ **Offline use**: Perfect for working without internet access.

**Cons**:
- ❌ **Setup required**: Installation of VS Code, Python, and extensions is necessary.
- ❌ **No free GPU unless you have one**: For tasks that require heavy computation — such as those you might encounter during your practical project or thesis (e.g. if you work with big data) — you can request access to the university's High Performance Computing (HPC) cluster [Link to wiki](https://hpcwiki.uol.de/).

**Technical Details**:
- Notebooks are rendered via the Jupyter extension in VS Code.
- Executes code using the selected kernel (e.g. Python environment).
- Local file system access for loading datasets or saving outputs.
- Fully customizable environments (e.g. different Python versions, CUDA support).

---

### Summary Table

| Feature                | Google Colab         | VS Code (Local)            |
|------------------------|----------------------|-----------------------------|
| Setup Required         | ❌ None              | ✅ Yes                      |
| Free GPU Access        | ✅ Yes               | ❌ No (unless local GPU)    |
| Custom Environments    | ❌ Limited           | ✅ Full control             |
| File System Access     | 🔸 Virtualized       | ✅ Full access              |
| Offline Use            | ❌ No                | ✅ Yes                      |
| Collaboration          | ✅ Easy via Drive    | 🔸 Requires Git/Sharing     |
| Package Management     | 🔸 Limited pip       | ✅ pip, conda, custom builds|

---

Use **Colab** when you want a fast, shareable, cloud-based solution. Use **VS Code** when you need performance, flexibility, and control over your computational environment.

## Working with Jupyter Notebooks in VS Code

1. Install the Python and Jupyter extensions in VS Code (VS code will promt you to do so on the first run of your `.ipynb`).
2. Open any `.ipynb` file directly and interact with it.
3. Run cells with the play button (`▶️`) or use shortcuts (`Shift+Enter`).
4. Switch between Markdown and Code cells using the cell type selector or a shortcut (`Ctrl+M M` for Markdown, `Ctrl+M Y` for Code).
5. View outputs like plots, tables, and printed values right inside the editor.

```{admonition} Tip for Beginners
:class: hint dropdown

Always restart the kernel and run all cells in order if you're unsure what state your notebook is in. This ensures that your variables and outputs are consistent.
```


