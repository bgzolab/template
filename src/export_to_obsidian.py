from pickle import FALSE

import click
import os

from bangumi.client import BangumiClient
from bangumi.collection import get_all_collections_by_pages
from bangumi.enum import SubjectType, CollectionType
from cnblog.blog_post import get_cnblog_post_body_by_url
from cnblog.bookmark import get_bookmark_list
from utils.file_utils import output_content_to_file_path, get_clean_filename
from utils.md_utils import html_to_markdown_with_html2text, html_to_markdown_with_bs
from utils.template import WebPage
from utils.md_utils import dump_markdown_with_frontmatter
from bangumi.subject import get_subject_info, get_subject_character
from datetime import datetime

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

def bangumi_export(subject_type: int, collection_type: int, output_dir: str, template_path: str, force: bool = False):
    # NOTE: 暂时就导出游戏
    client = BangumiClient()
    username = client.get_user()['username']
    limit = 30
    offset = 0

    while True:
        results = get_all_collections_by_pages(
            username,
            subject_type,
            collection_type,
            limit=limit,
            offset=offset
        )
        if not results:
            break
        if len(results) == 0:
            break
        offset += limit
        for res in results:
            # print("get response=", res)
            try:
                if not write_bangumi_data_from_id(
                        subject_id=res.subject_id,
                        collection_type=collection_type,
                        output_dir=output_dir,
                        template_path=template_path,
                        force=force):
                    if not force:
                        return
            except Exception as e:
                print(f"跳过:{res.subject.name}, subject_id={res.subject_id}, error={e}")
            print(f"处理完成={res.subject_id}")


def write_bangumi_data_from_id(subject_id: int, collection_type: int, output_dir: str, template_path: str, force: bool = False) -> bool:
    # 1. 获取条目详情
    subject = get_subject_info(subject_id)
    if not subject:
        print(f"未获取到条目详情: {subject_id}")
        return True

    subject_type = subject.type_id
    subject_type_en = SubjectType.get_name_en(subject_type)
    collection_type_en = CollectionType.get_name_en(collection_type)
    tags = ['bangumi/'+collection_type_en, 'bangumi/' + subject_type_en]
    filename = str(subject_id) + "-" + get_clean_filename(subject.name_cn or subject.name or str(subject.id)) + '.md'
    output_path = os.path.join(output_dir, subject_type_en, filename)
    if os.path.exists(output_path) and not force:
        print(f"已存在，提前结束: {filename}")
        return False

    # 2. 读取模板内容
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 3. 渲染模板（这里只做简单替换，可根据需要扩展）
    # 你可以根据模板变量名和 subject 字段进行映射
    content = template
    content = content.replace('{{title}}', subject.name_cn or subject.name or "")
    content = content.replace('{{bangumi}}', str(subject.id))
    content = content.replace('{{cover}}', subject.images.medium if subject.images else "")
    content = content.replace('{{created}}', subject.date + datetime.now().strftime('T%H:%M:%S%z') or datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'))
    content = content.replace('{{modified}}', datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'))
    content = content.replace('{{rating}}', str(subject.rating.score) if subject.rating and subject.rating.score else "")
    content = content.replace('{{type}}', 'bangumi/' + subject_type_en)
    content = content.replace('{{aliases}}', subject.name)
    content = content.replace('{{tags}}', str(tags))
    content = content.replace('{{characters}}', get_output_character_string(subject_id))
    content = content.replace('{{summary}}', subject.summary or "")

    # 4. 写入文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # utils.file_utils.ensure_output_directory_exists()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"写入完成: {output_path}")
    return True


def get_output_character_string(subject_id: int) -> str:
    result = ""
    character_template = """### {}:{}

![]({})"""
    character_list = get_subject_character(subject_id)
    for character in character_list:
        if result != '':
            result += '\n\n'
        result += character_template.format(
            character.name,
            character.relation,
            character.images.medium if character.images else ""
        )

    return  result

@click.group()
def eto():
    pass

@eto.command()
@click.option('--output', '-o', required=True, help='输出目录')
def cnblog(output):
    cnblog_export(output)

@eto.command()
@click.option('--template', '-t', required=True, type=str, help='模板文件')
@click.option('--subject_type', '-s', required=True, type=int, help='主题类型')
@click.option('--output', '-o', required=True, help='输出目录')
@click.option('--collection_type', '-c', required=False, type=int, help='收藏类型')
@click.option('--force', required=False, is_flag=True, help='是否强制覆盖')
def bangumi(subject_type, collection_type, output, template, force):
    if collection_type:
        bangumi_export(subject_type, collection_type, output, template, force)
    else:
        sync_all_collection_under_subject_type(subject_type, output, template, force)

def sync_all_collection_under_subject_type(subject_type: int, output_dir: str, template_path: str, force: bool = False):
    collection_type_list = CollectionType.all()
    for collection_type in collection_type_list:
        print("正在处理: ", collection_type)
        bangumi_export(
            subject_type=subject_type,
            collection_type=collection_type.value,
            output_dir=output_dir,
            template_path=template_path,
            force=force
        )
        print("处理完成: ", collection_type)

if __name__ == '__main__':
    eto()
    # write_bangumi_data_from_id(
    #     subject_id=208754,
    #     collection_type=2,
    #     output_dir="output/bangumi",
    #     template_path="config/bangumi_template.md"
    # )
    # sync_all_collection_under_subject_type(
    #     subject_type=SubjectType.ANIME.value,
    #     output_dir="output/bangumi",
    #     template_path="config/bangumi_template.md"
    # )


