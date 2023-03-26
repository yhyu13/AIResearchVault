import dearpygui.dearpygui as dpg
import os
import subprocess
import sys

def run_curl_pdf(sender, data):
    if sys.platform == "win32":
        # Windows
        ext = ".bat"
    else:
        # Unix-like
        ext = ".sh"

    url = dpg.get_value("url_input")
    pdf = os.path.join(dpg.get_value("pdf_dir"), dpg.get_value("pdf_input"))
    if not pdf.endswith('.pdf'):
        pdf += '.pdf'

    print(f'Run \n url:{url}\n pdf:{pdf}')

    result = subprocess.run([os.path.join(os.getcwd(), f"curl_pdf{ext} {url} \"{pdf}\"")], capture_output=True, shell=True)
    if result.returncode == 0:
        print("Script succeeded")
    else:
        print("Script failed with return code", result.returncode)
        print(result.stderr)


def write_to_textbox(textbox_id):
    def write(text):
        dpg.set_value(textbox_id, dpg.get_value(textbox_id) + text)
    return write


dpg.create_context()
dpg.create_viewport(title='AI Research Vault', width=800, height=400)

with dpg.window(label="PDF Downloader", width=800, height=200) as primary_window:
    dpg.add_text("Enter URL:")
    dpg.add_input_text(tag="url_input", width=800)

    dpg.add_text("Enter PDF directory:")
    dpg.add_input_text(tag="pdf_dir", width=800)

    dpg.add_text("Enter PDF file name:")
    dpg.add_input_text(tag="pdf_input", width=800)

    dpg.add_button(label="Download PDF", callback=run_curl_pdf)

    textbox_id = dpg.add_input_text(label="Output", multiline=True, height=200)
    sys.stdout.write = write_to_textbox(textbox_id)


dpg.setup_dearpygui()

dpg.show_viewport()
dpg.set_primary_window(window=primary_window, value=True)

dpg.start_dearpygui()

dpg.destroy_context()

