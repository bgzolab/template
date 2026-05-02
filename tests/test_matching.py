from __future__ import annotations

from venera_parser_bangumi.models import BangumiSubject, SyncCandidate
from venera_parser_bangumi.sync.candidates import build_search_request
from venera_parser_bangumi.sync.matching import match_search_result


def make_request(title: str = "海贼王"):
    candidate = SyncCandidate(
        source_table="Doing",
        target_state="doing",
        record_id="1",
        name=title,
        author="尾田荣一郎",
        subject_type=0,
        tags=["热血"],
        translated_tags=["冒险"],
    )
    return build_search_request(candidate)


def test_match_search_result_returns_matched_for_single_exact_hit() -> None:
    request = make_request()
    result = match_search_result(request, [BangumiSubject(1, "ONE PIECE", "海贼王")])

    assert result.status == "matched"
    assert result.subject is not None
    assert result.subject.subject_id == 1


def test_match_search_result_returns_no_result_for_empty_hits() -> None:
    request = make_request()
    result = match_search_result(request, [])

    assert result.status == "skipped_no_result"


def test_match_search_result_returns_ambiguous_for_multiple_exact_hits() -> None:
    request = make_request()
    result = match_search_result(
        request,
        [BangumiSubject(1, "海贼王"), BangumiSubject(2, "ONE PIECE", "海贼王")],
    )

    assert result.status == "skipped_ambiguous"
    assert len(result.candidate_subjects) == 2


def test_match_search_result_reports_ambiguous_for_duplicate_exact_bangumi_titles() -> None:
    request = make_request("泛而不精的我被逐出了勇者队伍")
    result = match_search_result(
        request,
        [
            BangumiSubject(
                352968,
                "勇者パーティを追い出された器用貧乏 ～パーティ事情で付与術士をやっていた剣士、万能へと至る～",
                "泛而不精的我被逐出了勇者队伍",
            ),
            BangumiSubject(
                367518,
                "勇者パーティを追い出された器用貧乏 ～パーティ事情で付与術士をやっていた剣士、万能へと至る～",
                "泛而不精的我被逐出了勇者队伍",
            ),
        ],
    )

    assert result.status == "skipped_ambiguous"
    assert [subject.subject_id for subject in result.candidate_subjects] == [352968, 367518]


def test_match_search_result_reports_no_result_when_only_cross_script_title_exists() -> None:
    request = make_request("Clevatess - 魔獸之王與嬰兒與屍之勇者")
    result = match_search_result(
        request,
        [
            BangumiSubject(
                312835,
                "クレバテス -魔獣の王と赤子と屍の勇者-",
                "Clevatess -魔兽之王与婴儿与尸之勇者",
            )
        ],
    )

    assert result.status == "matched"
    assert result.subject is not None
    assert result.subject.subject_id == 312835


def test_match_search_result_reports_ambiguous_for_simplified_traditional_punctuation_variants() -> None:
    request = make_request("再見龍生你好人生")
    result = match_search_result(
        request,
        [
            BangumiSubject(171069, "さようなら竜生、こんにちは人生", "再见龙生，你好人生"),
            BangumiSubject(235408, "さようなら竜生、こんにちは人生", "再见龙生，你好人生"),
            BangumiSubject(27427, "DRAGON BALL (42)"),
            BangumiSubject(445260, "再見！皮諾丘～雙子物語～", "再见！皮诺丘～双子物语～"),
            BangumiSubject(115815, "篠原千絵傑作集 (2) 目撃者にさようなら"),
            BangumiSubject(152643, "さよならパーフェクト", "再見，完美的我們"),
            BangumiSubject(237758, "さよならバイバイ", "再見Byebye"),
            BangumiSubject(367055, "グッバイ・フライデー", "再見‧星期五"),
            BangumiSubject(499432, "Kylooe 3 再見微笑"),
            BangumiSubject(595059, "意外事件之再見愛 (上)"),
        ],
    )

    assert result.status == "skipped_ambiguous"
    assert [subject.subject_id for subject in result.candidate_subjects] == [171069, 235408]


def test_match_search_result_matches_alias_token_variant() -> None:
    request = make_request("SPYXFAMILY 間諜過家家")
    result = match_search_result(
        request,
        [
            BangumiSubject(279379, "SPY×FAMILY", "间谍过家家"),
            BangumiSubject(637171, "妹よ、その侯爵家令息は間諜です"),
        ],
    )

    assert result.status == "matched"
    assert result.subject is not None
    assert result.subject.subject_id == 279379


def test_match_search_result_avoids_false_positive_for_unrelated_partial_titles() -> None:
    request = make_request("黃泉的使者")
    result = match_search_result(
        request,
        [
            BangumiSubject(448305, "让一让，你挡了我的黄泉路", "让一让，你挡了我的黄泉路"),
            BangumiSubject(598574, "浮生夢之黃泉", "浮生梦之黄泉"),
            BangumiSubject(318656, "六仙卷二：冥府黃泉一遊禁止攜帶危險物品"),
        ],
    )

    assert result.status == "skipped_no_result"
    assert result.candidate_subjects == []