import click
from cnblog.blog_post import get_cnblog_post_body_by_url
from cnblog.bookmark import get_bookmark_list
from utils.file_utils import output_content_to_file_path, get_clean_filename
from utils.md_utils import html_to_markdown_with_html2text, html_to_markdown_with_bs
from utils.template import WebPage
from utils.md_utils import dump_markdown_with_frontmatter
import os


# CNBLOG 博客园
def cnblog_export(output_dir):
    page_index = 1
    page_size = 100
    while True:
        bookmarks = get_bookmark_list(page_index, page_size)
        if not bookmarks:
            break
        for bm in bookmarks:
            filename = get_clean_filename(bm.Title)
            file_path = os.path.join(output_dir, f"~{filename}.md")
            if os.path.exists(file_path):
                print(f"已存在，提前结束: {filename}.md")
                return  # 剪枝，提前退出
            if bm.FromCNBlogs:
                webpage = WebPage(
                    title=bm.Title,
                    source=bm.LinkUrl,
                    created=bm.DateAdded,
                    modified=bm.DateAdded,
                    type="archive-web"
                )

                md = dump_markdown_with_frontmatter(
                    webpage.__dict__,
                    html_to_markdown_with_bs(
                        get_cnblog_post_body_by_url(bm.LinkUrl)
                    )
                )
                output_content_to_file_path(
                    output_dir,
                    filename,
                    md,
                    "md")

                print(f"Done: {bm.Title}")
            else:
                print(f"Skip: {bm.Title}")
        page_index += 1

@click.command()
@click.argument('method')
@click.option('--output', '-o', required=True, help='输出目录')
def eto(method, output):
    if method == 'cnblog':
        cnblog_export(output)
    else:
        print(f"未知方法: {method}")

if __name__ == '__main__':
    eto()
