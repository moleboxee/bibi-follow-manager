# -*- coding: utf-8 -*-
"""核心逻辑单元测试(无第三方依赖,直接运行):

    python tests/test_core.py

覆盖:WBI 签名(官方文档测试向量)、变化归因、风控离线回退、
快照写入、历史合并、Cookie 解析、注销识别、版本比较。
"""
import hashlib
import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import time

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "bibi", HERE.parent / "bibi_follow_manager.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# 把所有本地数据文件指到临时目录,避免污染程序目录
TMP = tempfile.mkdtemp(prefix="bibi_test_")
m.DATA_FILE = os.path.join(TMP, "data.json")
m.SNAPSHOT_FILE = os.path.join(TMP, "snapshot.json")
m.OPS_FILE = os.path.join(TMP, "ops.json")
m.HISTORY_FILE = os.path.join(TMP, "history.json")
m.ACTIVITY_FILE = os.path.join(TMP, "activity.json")
m.CACHE_FILE = os.path.join(TMP, "cache.json")

RESULTS = []


def test(fn):
    RESULTS.append((fn.__name__, fn, None))
    return fn


# ---------- WBI 签名(bilibili-API-collect 文档官方测试向量) ----------
IMG_KEY = "7cd084941338484aae1ad9425b84077c"
SUB_KEY = "4932caff0ff746eab6f01bf08b70ac45"
MIXIN_EXPECT = "ea1db124af3c7062474693fa704f4ff8"


@test
def wbi_mixin_key_matches_official_vector():
    raw = IMG_KEY + SUB_KEY
    got = m.derive_mixin_key(raw)
    assert got == MIXIN_EXPECT, "mixin_key 不匹配: %s" % got


@test
def wbi_sign_official_vector():
    b = m.Bili()
    b._mixin_key = lambda: MIXIN_EXPECT  # 固定 mixin,避免网络请求
    real_time = time.time
    try:
        time.time = lambda: 1702204169.0  # 文档示例的 wts
        p = b.wbi_sign({"foo": 114, "bar": 514, "zab": 1919810})
    finally:
        time.time = real_time
    assert p["wts"] == "1702204169", p
    # 文档:按键名升序排列 → bar=514&foo=114&wts=1702204169&zab=1919810
    q = "bar=514&foo=114&wts=1702204169&zab=1919810"
    assert p["w_rid"] == hashlib.md5((q + MIXIN_EXPECT).encode()).hexdigest(), p


@test
def wbi_sign_filters_special_chars_and_encodes_space():
    b = m.Bili()
    b._mixin_key = lambda: MIXIN_EXPECT
    real_time = time.time
    try:
        time.time = lambda: 1702204169.0
        p = b.wbi_sign({"q": "a b!c(d)e"})
    finally:
        time.time = real_time
    # !'()* 被过滤 → "a bcde";查询串中空格编码为 %20(大写十六进制)
    q = "q=a%20bcde&wts=1702204169"
    assert p["w_rid"] == hashlib.md5((q + MIXIN_EXPECT).encode()).hexdigest(), p


# ---------- 变化归因 ----------
@test
def diff_removed_reason_you():
    now = time.time()
    old = [{"mid": 1, "uname": "甲"}]
    new = [{"mid": 2, "uname": "乙"}]
    d = m.diff_relation(old, new, {"1": now - 100})
    assert d["removed"][0]["reason"] == "you"
    assert d["added"][0]["reason"] == "new"


@test
def diff_removed_reason_they():
    old = [{"mid": 1, "uname": "甲"}]
    new = []
    d = m.diff_relation(old, new, {})
    assert d["removed"][0]["reason"] == "they"


@test
def diff_added_reason_you():
    now = time.time()
    new = [{"mid": 2, "uname": "乙"}]
    d = m.diff_relation([], new, {}, {"2": now - 100})
    assert d["added"][0]["reason"] == "you"


@test
def diff_renamed():
    d = m.diff_relation([{"mid": 1, "uname": "旧名"}],
                        [{"mid": 1, "uname": "新名"}], {})
    assert d["renamed"][0]["from"] == "旧名" and d["renamed"][0]["to"] == "新名"


# ---------- 注销识别 ----------
@test
def trim_user_detects_deactivated():
    for name in ("账号已注销", "帐号已注销", "账户已注销"):
        u = m.Bili._trim_user({"mid": 1, "uname": name})
        assert u["deactivated"] == 1, name
    u = m.Bili._trim_user({"mid": 1, "uname": "我关注注销教程"})
    assert u["deactivated"] == 0


# ---------- Cookie 解析 ----------
@test
def set_cookie_full_and_bare():
    b = m.Bili()
    b.set_cookie_str("SESSDATA=aaa; bili_jct=bbb; DedeUserID=123; path=/")
    assert b.cookies["SESSDATA"] == "aaa"
    assert b.cookies["bili_jct"] == "bbb"
    assert b.cookies["DedeUserID"] == "123"
    assert "path" not in b.cookies
    b2 = m.Bili()
    b2.set_cookie_str("bare_sessdata_value")
    assert b2.cookies["SESSDATA"] == "bare_sessdata_value"


