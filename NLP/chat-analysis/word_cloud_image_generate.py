import matplotlib.pyplot as plt
from wordcloud import WordCloud




def create_wordcloud_image(params):
    wordcloud = WordCloud(
        width=params["image_width"],
        height=params["image_height"],
        background_color=params["img_background_color"],
        colormap=params["text_color_map"],
        max_words=params["max_words"],
        scale=params["scale"]
    ).generate(params["generate_text"])

    fig, ax = plt.subplots(figsize=params["figsize"])

    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    fig.savefig(
        params["file_name"] + ".png",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
        facecolor=params["img_background_color"]
    )

    plt.show()
    plt.close(fig)