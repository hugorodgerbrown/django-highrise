"""
Django test for django-highrise app.
"""
from pyrise import Highrise
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from . import (
    create_new_contact,
    sync_user,
    init,
    test_me,
    HighriseSyncException
)


class HighriseIntegrationTestCase(TestCase):
    """
    Tests for django_highrise app.
    """

    def setUp(self):
        """
        Initialise pyrise connection settings, and test connectivity.
        """
        init(settings.HIGHRISE_SERVER, settings.HIGHRISE_API_KEY)
        self.test_user = User.objects.create_user('john',
            'lennon@thebeatles.com', 'johnpassword')
        self.test_user.first_name = 'john'
        self.test_user.last_name = 'lennon'

    def tearDown(self):
        pass

    def test_unitialised_connection(self):
        """Test that correct exception is raised if pyrise is not initialised."""
        Highrise._server = None
        with self.assertRaises(HighriseSyncException) as cm:
            sync_user(self.test_user)

        ex = cm.exception
        self.assertEqual(
            ex.message[:39],
            "Highrise connection is not initialised."
        )

    def test_test_me(self):
        """Test the 'test_me' function that pings Highrise."""
        self.assertTrue(test_me())

    def test_contact_properties(self):
        """Test basic read/write properties of HighriseContact object."""
        user = self.test_user
        contact = sync_user(user)
        self.assertEqual(
            unicode(contact),
            u"%s = %s" % (user.first_name, contact.highrise_id)
        )
        self.assertEqual(
            str(contact),
            "%s = %s" % (user.first_name, contact.highrise_id)
        )
        person = contact.person
        contact.person = None
        self.assertIsNone(contact.person)
        self.assertIsNone(contact.highrise_id)
        contact.person = person
        self.assertEqual(contact.person, person)
        self.assertEqual(contact.highrise_id, person.id)

    def test_sync_new_user(self):
        """Test syncing a user who is not already in Highrise."""
        user = self.test_user
        contact = sync_user(user)
        cp = contact.person
        self.assertIsNotNone(cp)
        self.assertEqual(cp.id, contact.highrise_id)
        self.assertEqual(cp.first_name, user.first_name)
        self.assertEqual(cp.last_name, user.last_name)
        self.assertEqual(len(cp.contact_data.email_addresses), 1)
        self.assertEqual(cp.contact_data.email_addresses[0].address, user.email)
        self.assertIsNone(contact.company_id)
        # always clean up after yourself.
        contact.person.delete()

    def test_sync_existing_user(self):
        """Test syncing a user a second time."""
        user = self.test_user
        contact1 = sync_user(user)
        contact2 = sync_user(user)
        self.assertEqual(contact1.person.id, contact2.person.id)
        self.assertEqual(contact1.highrise_id, contact2.highrise_id)
        self.assertEqual(contact1.created_at, contact2.created_at)
        self.assertEqual(contact1.last_synced_at, contact2.last_synced_at)
        self.assertNotEqual(contact1.company_id, contact2.last_synced_at)
        contact1.person.delete()

    def test_duplicate_highrise_contacts_raises_exception(self):
        """Test that duplicate highrise contacts (same email) will raise an exception."""
        user = self.test_user
        p1 = create_new_contact(user)
        p2 = create_new_contact(user)
        with self.assertRaises(HighriseSyncException):
            sync_user(user)
        p1.delete()
        p2.delete()
