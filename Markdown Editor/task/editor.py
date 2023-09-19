class Formatter:
    def get_help(self):
        menu = """Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line
    Special commands: !help !done"""
        print(menu)

    def plain(self, raw_text: str) -> str:
        return raw_text

    def bold(self, raw_text: str) -> str:
        return f"**{raw_text}**"

    def italic(self, raw_text: str) -> str:
        return f"*{raw_text}*"

    def header(self, level: int, raw_text: str) -> str:
        return f"{'#' * level} {raw_text}"

    def link(self, label: str, url: str) -> str:
        return f"[{label}]({url})"

    def inline_code(self, raw_text: str) -> str:
        return f"`{raw_text}`"

    def ordered_list(self, elements: list) -> str:
        text = self.create_list(elements, is_ordered=True)
        return text

    def unordered_list(self, elements: list) -> str:
        text = self.create_list(elements, is_ordered=False)
        return text

    def create_list(self, elements: list, is_ordered: bool = True) -> str:
        text = ""
        if is_ordered:
            for index, element in enumerate(elements):
                text += f"{index + 1}. {element}\n"
        else:
            for _, element in enumerate(elements):
                text += f"* {element}\n"
        return text

    def new_line(self) -> str:
        return "\n"


def print_processed_lines(lines: list):
    for line in lines:
        print(line, end="")
    print()


def save_file(text: list):
    with open("output.md", "w", encoding="utf-8") as output_file:
        for line in text:
            output_file.write(line)


def main():
    formatter = Formatter()
    processed_text = []
    formatters = {
        "plain": formatter.plain,
        "bold": formatter.bold,
        "italic": formatter.italic,
        "header": formatter.header,
        "link": formatter.link,
        "inline-code": formatter.inline_code,
        "ordered-list": formatter.ordered_list,
        "unordered-list": formatter.unordered_list,
        "new-line": formatter.new_line,
    }
    is_done = False
    while not is_done:

        option = input("Choose a formatter: ")

        if option == "!help":
            formatter.get_help()
        elif option == "!done":
            save_file(processed_text)
            is_done = True
        elif option not in formatters:
            print("Unknown formatting type or command")
            continue
        else:
            match option:
                case "plain" | "bold" | "italic" | "inline-code":
                    raw_text = input("Text: ")
                    function = getattr(formatter, option.replace("-", "_"))
                    processed_text += function(raw_text)
                case "header":
                    correct_level = False
                    level: int
                    while not correct_level:
                        level = int(input("Level: "))
                        if level in range(1, 7):
                            correct_level = True
                        else:
                            print("The level should be within the range of 1 to 6")
                            continue
                    raw_text = input("Text: ")
                    if len(processed_text) == 0:
                        processed_text += f"{formatter.header(level, raw_text)}\n"
                    else:
                        processed_text += f"\n{formatter.header(level, raw_text)}\n"
                case "link":
                    label = input("Label: ")
                    url = input("URL: ")
                    processed_text += formatter.link(label, url)
                case "new-line":
                    processed_text += formatter.new_line()
                case "ordered-list" | "unordered-list":
                    correct_input = False
                    number_rows: int
                    while not correct_input:
                        number_rows = int(input("Number of rows: "))
                        if number_rows > 0:
                            correct_input = True
                        else:
                            print("The number of rows should be greater than zero")
                            continue
                    raw_text = [input(f"Row #{i}: ") for i in range(1, number_rows + 1)]
                    function_list = getattr(formatter, option.replace("-", "_"))
                    processed_text += function_list(raw_text)

            print_processed_lines(processed_text)


if __name__ == "__main__":
    main()
