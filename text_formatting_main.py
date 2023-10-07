from pynput.keyboard import Key, Controller, Listener
import time


keyboard = Controller()

seconds_wait = 8

print(f"*There is a file `cells_calculation.png` which shows what part of the table needs to be included in the calculation*")
num_cells = int(input("How many cells do you have? (You can calculate the number of cells by multiplying the number of columns by the number of rows): "))
print(f"Go to Word, put you cursor at the end of the last cell in the table and wait {seconds_wait} seconds :)")
time.sleep(seconds_wait)

keys_dict = {
    'alt_l': Key.alt_l,
    'shift_l': Key.shift_l,
    'end': Key.end,
    'page_down': Key.page_down,
    'ctrl': Key.ctrl,
    'tab': Key.tab
}


def press_and_release_keys(wanted_keys):
    for p_key in wanted_keys:  # `p_key` stands for "press key"
        if p_key in keys_dict.keys():
            keyboard.press(keys_dict[p_key])
        else:
            keyboard.press(p_key)

    for r_key in wanted_keys:  # `r_key` stands for "release key"
        if r_key in keys_dict.keys():
            keyboard.release(keys_dict[r_key])
        else:
            keyboard.release(r_key)


def write_quotation_mark(symbol, times):
    for p in range(times):
        keyboard.press(symbol)
        keyboard.release(symbol)
        press_and_release_keys(['ctrl', 'z'])


for i in range(num_cells):
    write_quotation_mark("'", 1)

    press_and_release_keys(['shift_l', 'end'])
    keyboard.press(Key.left)
    keyboard.press(Key.left)

    write_quotation_mark("'", 1)

    if i == num_cells - 1:
        break

    press_and_release_keys(['shift_l', 'tab'])
    keyboard.press(Key.right)
    keyboard.release(Key.right)


# This selects the row
press_and_release_keys(['alt_l', 'shift_l', 'end'])

# This selects the whole table (firstly we need to select the row so we can select the whole table)
press_and_release_keys(['alt_l', 'shift_l', 'page_down'])

# This copies the table
press_and_release_keys(['ctrl', 'c'])


copied_table_list = []
print("Paste the result here (`ctrl` + `v`): ")

while True:
    text_line = input()

    if text_line == "":
        break

    copied_table_list.append(text_line)

new_list_copied_table = []
for line in copied_table_list:
    line = line.replace("\t", "$$$$$")
    new_list_copied_table.append(line.split("$$$$$"))

print("\nResult:\n")

for i in range(len(new_list_copied_table)):
    row = new_list_copied_table[i]
    row_result_as_str = "("

    for j in range(len(row)):
        current_element = row[j]
        el_without_quotes = current_element[1:len(current_element) - 1]

        if el_without_quotes == "NULL" or \
            (el_without_quotes.isdigit() and el_without_quotes[0] != '0') or \
                (el_without_quotes.replace(".", "", 1).isdigit() and el_without_quotes.count(".") < 2 and el_without_quotes[0] != '0'):
            row_result_as_str += f"{el_without_quotes}"
        else:
            row_result_as_str += current_element

        if j != len(row) - 1:
            row_result_as_str += ", "

    if i == len(new_list_copied_table) - 1:
        row_result_as_str += ");"
    else:
        row_result_as_str += "), "

    print(row_result_as_str)

print("\nPress `Esc` to finish the program.\n")


def on_release(key):
    if key == Key.esc:
        print("Program finished successfully!")
        listener.stop()
        raise SystemExit


with Listener(on_release=on_release) as listener:
    listener.join()
