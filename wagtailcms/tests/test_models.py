from django.test import TestCase, RequestFactory
from wagtail.images.tests.utils import Image, get_test_image_file

from wagtailcms.models import *


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class LinkBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = LinkBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = block.get_context({
            'url': 'url',
            'text': 'text',
            'cls': 'class'
        }, parent_context={
            'request': request,
        })
        self.assertEqual('url?country=104', context.get('href'))
        self.assertEqual('text', context.get('text'))
        self.assertEqual('class', context.get('class'))


class AnchorBlockTestCase(TestCase):

    def test_get_context(self):
        block = AnchorBlock()
        context = block.get_context({'slug': 'slug'})
        self.assertEqual('slug', context.get('slug'))


class FAQsBlockTestCase(TestCase):

    def test_get_context(self):
        block = FAQsBlock()
        context = block.get_context({
            'title': 'title',
            'faqs': [
                {
                    'slug': 'slug1',
                    'question': 'question1',
                    'answer': 'answer1'
                },
                {
                    'slug': 'slug2',
                    'question': 'question2',
                    'answer': 'answer2'
                },
            ]
        })
        self.assertEqual('title', context.get('title'))
        self.assertEqual(2, len(context.get('list')))
        self.assertEqual('slug1', context.get('list')[0]['slug'])
        self.assertEqual('question1', context.get('list')[0]['term'])
        self.assertEqual('answer1', context.get('list')[0]['definition'])


class TwitterBlockTestCase(TestCase):

    def test_get_context(self):
        block = TwitterBlock()
        context = block.get_context({
            'count': 3,
            'username': 'Land_Matrix',
        })
        self.assertEqual('', context.get('timeline'))
        self.assertEqual('Land_Matrix', context.get('username'))


class NoWrapsStreamBlockTestCase(TestCase):

    def setUp(self):
        self.block = NoWrapsStreamBlock()

        class ChildBlock:

            block_type = ''

            def __init__(self, value, block_type=''):
                self.value = value
                self.block_type = block_type

            def render(self, context=None):
                return self.value

        self.children = [
            ChildBlock('1', 'full_width_container'),
            ChildBlock('2', 'test')
        ]

    def test_render_basic(self):
        output = self.block.render_basic(self.children)
        self.assertEqual('<div class="">1</div>\n<div class="block-test block">2</div>', output)


class NoWrapsStreamFieldTestCase(TestCase):

    def test_init(self):
        block = NoWrapsStreamField(Block())
        self.assertIsInstance(block.stream_block, Block)
        block = NoWrapsStreamField(Block)
        self.assertIsInstance(block.stream_block, Block)
        block = NoWrapsStreamField([])
        self.assertIsInstance(block.stream_block, NoWrapsStreamBlock)


class ImageBlockTestCase(TestCase):

    def test_get_context(self):
        block = ImageBlock()
        image = Image.objects.create(id=1, title='Test', file=get_test_image_file())
        context = block.get_context(image)
        self.assertGreater(len(context.get('url')), 0)
        self.assertEqual('Test', context.get('name'))


class LinkedImageBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = LinkedImageBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        image = Image.objects.create(id=1, title='Test', file=get_test_image_file())
        context = block.get_context({
            'url': 'url',
            'image': image,
        }, {
            'request': request
        })
        self.assertEqual('url?country=104', context.get('href'))
        self.assertGreater(len(context.get('url')), 0)


class SliderBlockTestCase(TestCase):

    def test_get_context(self):
        block = SliderBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        image = Image.objects.create(id=1, title='Test', file=get_test_image_file())
        context = block.get_context({
            'title': 'title',
            'images': [
                {
                    'image': image,
                    'url': 'url',
                    'caption': 'caption',
                }
            ]
        }, {
            'request': request
        })
        self.assertEqual('title', context.get('title'))
        self.assertEqual(1, len(context.get('images')))
        self.assertGreater(len(context.get('images')[0]['url']), 0)
        self.assertEqual('Test', context.get('images')[0]['name'])
        self.assertEqual('url', context.get('images')[0]['href'])
        self.assertEqual('caption', context.get('images')[0]['caption'])


class GalleryBlockTestCase(TestCase):

    def test_get_context(self):
        block = GalleryBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        image = Image.objects.create(id=1, title='Test', file=get_test_image_file())
        context = block.get_context({
            'title': 'title',
            'columns': '2',
            'images': [
                {
                    'image': image,
                    'url': 'url',
                }
            ]
        }, {
            'request': request
        })
        self.assertEqual('title', context.get('title'))
        self.assertEqual(2, context.get('columns'))
        self.assertEqual(1, len(context.get('images')))
        self.assertGreater(len(context.get('images')[0]['url']), 0)
        self.assertEqual('Test', context.get('images')[0]['name'])
        self.assertEqual('url', context.get('images')[0]['href'])


class TitleWithIconBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = TitleWithIconBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = block.get_context({
            'value': 'value',
            'fa_icon': 'fa_icon',
            'url': 'url',
        }, {
            'request': request
        })
        self.assertEqual('value', context.get('value'))
        self.assertEqual('fa_icon', context.get('fa_icon'))
        self.assertEqual('url?country=104', context.get('url'))


class LatestNewsBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context_with_country(self):
        block = LatestNewsBlock()
        request = RequestFactory()
        page = BlogPage.objects.create(title='Blog Page', path='/', depth=0, live=True)
        page.tags.add('myanmar')
        page.save()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = block.get_context({
            'limit': '3',
        }, {
            'request': request
        })
        self.assertEqual(104, context.get('country').id)
        self.assertEqual('Myanmar', context.get('name'))
        self.assertEqual(1, len(context.get('news')))


class StatisticsBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = StatisticsBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = block.get_context({}, {
            'request': request
        })
        self.assertEqual(104, context.get('country').id)


class MapDataChartsBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = MapDataChartsBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = block.get_context({}, {
            'request': request
        })
        self.assertEqual(104, context.get('country').id)


class LinkMapBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = LinkMapBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = block.get_context({}, {
            'request': request
        })
        self.assertEqual({'implementation', 'intention', 'level_of_accuracy'}, set(context.get('legend').keys()))
        self.assertGreater(len(context.get('legend_json')), 0)
        self.assertEqual(104, context.get('map_object').id)
        self.assertEqual(True, context.get('is_country'))


class LatestDatabaseModificationsBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = LatestDatabaseModificationsBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = block.get_context({
            'limit': 'limit'
        }, {
            'request': request
        })
        self.assertEqual(104, context.get('country').id)
        self.assertEqual('limit', context.get('limit'))


class RegionBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = RegionBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = block.get_context({}, {
            'request': request
        })
        self.assertEqual(104, context.get('country').id)
        self.assertEqual(142, context.get('region').id)


class CountriesBlockTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        block = CountriesBlock()
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'region_slug': 'asia'})
        context = block.get_context({}, {
            'request': request
        })
        self.assertEqual(142, context.get('region').id)
        self.assertGreater(len(context.get('countries')), 0)


class Columns1To1BlockTestCase(TestCase):

    def test_get_context(self):
        block = Columns1To1Block()
        context = block.get_context({
            'left_column': 'left_column',
            'right_column': 'right_column',
        })
        self.assertEqual('left_column', context.get('left_column'))
        self.assertEqual('right_column', context.get('right_column'))


class ThreeColumnsBlockTestCase(TestCase):

    def test_get_context(self):
        block = ThreeColumnsBlock()
        context = block.get_context({
            'left_column': 'left_column',
            'middle_column': 'middle_column',
            'right_column': 'right_column',
        })
        self.assertEqual('left_column', context.get('left_column'))
        self.assertEqual('middle_column', context.get('middle_column'))
        self.assertEqual('right_column', context.get('right_column'))


class TabsBlockTestCase(TestCase):

    def test_get_context(self):
        block = TabsBlock()
        context = block.get_context({
            'tabs': [
                {
                    'title': 'title',
                    'fa_icon': 'fa_icon',
                    'content': 'content',
                }
            ]
        })
        self.assertEqual(1, len(context.get('list')))
        self.assertEqual('title', context.get('list')[0]['title'])
        self.assertEqual('fa_icon', context.get('list')[0]['fa_icon'])
        self.assertEqual('content', context.get('list')[0]['content'])


class FullWidthContainerBlockTestCase(TestCase):

    def test_get_context(self):
        block = FullWidthContainerBlock()
        context = block.get_context({
            'content': 'content',
            'color': 'color'
        })
        self.assertEqual('content', context.get('content'))
        self.assertEqual('color', context.get('color'))


class RegionIndexTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        page = RegionIndex.objects.create(title='Blog Page', path='/', depth=0)
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'region_slug': 'asia'})
        context = page.get_context(request)
        self.assertEqual(142, context.get('region').id)


class CountryIndexTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_context(self):
        page = CountryIndex.objects.create(title='Blog Page', path='/', depth=0)
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        context = page.get_context(request)
        self.assertEqual(104, context.get('country').id)


class WagtailCMSModelsTestCase(TestCase):

    fixtures = [
        'countries_and_regions'
    ]

    def test_get_country_or_region_with_page_country(self):
        page = CountryPage.objects.create(title='Myanmar Page', country_id=104, path='/', depth=0)
        result = get_country_or_region(RequestFactory(), page=page)
        self.assertEqual(104, result.get('country').id)

    def test_get_country_or_region_with_page_region(self):
        page = RegionPage.objects.create(title='Asia Page', region_id=142, path='/', depth=0)
        result = get_country_or_region(RequestFactory(), page=page)
        self.assertEqual(142, result.get('region').id)

    def test_get_country_or_region_with_request_country(self):
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        result = get_country_or_region(request)
        self.assertEqual(104, result.get('country').id)

    def test_get_country_or_region_with_request_region(self):
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'region_slug': 'asia'})
        result = get_country_or_region(request)
        self.assertEqual(142, result.get('region').id)

    def test_get_country_or_region_link(self):
        request = RequestFactory()
        request.resolver_match = AttrDict(kwargs={'country_slug': 'myanmar'})
        link = get_country_or_region_link('url', request=request)
        self.assertEqual('url?country=104', link)

    def test_editor_js(self):
        self.assertGreater(len(editor_js()), 0)

    def test_editor_css(self):
        self.assertGreater(len(editor_css()), 0)

    def test_whitelister_element_rules(self):
        rules = whitelister_element_rules()
        self.assertIsInstance(rules, dict)
        self.assertGreater(len(rules.keys()), 0)
