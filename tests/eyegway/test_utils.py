import eyegway.utils.generators as eug


class TestDemoData:

    def test_demo_data(self):

        generator = eug.DemoDataGenerator()
        data = generator.generate()
        assert len(data.keys()) > 0
