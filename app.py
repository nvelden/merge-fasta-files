from shiny.express import input, render, ui
from shiny import reactive
from utils import remove_duplicate_fasta_entries
import pandas

# UI
ui.busy_indicators.use(spinners=True, pulse=True, fade=True)
ui.input_file(
    "fasta_files", 
    "Upload FASTA files:", 
    multiple=True, 
    width="100%", 
    accept=".fa, .fasta, .faa, .fna"
)

ui.input_checkbox(
    "remove_duplicates", 
    "Remove duplicate entries", 
    value=True
)

@render.download(filename="merged.fasta")
def download_fasta():
    files = input.fasta_files()
    if not files:
        ui.notification_show("No FASTA files uploaded.", type="error")
        return

    output = []
    for info in files:
        with open(info["datapath"], "r") as f:
            content = f.read()
        output.append(content)

    merged = "\n\n".join(output)

    if input.remove_duplicates():
        merged, removed = remove_duplicate_fasta_entries(merged)
        if removed > 0:
            ui.notification_show(f"{removed} duplicate sequence(s) removed.", type="warning")

    yield merged



# @reactive.effect
# def _():
#     ui.update_action_link("download_fasta", label="busy")

# @render.code
# @reactive.event(input.merge)
# def txt():
#     files = input.fasta_files()
#     if not files:
#         return "# No FASTA files uploaded."

#     output = []
#     for info in files:
#         with open(info["datapath"], "r") as f:
#             content = f.read()
#         output.append(content)

#     merged = "\n\n".join(output)

#     if input.remove_duplicates():
#         merged = remove_duplicate_fasta_entries(merged)

#     return merged

# Reactive value to track processing state
