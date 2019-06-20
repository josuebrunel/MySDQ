import pytest

from mysdq import DictQuerer
from mysdq.query import Xoperator


def test_dictquerer():
    data = [{'foo': 'bar'}]
    qs = DictQuerer(data)
    assert isinstance(qs._xoperator,  (Xoperator,)) is True
    assert str(qs) == str(data)
    assert repr(qs) == "<DictQuerer: [{'foo': 'bar'}] >"


def test_query_count(data):
    qs = DictQuerer(data)
    assert qs.count() == 7


def test_query_key(data):
    qs = DictQuerer(data)
    assert qs.get(nickname='foo') is None
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
    assert qs.delete(nickname='foo') is False
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
    res = qs.order_by('age', asc=False)
    assert res.first()['nickname'] == 'kyoung'


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


def test_dictquerer_operator_in(data):
    qs = DictQuerer(data)
    res = qs.filter(age__in=[15, 24, 25])
    assert res.count() == 4


def test_dictquerer_operator_not_in(data):
    qs = DictQuerer(data)
    res = qs.filter(age__not_in=[15, 24, 25])
    assert res.count() == 3


def test_dictquerer_operator_icontains(data):
    qs = DictQuerer(data)
    res = qs.filter(address__city__icontains='paris')
    assert res.count() == 1


def test_dictquerer_operator_startswith(data):
    qs = DictQuerer(data)
    res = qs.filter(nickname__startswith='j')
    assert res.count() == 2


def test_dictquerer_operator_endswith(data):
    qs = DictQuerer(data)
    res = qs.filter(nickname__endswith='g')
    assert res.count() == 2


def test_dictquerer_operator_regex(data):
    qs = DictQuerer(data)
    res = qs.filter(address__name__regex=r'^rue.*')
    assert res.count() == 2
    res = qs.filter(address__name__regex=r'.*tchibimda')
    assert res.count() == 1


def test_dictquerer_operator_iregex(data):
    qs = DictQuerer(data)
    res = qs.filter(address__city__iregex='.*noire$')
    assert res.count() == 2
