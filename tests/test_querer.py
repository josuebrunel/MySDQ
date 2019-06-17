import pytest

from mysdq import DictQuerer


def test_query_count(data):
    qs = DictQuerer(data)
    assert qs.count() == 7


def test_query_key(data):
    qs = DictQuerer(data)
    yloking = qs.get(nickname='yloking')
    assert yloking['firstname'] == 'yosuke'
    assert yloking['lastname'] == 'loking'
    assert yloking['age'] == 25

    assert qs.filter(age__lt=25).count() == 2

    with pytest.raises(Exception) as exc:
        DictQuerer(data).get(age=25)
    assert exc.value.args[0] == 'Multiple values returned'

    DictQuerer(data).filter(lastname='young', age__le=20).exists is False


def test_query_subkey(data):
    qs = DictQuerer(data)
    res = qs.filter(address__zipcode='94290')
    assert res.count() == 1
    assert res.first()['nickname'] == 'jkouka'
    res = qs.filter(address__num__ge=100)
    assert res.count() == 2
    assert res.last()['address']['num'] in (118, 119)


def test_query_deletion(data):
    qs = DictQuerer(data)
    assert qs.count() == 7
    qs.delete(address__zipcode="")
    assert qs.count() == 5
    qs.delete()
    assert qs.count() == 0


def test_query_list_item(data):
    qs = DictQuerer(data)
    res = qs.filter(profiles__0__url__contains='loking')
    assert res.count() == 1
    assert res.first()['nickname'] == 'yloking'
    res = qs.filter(profiles__0__username='dmccrey', age__ge=32)
    assert res.last()['firstname'] == 'david'


def test_query_orderby(data):
    qs = DictQuerer(data)
    res = qs.order_by('age')
    assert res.first()['nickname'] == 'tblack'
    assert res.last()['nickname'] == 'kyoung'


def test_query_groupby(data):
    qs = DictQuerer(data)
    res = qs.group_by('age')
    assert len(res[25]) == 2


def test_query_values(data):
    qs = DictQuerer(data)
    res = qs.filter(address__city='Pointe-Noire').values('nickname', 'age')
    assert len(res) == 2
    for item in res:
        assert item['age'] in (24, 32)
        assert item['nickname'] in ('dmccrey', 'kkwame')


def test_query_apply(data):
    qs = DictQuerer(data)
    res = qs.filter(age__lt=18).apply(lambda x: x*2, 'age').first()
    assert res['nickname'] == 'tblack'
    assert res['age'] == 30
    qs.apply(
            lambda x: x.update({'city': 'Paris', 'zipcode': '75008', 'country': 'France'}) or x, 'address')
    assert qs.filter(address__country='France').count() == 7
