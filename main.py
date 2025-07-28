from cnblog.blog_post import get_cnblog_post_body_by_url
from cnblog.bookmark import get_bookmark_list
from utils.file_utils import output_content_to_file_path, get_clean_filename
from utils.md_utils import html_to_markdown_with_html2text, html_to_markdown_with_bs
from utils.template import WebPage
from utils.md_utils import dump_markdown_with_frontmatter


# CNBLOG 博客园
def cnblog_export():
    bookmarks = get_bookmark_list()
    for bm in bookmarks:
        if bm.FromCNBlogs:
            webpage = WebPage(
                title=bm.Title,
                source=bm.LinkUrl,
                created=bm.DateAdded,
                modified=bm.DateAdded,
                type="archive-web"
            )

            md = dump_markdown_with_frontmatter(webpage.__dict__,
                                                    html_to_markdown_with_bs(
                                                        get_cnblog_post_body_by_url(bm.LinkUrl)
                                                    )
                                                )
            output_content_to_file_path(
                get_clean_filename(bm.Title), md, "md")

            print(f"Done: {bm.Title}")
            # utils.md_utils.html_to_markdown_with_html2text(bm.url)
        else:
            print(f"Skip: {bm.Title}")


if __name__ == '__main__':
    try:
        cnblog_export()
    except Exception as e:
        print(f"An error occurred: {e}")