# ---------- 版本比较 ----------
@test
def ver_tuple_ordering():
    assert m._ver_tuple("1.10.0") > m._ver_tuple("1.9.9")
    assert m._ver_tuple("2.0.0") > m._ver_tuple("1.99.99")
    assert not (m._ver_tuple("1.4.0") > m._ver_tuple("1.4.0"))


# ---------- 历史记录合并 ----------
@test
def record_history_merges_recent():
    hfile = os.path.join(TMP, "h.json")
    m.HISTORY_FILE = hfile
    if os.path.exists(hfile):
        os.remove(hfile)
    real_time = time.time
    try:
        time.time = lambda: 1000.0
        m.record_history(10, 5)      # follower=5 才会记录
        time.time = lambda: 1100.0   # 100 秒后:应合并为同一条
        m.record_history(11, 6)
        data = json.load(open(hfile, encoding="utf-8"))
        assert len(data) == 1 and data[0]["follower"] == 6
        time.time = lambda: 1000.0 + 3600  # 1小时后:新增一条
        m.record_history(12, 7)
        data = json.load(open(hfile, encoding="utf-8"))
        assert len(data) == 2
    finally:
        time.time = real_time


# ---------- 关系缓存(tags 覆盖回归) ----------
@test
def relation_cache_keeps_tags():
    cfile = os.path.join(TMP, "c.json")
    m.CACHE_FILE = cfile
    if os.path.exists(cfile):
        os.remove(cfile)
    m.save_relation_cache("followings", [{"mid": 1, "uname": "a"}])
    m.save_relation_cache("tags", [{"tagid": 7, "name": "g"}])
    data = json.load(open(cfile, encoding="utf-8"))
    assert isinstance(data["tags"], list), "tags 被覆盖成时间戳!"
    assert data["tags"][0]["tagid"] == 7
    assert isinstance(data["cached_at"], float)


# ---------- 风控离线回退 ----------
class _StubFailFetch:
    """mid() 正常,但拉取关注列表时抛风控错误。"""

    def mid(self):
        return "123"

    def fetch_all_followings(self, mid, progress_cb=None):
        raise m.BiliError("触发B站风控(-352)", code=-352)

    def stat(self):
        raise AssertionError("回退路径不应再调用 stat")


@test
def rebuild_cache_falls_back_to_cache():
    m.CACHE_FILE = os.path.join(TMP, "c2.json")
    if os.path.exists(m.CACHE_FILE):
        os.remove(m.CACHE_FILE)
    full = [{"mid": 1, "uname": "a", "sign": "", "face": "", "attribute": 6,
             "special": 0, "mtime": 123, "deactivated": 0}]
    m.save_relation_cache("followings", full)
    m.save_relation_cache("tags", [{"tagid": 7, "name": "g", "count": 1}])
    m.rebuild_cache(_StubFailFetch())
    assert m.CACHE["status"] == "ok", m.CACHE
    assert m.CACHE["stale"] is True
    assert m.CACHE["followings"] == full
    assert m.CACHE["tags"][0]["tagid"] == 7
    assert "回退" in m.CACHE["error"]


class _StubOK:
    def mid(self):
        return "123"

    def fetch_all_followings(self, mid, progress_cb=None):
        if progress_cb:
            progress_cb(2, 2)
        return [{"mid": 1, "uname": "a", "sign": "", "face": "",
                 "attribute": 6, "special": 0, "mtime": 1},
                {"mid": 2, "uname": "b", "sign": "", "face": "",
                 "attribute": 2, "special": 1, "mtime": 2}], 2

    def tags(self):
        return []

    def stat(self):
        return {"following": 2, "follower": 9}


@test
def rebuild_cache_success_writes_snapshot_and_cache():
    m.SNAPSHOT_FILE = os.path.join(TMP, "s.json")
    m.CACHE_FILE = os.path.join(TMP, "c3.json")
    for f in (m.SNAPSHOT_FILE, m.CACHE_FILE):
        if os.path.exists(f):
            os.remove(f)
    m.rebuild_cache(_StubOK())
    assert m.CACHE["status"] == "ok" and m.CACHE["stale"] is False
    snap = json.load(open(m.SNAPSHOT_FILE, encoding="utf-8"))
    assert [u["mid"] for u in snap["followings"]] == [1, 2]  # mini 快照
    cache = json.load(open(m.CACHE_FILE, encoding="utf-8"))
    assert len(cache["followings"]) == 2                     # 全量字段缓存
    hist = json.load(open(m.HISTORY_FILE, encoding="utf-8"))
    assert hist[-1]["follower"] == 9


# ---------- 运行 ----------
def main():
    failed = []
    for name, fn, _ in RESULTS:
        try:
            fn()
            print("PASS %s" % name)
        except AssertionError as e:
            failed.append(name)
            print("FAIL %s : %s" % (name, e))
        except Exception as e:
            failed.append(name)
            print("ERROR %s : %r" % (name, e))
    print("-" * 40)
    print("%d/%d 通过" % (len(RESULTS) - len(failed), len(RESULTS)))
    if failed:
        print("失败:", ", ".join(failed))
        sys.exit(1)


if __name__ == "__main__":
    main()
