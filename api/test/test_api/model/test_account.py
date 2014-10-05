
#from vistar.model import Advertiser
#from vistar.model import Network
#from vistar.model import User
#from vistar.model import db
#
#from test import ModelTestCase

from injector import inject

from api.model import Account
from api.model import Accounts
from test import ModelTest


class TestAccount(ModelTest):

 @inject(accounts=Accounts)
 def test_get_by_id(self, accounts):
   account = Account(email='test@foo.com', name='Test User')
   self.db.session.add(account)
   self.db.session.commit()

   account1 = accounts.query.get(account.id)
   self.assertEquals(account.id, account1.id)

#  def test_has_advertisers(self):
#    user1 = self.create_user(email='user1@example.com')
#    user2 = self.create_user(email='user2@example.com')
#    advertiser = self.create_advertiser(user=user1)
#    db.session.commit()
#
#    user1_advertisers = list(user1.advertisers)
#    self.assertEquals(1, len(user1_advertisers))
#    self.assertEquals(advertiser.id, user1_advertisers[0].id)
#
#    self.assertEquals(0, len(user2.advertisers))
#
#  def test_cascading_delete_of_advertisers(self):
#    user1 = self.create_user(email='test@example.com')
#    user2 = self.create_user(email='user2@example.com')
#
#    self.create_advertiser(user=user1)
#    self.create_advertiser(user=user1)
#    self.create_advertiser(user=user2)
#    db.session.commit()
#
#    self.assertEquals(2, len(user1.advertisers))
#    self.assertEquals(1, len(user2.advertisers))
#    self.assertEquals(3, Advertiser.query.count())
#
#    db.session.delete(user2)
#    db.session.commit()
#    self.assertEquals(2, Advertiser.query.count())
#
#    db.session.delete(user1)
#    db.session.commit()
#    self.assertEquals(0, Advertiser.query.count())
#
#  def test_has_networks(self):
#    user1 = self.create_user(email='user1@example.com')
#    user2 = self.create_user(email='user2@example.com')
#    network = self.create_network(partner=user1)
#    db.session.commit()
#
#    user1_networks = list(user1.networks)
#    self.assertEquals(1, len(user1_networks))
#    self.assertEquals(network.id, user1_networks[0].id)
#
#    user2_networks = list(user2.networks)
#    self.assertEquals(0, len(user2_networks))
#
#  def test_cascading_delete_of_networks(self):
#    user1 = self.create_user(email='test@example.com')
#    user2 = self.create_user(email='user2@example.com')
#
#    self.create_network(partner=user1)
#    self.create_network(partner=user1)
#    self.create_network(partner=user2)
#    db.session.commit()
#
#    self.assertEquals(2, len(user1.networks))
#    self.assertEquals(1, len(user2.networks))
#    self.assertEquals(3, Network.query.count())
#
#    db.session.delete(user2)
#    db.session.commit()
#    self.assertEquals(2, Network.query.count())
#
#    db.session.delete(user1)
#    db.session.commit()
#    self.assertEquals(0, Network.query.count())
#
#  def test_client_campaigns(self):
#    user = self.create_user(is_client=True, is_partner=True)
#    db.session.commit()
#
#    client_campaign = self.create_direct_campaign(
#      insertion_order = self.create_insertion_order(
#        advertiser = self.create_advertiser(user=user)))
#
#    partner_campaign = self.create_direct_campaign(
#      insertion_order = self.create_insertion_order(
#        network = self.create_network(partner=user)))
#
#    partner_direct_campaign = self.create_direct_campaign(
#      insertion_order = self.create_insertion_order(
#        network = self.create_network(partner=user),
#        client_id = user.id))
#
#    db.session.commit()
#
#    self.assertTrue(client_campaign in list(user.client_campaigns))
#    self.assertTrue(partner_direct_campaign in list(user.client_campaigns))
#
#    self.assertTrue(partner_campaign in list(user.partner_campaigns))
#    self.assertTrue(partner_direct_campaign in list(user.partner_campaigns))
#
#  def test_has_insertion_orders(self):
#    user = self.create_user(is_client=True)
#    advertiser = self.create_advertiser(user=user)
#    users_io = self.create_insertion_order(advertiser=advertiser)
#    self.create_insertion_order()
#    db.session.commit()
#
#    io_ids = list(io.id for io in user.insertion_orders)
#    self.assertEquals([users_io.id], io_ids)
#
#  def test_partner_ios(self):
#    partner = self.create_user(is_partner=True)
#    partner_io = self.create_insertion_order(
#      network=self.create_network(partner=partner))
#
#    client = self.create_user(is_client=True)
#    client_io = self.create_insertion_order(
#      advertiser=self.create_advertiser(user=client))
#
#    shared_io = self.create_insertion_order(
#      advertiser = self.create_advertiser(user=client),
#      network    = self.create_network(partner=partner))
#
#    db.session.commit()
#
#    self.assertEquals(sorted([partner_io.id, shared_io.id]),
#                      sorted(io.id for io in partner.insertion_orders))
#
#    self.assertEquals(sorted([client_io.id, shared_io.id]),
#                      sorted(io.id for io in client.insertion_orders))
#
#  def test_direct_advertisers(self):
#    """
#    it should include only advertisers specified thru client audience insertion
#    orders
#    """
#    user1       = self.create_user(email='user1@example.com')
#    user2       = self.create_user(email='user2@example.com')
#    advertiser1 = self.create_advertiser(user=user1)
#    advertiser2 = self.create_advertiser(user=user2)
#    self.create_insertion_order(_client=user1, advertiser=advertiser2)
#
#    db.session.commit()
#
#    advertisers = list(user1.direct_advertisers)
#
#    self.assertNotIn(advertiser1, advertisers)
#    self.assertIn(advertiser2, advertisers)
#
#  def test_audience_advertisers(self):
#    user1       = self.create_user(email='user1@example.com')
#    user2       = self.create_user(email='user2@example.com')
#    advertiser1 = self.create_advertiser(user=user1)
#    advertiser2 = self.create_advertiser(user=user2)
#    self.create_insertion_order(_client=user1, advertiser=advertiser2)
#
#    db.session.commit()
#
#    advertisers = list(user1.audience_advertisers)
#
#    self.assertIn(advertiser1, advertisers)
#    self.assertNotIn(advertiser2, advertisers)
#
#  def test_direct_creatives(self):
#    """
#    test_creatives_from_orders should fetch creatives that appear in campaigns
#    on insertion orders
#    """
#    user1       = self.create_user(email='user1@example.com')
#    user2       = self.create_user(email='user2@example.com')
#    advertiser1 = self.create_advertiser(user=user1)
#
#    insertion_order = self.create_insertion_order(_client=user2,
#        advertiser=advertiser1)
#    campaign = self.create_direct_campaign(insertion_order=insertion_order)
#    creative = self.create_creative(advertiser=advertiser1)
#
#    campaign.creatives = [creative]
#
#    db.session.commit()
#
#    creatives = list(user2.direct_creatives)
#
#    self.assertIn(creative, creatives)
