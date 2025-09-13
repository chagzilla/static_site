from textnode import TextType, TextNode
def main():
    t = TextNode("This is some anchor text", TextType.LINKS, "https://www.boot.dev")
    print(t)


if __name__ == "__main__":
    main()
