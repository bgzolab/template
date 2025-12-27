from pickle import FALSE

import click
import os

from bangumi.client import BangumiClient
from bangumi.collection import get_all_collections_by_pages
from bangumi.enum import SubjectType, CollectionType
from cnblog.blog_post import get_cnblog_post_body_by_url
from cnblog.bookmark import get_bookmark_list
from qireader.getext import get_html_text_from_url
from utils.file_utils import output_content_to_file_path, get_clean_filename
from utils.md_utils import html_to_markdown_with_html2text, html_to_markdown_with_bs
from utils.template import WebPage
from utils.md_utils import dump_markdown_with_frontmatter
from bangumi.subject import get_subject_info, get_subject_character
from datetime import datetime

from v2ex.mytopic import get_fav_list_topic_id_page
from v2ex.topic import get_v2ex_topic_info
from weibo.like import get_weibo_like_list
from zhihu.collection import get_collection_page


# CNBLOG 博客园
def cnblog_export(output_dir):
    page_index = 1
    page_size = 100
    result_index = ""
    while True:
        bookmarks = get_bookmark_list(page_index, page_size)
        if not bookmarks:
            break
        for bm in bookmarks:
            filename = get_clean_filename(bm.Title)
            file_path = os.path.join(output_dir, f"~{filename}.md")
            if os.path.exists(file_path):
                print(f"已存在，提前结束: {filename}.md")
                print("输出index:\n", result_index)
                return  # 剪枝，提前退出
            if bm.FromCNBlogs:
                webpage = WebPage(
                    comments=True,
                    draft=True,
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
            result_index += f'\n- [[~{filename}|{bm.Title}]]'
        page_index += 1
    print("输出index:\n", result_index)

def bangumi_export(subject_type: int, collection_type: int, output_dir: str, template_path: str, force: bool = False):
    client = BangumiClient()
    username = client.get_user()['username']
    limit = 30
    offset = 0
    result_index = ""

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
                result, filename, title = write_bangumi_data_from_id(
                    subject_id=res.subject_id,
                    collection_type=collection_type,
                    output_dir=output_dir,
                    template_path=template_path,
                    force=force)
                if result:
                    result_index += f'\n- [[{filename}|{title}]]'
                elif not force:
                    print(f"写入失败: {filename}")
                    print("输出index\n", result_index)
                    return
            except Exception as e:
                print(f"跳过:{res.subject.name}, subject_id={res.subject_id}, error={e}")
            print(f"处理完成={res.subject_id}")
    print("输出index\n", result_index)


def write_bangumi_data_from_id(subject_id: int, collection_type: int, output_dir: str, template_path: str, force: bool = False) -> (bool, str, str):
    # 1. 获取条目详情
    subject = get_subject_info(subject_id)
    if not subject:
        print(f"未获取到条目详情: {subject_id}")
        # 当前条目可能有问题，不能影响后续的导出执行，需要跳过
        return True, '', ''

    subject_type = subject.type_id
    subject_type_en = SubjectType.get_name_en(subject_type)
    collection_type_en = CollectionType.get_name_en(collection_type)
    tags = ['bangumi/'+collection_type_en, 'bangumi/' + subject_type_en]
    # 处理别名
    aliases_set = { subject.name }
    website_set = set() # {}
    if subject.name_cn:
        aliases_set.add(subject.name_cn)
    # if subject.infobox:
    #     for item in subject.infobox:
    #         if item['key'] == '别名':
    #             for v in item['value']:
    #                 if v['v'] != '':
    #                     aliases_set.add(v['v'])

    if subject.infobox:
        for item in subject.infobox:
            # 添加官方网站1
            website_set.update(
                parse_infobox_value(item) if item.get("key") == "官方网站" else []
            )
            # 添加官方网站2
            website_set.update(
                parse_infobox_value(item) if item.get("key") == "website" else []
            )
            # 更新别名
            aliases_set.update(
                parse_infobox_value(item) if item.get("key") == "别名" else []
            )
    created_date = (subject.date or datetime.now().strftime('%Y-%m-%d')) + datetime.now().strftime('T%H:%M:%S%z')
    filename = str(subject_id) + "-" + get_clean_filename(subject.name_cn or subject.name or str(subject.id)) + '.md'
    output_path = os.path.join(output_dir, subject_type_en, filename)
    if os.path.exists(output_path) and not force:
        print(f"已存在，提前结束: {filename}")
        return False, '', ''

    # 2. 读取模板内容
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # 3. 渲染模板（这里只做简单替换，可根据需要扩展）
    # 你可以根据模板变量名和 subject 字段进行映射
    content = template
    title = subject.name_cn or subject.name or ""
    content = content.replace('{{tags}}', str(tags))
    content = content.replace('{{aliases}}', str(list(aliases_set)))
    content = content.replace('{{website}}', str(list(website_set)))
    content = content.replace('{{title}}', title)
    content = content.replace('{{bangumi}}', str(subject.id))
    content = content.replace('{{cover}}', subject.images.medium if subject.images else "")
    content = content.replace('{{created}}', created_date)
    content = content.replace('{{modified}}', datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'))
    content = content.replace('{{rating}}', str(subject.rating.score) if subject.rating and subject.rating.score else "")
    content = content.replace('{{type}}', 'bangumi/' + subject_type_en)
    content = content.replace('{{characters}}', get_output_character_string(subject_id))
    content = content.replace('{{summary}}', subject.summary or "")

    # 4. 写入文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # utils.file_utils.ensure_output_directory_exists()
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"写入完成: {output_path}")
    return True, filename, title


def parse_infobox_value(item):
    value = item.get("value")
    if isinstance(value, str):
        # 直接返回字符串
        return [value]
    elif isinstance(value, list):
        # 提取每个字典的 'v' 字段
        return [v.get("v") for v in value if isinstance(v, dict) and "v" in v]
    else:
        # 其他类型，返回空列表或自定义处理
        return []

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

@eto.command()
@click.option('--tag', '-t', required=True, type=str, help='收藏夹ID')
@click.option('--output', '-o', required=True, help='输出目录')
def qireader(tag, output):
    from qireader.readlatter import get_list_from_read_latter
    older_than = None
    result_index = "";

    while True:
        entries = get_list_from_read_latter(tag, older_than)
        if not entries:
            break

        for entry in entries:
            filename = get_clean_filename(entry.title)
            file_path = os.path.join(output, f"~{filename}.md")
            if os.path.exists(file_path):
                print(f"已存在: {filename}.md，同步结束")
                print("导出index\n", result_index)
                return

            timestamp_seconds = int(entry.timestamp) / 1_000_000_000
            webpage = WebPage(
                comments=True,
                draft=True,
                title=entry.title,
                source=entry.url,
                created=datetime.fromtimestamp(timestamp_seconds).strftime('%Y-%m-%dT%H:%M:%S%z'),
                modified=datetime.fromtimestamp(timestamp_seconds).strftime('%Y-%m-%dT%H:%M:%S%z'),
                type="archive-web"
            )
            # 尝试获取内容
            content = ''
            try:
                content = html_to_markdown_with_html2text(get_html_text_from_url(entry.url))
            except Exception as e:
                print(f"处理{filename}的全文时候发生异常，源地址可以已经删除，直接跳过，请手动处理！")

            md = dump_markdown_with_frontmatter(
                webpage.__dict__,
                content,
            )
            output_content_to_file_path(
                output,
                filename,
                md,
                "md")

            print(f"Done: {entry.title}")
            result_index += f'\n- [[~{filename}|{entry.title}]]'
        older_than = str(entries[-1].timestamp)
    # 容错处理
    print("导出index\n", result_index)

@eto.command()
@click.option('--output', '-o', required=True, help='输出目录')
def v2ex(output):
    result_index = "";
    page = 1
    while True:
        id_list = get_fav_list_topic_id_page(page)
        if not id_list or len(id_list) == 0:
            break
        page = page + 1
        for id in id_list:
            result = get_v2ex_topic_info(id)
            if not result:
                continue
            topic = result.result
            filename = get_clean_filename(str(id) + '-' + topic.title)
            file_path = os.path.join(output, f"~{filename}.md")
            if os.path.exists(file_path):
                print(f"已存在: {filename}.md，同步结束")
                print("导出index\n", result_index)
                return
            created_time = datetime.fromtimestamp(topic.created).strftime('%Y-%m-%dT%H:%M:%S%z')
            modified_time = datetime.fromtimestamp(topic.last_modified).strftime('%Y-%m-%dT%H:%M:%S%z')
            webpage = WebPage(
                comments=True,
                draft=True,
                title=topic.title,
                source=topic.url,
                created=created_time,
                modified=modified_time,
                type="archive-web"
            )
            md = dump_markdown_with_frontmatter(
                webpage.__dict__,
                topic.content
            )
            output_content_to_file_path(
                output,
                filename,
                md,
                "md")

            print(f"Done: {topic.title}")
            result_index += f'\n- [[~{filename}|{topic.title}]]'
    print("导出完成index\n", result_index)

@eto.command()
@click.option('--collection', '-c', required=True, help='收藏夹')
@click.option('--output', '-o', required=True, help='输出目录')
def zhihu(collection, output):
    result_index = "";
    offset = 0
    limit = 20

    while True:
        page = get_collection_page(collection, offset, limit)
        # 处理当前页的数据
        for c in page.data:
            content = c.content
            article = ''
            title = ''
            id = content.id
            if isinstance(content.content, list):
                # 想法
                title = c.content.content[0]['title']
                article = content.content[0]['content']
            else:
                title = content.title or content.question.title
                article = content.content

            filename = get_clean_filename( id + "-" + title)
            file_path = os.path.join(output, f"~{filename}.md")
            if os.path.exists(file_path):
                print(f"已存在: {filename}.md，同步结束")
                print("导出index\n", result_index)
                return

            created_time = datetime.fromtimestamp(content.created_time).strftime('%Y-%m-%dT%H:%M:%S%z')
            modified_time = datetime.fromtimestamp(content.updated_time).strftime('%Y-%m-%dT%H:%M:%S%z')
            webpage = WebPage(
                comments=True,
                draft=True,
                title=title,
                source=content.url,
                created=created_time,
                modified=modified_time,
                type="archive-web"
            )
            md = dump_markdown_with_frontmatter(
                webpage.__dict__,
                html_to_markdown_with_html2text(article)
            )
            output_content_to_file_path(
                output,
                filename,
                md,
                "md")

            print(f"Done: {title}")
            result_index += f'\n- [[~{filename}|{title}]]'


        if page.data is None or len(page.data) == 0:
            break
        offset += limit

    print(f"输出index:\n{result_index}")


'''
获取微博图片链接

TODO 下载图片
'''
def handle_weibo_pic(item) -> str:
    if item.pic_num is None or item.pic_num == 0 or item.pic_ids is None or len(item.pic_ids) == 0 :
        return ""
    result = ""
    pic_infos = item.pic_infos
    for pic_id in item.pic_ids:
        pic_info = pic_infos[pic_id]
        url = pic_info.largest['url']
        result += f"![{pic_id}]({url})\n\n"
    return result

# @eto.command()
# @click.option('--uid', '-u', required=True, help='用户ID')
# @click.option('--output', '-o', required=True, help='输出目录')
def weibo(uid: int, output: str):
    result_index = "";
    page_index = 1
    while True:
        page = get_weibo_like_list(uid, page_index)
        if page is None:
            print("获取微博喜欢列表失败，请检查接口")
            break

        if page.ok == 1:
            list = page.data.list
            if len(list) == 0:
                break

            for item in list:
                post_id = item.mblogid
                post_user = item.user.id
                post_url = f"https://weibo.com/{post_user}/{post_id}"
                filename = f"{post_user}-{post_id}"

                auther_name = item.user.screen_name
                context_digest = get_clean_filename(item.text_raw[:10])
                title = auther_name + ":" + context_digest

                created_at_str = item.created_at
                article_html = item.text

                # %a: 缩写星期 (Wed)
                # %b: 缩写月份 (Dec)
                # %d: 日期 (24)
                # %H:%M:%S: 时间 (04:08:45)
                # %z: 时区偏移 (+0800)
                # %Y: 年份 (2025)
                dt_obj = datetime.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")
                webpage = WebPage(
                    comments=True,
                    draft=True,
                    title=title,
                    source=post_url,
                    created=dt_obj.strftime("%Y-%m-%dT%H:%M:%S"),
                    modified=dt_obj.strftime("%Y-%m-%dT%H:%M:%S"),
                    type="archive-web"
                )
                md = dump_markdown_with_frontmatter(
                    webpage.__dict__,
                    html_to_markdown_with_html2text(article_html) + handle_weibo_pic(item)
                )
                output_content_to_file_path(
                    output,
                    filename,
                    md,
                    "md")

                print(f"Done: {title}")
                result_index += f'\n- [[~{filename}|{title}]]'
            page_index += 1

        else:
            print("获取微博喜欢列表失败，请检查接口")
            break

    print(f"输出index:\n{result_index}")


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
    # eto()

    # v2ex("output/v2ex")
    # zhihu(908297073, "output/zhihu")
    # write_bangumi_data_from_id(
    #     subject_id=334105,
    #     collection_type=2,
    #     output_dir="output/bangumi",
    #     template_path="config/bangumi_template.md"
    # )
    # sync_all_collection_under_subject_type(
    #     subject_type=SubjectType.ANIME.value,
    #     output_dir="output/bangumi",
    #     template_path="config/bangumi_template.md"
    # )
    # qireader('tag-xxx', "output/qireader")

    weibo(8221250887, "output/weibo")
