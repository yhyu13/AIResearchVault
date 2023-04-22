import dearpygui.dearpygui as dpg
import os
import subprocess
import sys
import locale
import pickle
import re

class MyState:
    def __init__(self, proxy, url, dir, name):
        self.proxy = proxy
        self.url = url
        self.dir = dir
        self.name = name

    def __str__(self):
        return f"proxy: {self.proxy}, url: {self.url}, dir: {self.dir}, name: {self.name}"
    
    def load(self):
        script_name = os.path.basename(__file__)
        pickle_file = f"./dpg/{script_name}.pickle"
        # load the object from the file using pickle
        if os.path.exists(pickle_file):
            # yuhang : only overload attribute that exists
            for attr, value in pickle.load(open(pickle_file, 'rb')).__dict__.items():
                if hasattr(self, attr):
                    print(f'Reload app state {attr} : {value}')
                    setattr(self, attr, value)
                    
    def dump(self):
        script_name = os.path.basename(__file__)
        pickle_file = f"./dpg/{script_name}.pickle"
        # dump the object to the file using pickle
        pickle.dump(self, open(pickle_file, 'wb'))

# create an instance of MyState
my_state = MyState("http://127.0.0.1:8889", "https://example.com", "/path/to/dir", "example.pdf")  
bWin32 = sys.platform == "win32"

def run_curl_pdf(sender, data):
    if bWin32:
        # Windows
        ext = ".bat"
    else:
        # Unix-like
        ext = ".sh"

    proxy = dpg.get_value("proxy_input")
    url = dpg.get_value("url_input")
    if not url.endswith('.pdf'):
        print(f'{url} does not ends with .pdf!')
        return
    pdf_dir = dpg.get_value("pdf_dir")
    pdf_filename = dpg.get_value("pdf_input")
    pdf_filename = remove_invalid_chars(pdf_filename)
    pdf = os.path.join(pdf_dir, pdf_filename)
    if not pdf.endswith('.pdf'):
        pdf += '.pdf'
        
    my_state.proxy = proxy
    my_state.url = url
    my_state.dir = pdf_dir
    my_state.name = pdf_filename

    curl_path = "C:\Windows\System32\curl.exe" if bWin32 else "curl"

    cmd = f'''{curl_path} -o "{pdf}" "{url}"'''
    if proxy != '':
        cmd += f''' -x "{proxy}"'''
    cmd = cmd.replace("\\", "/")
    print(f'Run \n cmd: {cmd}')
    
    dpg.set_value("cmd_out", cmd)

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=not bWin32) 
    return_code = result.returncode 
    stdout, stderr = result.stdout.decode(), result.stderr.decode() 
    
    if return_code == 0:
        print("Script succeeded")

        pdf_size = os.path.getsize(pdf)
        if pdf_size > 500:
            print(f"PDF file size is above 500B, pdf_size: {pdf_size}B!")
        else:
            print(f"Warning : PDF file size is below 500B, pdf_size: {pdf_size}B")
    else:
        print("Script failed with return code ", return_code)
        print(stderr)
        print("Standard output:")
        print(stdout)


def remove_invalid_chars(filename):
    # Define a regular expression pattern to match invalid characters
    pattern = r'[\\/*?:"<>|()]'

    # Replace all invalid characters with an underscore
    return re.sub(pattern, '_', filename)

def write_to_textbox(textbox_id):
    def write(text):
        dpg.set_value(textbox_id, dpg.get_value(textbox_id) + text)
    return write

if __name__ == '__main__':

    my_state.load()

    system_cmd_encoding = locale.getpreferredencoding(False)
    print(f'system_cmd_encoding: {system_cmd_encoding}')

    dpg.create_context()
    dpg.create_viewport(title='AI Research Vault', width=800, height=400)

    with dpg.font_registry():
        with dpg.font(tag = 'CHN', file = './dpg/LXGWWenKai-Regular.ttf',
                        size = 12) as default_chn_font:
            # add the default font range
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)

    dpg.bind_font(default_chn_font)
    dpg.set_global_font_scale(1)

    with dpg.window(label="PDF Downloader", width=800, height=200) as primary_window:
        dpg.add_text("你好，世界！")  # Chinese text
        
        dpg.add_text("Enter Proxy:")
        dpg.add_input_text(tag="proxy_input", width=800, default_value=my_state.proxy)

        dpg.add_text("Enter URL:")
        dpg.add_input_text(tag="url_input", width=800, default_value=my_state.url)

        dpg.add_text("Enter PDF directory:")
        dpg.add_input_text(tag="pdf_dir", width=800, default_value=my_state.dir)

        dpg.add_text("Enter PDF file name:")
        dpg.add_input_text(tag="pdf_input", width=800, default_value=my_state.name)
        
        dpg.add_text("Cmd:")
        dpg.add_input_text(tag="cmd_out", width=800)

        dpg.add_button(label="Download PDF", callback=run_curl_pdf)

        textbox_id = dpg.add_input_text(label="Output", multiline=True, height=200)
        sys.stdout.write = write_to_textbox(textbox_id)


    dpg.setup_dearpygui()

    dpg.show_viewport()
    dpg.set_primary_window(window=primary_window, value=True)

    dpg.start_dearpygui()

    dpg.destroy_context()

    # save the object to a file using pickle
    my_state.dump()

