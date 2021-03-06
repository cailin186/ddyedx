from django.test.utils import override_settings

from xmodule.modulestore.xml_importer import import_from_xml

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.django import modulestore
from xmodule.modulestore import Location

from contentstore.tests.modulestore_config import TEST_MODULESTORE


# This test is in the CMS module because the test configuration to use a draft
# modulestore is dependent on django.
@override_settings(MODULESTORE=TEST_MODULESTORE)
class DraftReorderTestCase(ModuleStoreTestCase):

    def test_order(self):
        store = modulestore('direct')
        draft_store = modulestore('default')
        import_from_xml(store, 'common/test/data/', ['import_draft_order'], draft_store=draft_store)
        sequential = draft_store.get_item(
            Location('i4x', 'test_org', 'import_draft_order', 'sequential', '0f4f7649b10141b0bdc9922dcf94515a', None)
        )
        verticals = sequential.children

        # The order that files are read in from the file system is not guaranteed (cannot rely on
        # alphabetical ordering, for example). Therefore, I have added a lot of variation in filename and desired
        # ordering so that the test reliably failed with the bug, at least on Linux.
        #
        # 'a', 'b', 'c', 'd', and 'z' are all drafts, with 'index_in_children_list' of
        #  2 ,  4 ,  6 ,  5 , and  0  respectively.
        #
        # '5a05be9d59fc4bb79282c94c9e6b88c7' and 'second' are public verticals.
        self.assertEqual(7, len(verticals))
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/z', verticals[0])
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/5a05be9d59fc4bb79282c94c9e6b88c7', verticals[1])
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/a', verticals[2])
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/second', verticals[3])
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/b', verticals[4])
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/d', verticals[5])
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/c', verticals[6])

        # Now also test that the verticals in a second sequential are correct.
        sequential = draft_store.get_item(
            Location('i4x', 'test_org', 'import_draft_order', 'sequential', 'secondseq', None)
        )
        verticals = sequential.children
        # 'asecond' and 'zsecond' are drafts with 'index_in_children_list' 0 and 2, respectively.
        # 'secondsubsection' is a public vertical.
        self.assertEqual(3, len(verticals))
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/asecond', verticals[0])
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/secondsubsection', verticals[1])
        self.assertEqual(u'i4x://test_org/import_draft_order/vertical/zsecond', verticals[2])
