import eyegway.utils as eu


class TestDemoData:

    def test_demo_data(self):

        generator = eu.DemoDataGenerator()
        data = generator.generate()
        assert len(data.keys()) > 0
