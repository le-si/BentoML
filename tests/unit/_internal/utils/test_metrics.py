from __future__ import annotations

import math

from bentoml._internal.utils.metrics import INF
from bentoml._internal.utils.metrics import exponential_buckets
from bentoml._internal.utils.metrics import linear_buckets
from bentoml._internal.utils.metrics import metric_name


def _assert_equal(actual: tuple[float, ...], expected: tuple[float, ...]):
    assert len(actual) == len(expected)
    for i in range(len(actual)):
        assert math.isclose(actual[i], expected[i])


def test_exponential_buckets():
    # Test with extended range for LLM workloads
    _assert_equal(
        exponential_buckets(0.005, 2.0, 180.0),
        (
            0.005,
            0.01,
            0.02,
            0.04,
            0.08,
            0.16,
            0.32,
            0.64,
            1.28,
            2.56,
            5.12,
            10.24,
            20.48,
            40.96,
            81.92,
            163.84,
            180.0,
            INF,
        ),
    )
    _assert_equal(
        exponential_buckets(1, 1.5, 100.0),
        (
            1,
            1.5,
            2.25,
            3.375,
            5.0625,
            7.59375,
            11.390625,
            17.0859375,
            25.62890625,
            38.443359375,
            57.6650390625,
            86.49755859375,
            100.0,
            INF,
        ),
    )
    _assert_equal(
        exponential_buckets(10, 2.5, 1000.0),
        (10, 25.0, 62.5, 156.25, 390.625, 976.5625, 1000.0, INF),
    )

    _assert_equal(
        exponential_buckets(1, 1.1, 100000.0),
        (
            1,
            1.1,
            1.2100000000000002,
            1.3310000000000004,
            1.4641000000000006,
            1.6105100000000008,
            1.771561000000001,
            1.9487171000000014,
            2.1435888100000016,
            2.357947691000002,
            2.5937424601000023,
            2.853116706110003,
            3.1384283767210035,
            3.4522712143931042,
            3.797498335832415,
            4.177248169415656,
            4.594972986357222,
            5.054470284992944,
            5.559917313492239,
            6.115909044841463,
            6.72749994932561,
            7.400249944258172,
            8.140274938683989,
            8.954302432552389,
            9.849732675807628,
            10.834705943388391,
            11.91817653772723,
            13.109994191499954,
            14.420993610649951,
            15.863092971714948,
            17.449402268886445,
            19.19434249577509,
            21.1137767453526,
            23.22515441988786,
            25.54766986187665,
            28.102436848064315,
            30.91268053287075,
            34.003948586157826,
            37.40434344477361,
            41.14477778925097,
            45.25925556817607,
            49.785181124993684,
            54.76369923749306,
            60.24006916124237,
            66.26407607736661,
            72.89048368510328,
            80.17953205361361,
            88.19748525897498,
            97.01723378487249,
            106.71895716335975,
            117.39085287969573,
            129.1299381676653,
            142.04293198443185,
            156.24722518287504,
            171.87194770116255,
            189.05914247127882,
            207.96505671840671,
            228.7615623902474,
            251.63771862927217,
            276.80149049219943,
            304.4816395414194,
            334.9298034955614,
            368.4227838451175,
            405.2650622296293,
            445.79156845259223,
            490.3707252978515,
            539.4077978276367,
            593.3485776104004,
            652.6834353714405,
            717.9517789085846,
            789.7469567994432,
            868.7216524793876,
            955.5938177273264,
            1051.1531995000591,
            1156.2685194500652,
            1271.8953713950718,
            1399.0849085345792,
            1538.9933993880372,
            1692.8927393268411,
            1862.1820132595253,
            2048.400214585478,
            2253.240236044026,
            2478.564259648429,
            2726.4206856132723,
            2999.0627541746,
            3298.96902959206,
            3628.8659325512663,
            3991.7525258063934,
            4390.927778387033,
            4830.020556225737,
            5313.0226118483115,
            5844.324873033143,
            6428.757360336458,
            7071.633096370105,
            7778.796406007116,
            8556.676046607829,
            9412.343651268613,
            10353.578016395475,
            11388.935818035023,
            12527.829399838525,
            100000.0,
            INF,
        ),
    )


def test_linear_buckets():
    _assert_equal(
        linear_buckets(1.0, 1.0, 10.0),
        (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, INF),
    )

    _assert_equal(
        linear_buckets(0.1, 0.5, 10.0),
        (
            0.1,
            0.6,
            1.1,
            1.6,
            2.1,
            2.6,
            3.1,
            3.6,
            4.1,
            4.6,
            5.1,
            5.6,
            6.1,
            6.6,
            7.1,
            7.6,
            8.1,
            8.6,
            9.1,
            9.6,
            10.0,
            INF,
        ),
    )


def test_default_bucket():
    # Verify DEFAULT_BUCKET covers appropriate ranges for both fast APIs and LLM workloads
    from bentoml._internal.utils.metrics import DEFAULT_BUCKET

    # Test bucket count
    assert len(DEFAULT_BUCKET) == 16  # Optimized number of buckets

    # Test key latency boundaries
    assert DEFAULT_BUCKET[0] == 0.005  # Fast API calls start (5ms)
    assert DEFAULT_BUCKET[4] == 0.1  # Regular API calls start (100ms)
    assert DEFAULT_BUCKET[8] == 2.5  # Long API calls start (2.5s)
    assert DEFAULT_BUCKET[11] == 30.0  # LLM models start (30s)
    assert DEFAULT_BUCKET[-2] == 180.0  # Maximum LLM latency (180s)
    assert DEFAULT_BUCKET[-1] == float("inf")

    # Test monotonic increase
    for i in range(len(DEFAULT_BUCKET) - 1):
        assert DEFAULT_BUCKET[i] < DEFAULT_BUCKET[i + 1]


def test_metric_name():
    assert metric_name("runner_name", "metric_name") == "runner_name_metric_name"
    assert metric_name("runner.name", "metric_name") == "runner::name_metric_name"
    assert metric_name("runner-name", "metric_name") == "runner:name_metric_name"
    assert metric_name("runner_name", "metric.name") == "runner_name_metric::name"
    assert metric_name("runner_name", "metric-name") == "runner_name_metric:name"
    assert metric_name("runner_name", 1, "metric_name") == "runner_name_1_metric_name"
    assert (
        metric_name("runner_name", 1, "method_name", "metric_name")
        == "runner_name_1_method_name_metric_name"
    )
