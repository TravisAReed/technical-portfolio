def terminal_fg(text, hex_color): #hex color is the string for example white "FFFFFF"
    """
    Color only the font/text in the terminal.
    hex_color should look like 'FFA500'.
    """
    hex_color = hex_color.replace("#", "")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

#color gets saved in string
# s = f"hello: {terminal_fg("colorful world", "00FF00")}"
# print(s)

# print(print(
#     f"hello: {terminal_fg("colorful world", "00FF00")}",
#     flush=True
# ))