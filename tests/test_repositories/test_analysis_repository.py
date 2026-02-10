import pytest
from app.infrastructure.database.repositories.analysis_repository import (
    AnalysisRepository,
)


@pytest.mark.asyncio
async def test_get_tourists_for_all_dates(async_session, test_records):
    repo = AnalysisRepository(async_session)

    response = await repo.get_tourists_for_all_dates()

    assert response == {"Количество туристов за все даты": int(10)}


@pytest.mark.asyncio
async def test_get_tourists_for_every_month(async_session, test_records):
    repo = AnalysisRepository(async_session)

    response = await repo.get_tourists_for_every_month()

    assert isinstance(response["Количество туристов за периоды"], list)
    assert len(response["Количество туристов за периоды"]) > 0
    assert response["Количество туристов за периоды"][0]["Количество"] == 10


@pytest.mark.asyncio
async def test_get_tourists_for_random_period(async_session, test_records):
    repo = AnalysisRepository(async_session)

    response = await repo.get_tourists_for_random_period()
    assert isinstance(response["Количество посетителей за рандомный промежуток"], list)
    assert len(response["Количество посетителей за рандомный промежуток"]) > 0
    assert (
        response["Количество посетителей за рандомный промежуток"][0][
            "Количество человек:"
        ]
        == 10
    )


@pytest.mark.asyncio
async def test_get_tourists_by_country(async_session, test_records):
    repo = AnalysisRepository(async_session)

    response = await repo.get_tourists_by_country()
    assert isinstance(response["Территориальное распределение по странам"], list)
    assert len(response["Территориальное распределение по странам"]) > 0
    assert (
        response["Территориальное распределение по странам"][0][
            "Количество посетителей"
        ]
        == 1
    )


@pytest.mark.asyncio
async def test_get_tourists_by_region(async_session, test_records):
    repo = AnalysisRepository(async_session)

    response = await repo.get_tourists_by_region()
    assert isinstance(response["Территориальное распределение по регионам"], list)
    assert len(response["Территориальное распределение по регионам"]) > 0
    assert (
        response["Территориальное распределение по регионам"][0][
            "Количество посетителей"
        ]
        == 1
    )


@pytest.mark.asyncio
async def test_get_demographic_distribution(async_session, test_records):
    repo = AnalysisRepository(async_session)

    response = await repo.get_demographic_distribution()
    assert isinstance(response["Демографическое распределение"], list)
    assert len(response["Демографическое распределение"]) > 0
    assert response["Демографическое распределение"][0]["Количество"] == 1


@pytest.mark.asyncio
async def test_get_typical_tourist_profile(async_session, test_records):
    repo = AnalysisRepository(async_session)

    response = await repo.get_typical_tourist_profile()
    assert isinstance(response["Профиль среднестатестического туриста"], dict)
    assert (
        response["Профиль среднестатестического туриста"]["Количество дней в городе"]
        == 1
    )


@pytest.mark.asyncio
async def test_get_most_valuable_segments(async_session, test_records):
    repo = AnalysisRepository(async_session)

    response = await repo.get_most_valuable_segments()

    assert isinstance(response["Популярные категории туристов"], list)
    assert len(response["Популярные категории туристов"]) > 0
    assert (
        response["Популярные категории туристов"][0]["Среднее количество дней в городе"]
        == 1
    )
