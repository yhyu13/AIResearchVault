import dearpygui.dearpygui as dpg
import os
import subprocess
import sys
import locale

bWin32 = sys.platform == "win32"

def run_cmd(cmd):
    print(cmd)
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=not bWin32) 
    return_code = result.returncode 
    stdout, stderr = result.stdout.decode(), result.stderr.decode() 
        
    if return_code == 0:
        print("Repo moved successfully!")
    else: 
        print("Script failed with return code ", return_code)
        print(stderr)

def move_repo(sender, data):
    repo_path = os.path.normpath(dpg.get_value("repo_path_input"))
    destination = os.path.normpath(dpg.get_value("destination_input"))
    move_submodules = dpg.get_value("move_submodules_checkbox")

    if not os.path.exists(destination):
        os.mkdir(destination)

    if move_submodules:
        for submodule in os.listdir(repo_path):
            if os.path.isdir(os.path.join(repo_path, submodule)):
                cmd = f"git mv \"{os.path.join(repo_path, submodule)}\" \"{destination}\""
                run_cmd(cmd)
    else:
        cmd = f"git mv \"{repo_path}\" \"{destination}\""
        run_cmd(cmd)

def write_to_textbox(textbox_id):
    def write(text):
        dpg.set_value(textbox_id, dpg.get_value(textbox_id) + text)
    return write

if __name__ == '__main__':
    
    system_cmd_encoding = locale.getpreferredencoding(False)
    print(f'system_cmd_encoding: {system_cmd_encoding}')

    dpg.create_context()
    dpg.create_viewport(title='Move Repo', width=800, height=600)

    with dpg.font_registry():
        with dpg.font(tag = 'CHN', file = './dpg/LXGWWenKai-Regular.ttf',
                        size = 12) as default_chn_font:
            # add the default font range
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)

    dpg.bind_font(default_chn_font)
    dpg.set_global_font_scale(1)

    with dpg.window(label="Move Repo", width=800, height=600) as primary_window:
        dpg.add_text("你好，世界！")  # Chinese text

        dpg.add_text("Enter repo path:")
        dpg.add_input_text(tag="repo_path_input", width=800)

        dpg.add_text("Contains Submodule?")
        dpg.add_checkbox(tag="move_submodules_checkbox")

        dpg.add_text("Enter destination path:")
        dpg.add_input_text(tag="destination_input", width=800)

        dpg.add_button(label="Move Repo", callback=move_repo)

        textbox_id = dpg.add_input_text(label="Output", multiline=True, height=200)
        sys.stdout.write = write_to_textbox(textbox_id)

    dpg.setup_dearpygui()

    dpg.show_viewport()
    dpg.set_primary_window(window=primary_window, value=True)

    dpg.start_dearpygui()

    dpg.destroy_context()
