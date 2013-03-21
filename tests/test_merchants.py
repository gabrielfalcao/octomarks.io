from merchants.app import app
from merchants.models import Merchant, CompetitorTracker, Category


def teardown():
    """Flushes completely the test database.

    This function will be called by nose and will destroy our test db
    after each test. Make sure that the `settings_path` that you're
    passing to this app is the right one, LOL.
    """
    app.db.flush()


def test_new_merchant():
    # When I create a new merchant
    merchant = Merchant(
        name='Dat business!', zipcode=11249,
        email='dat@business.com',
        first_name='Ownerson', last_name='Moneymaker',
        address='708, Rua Duque de Caxias',
        phone='+1 (123) 456 7890')

    # Then I see that all the fields were set properly
    merchant.name.should.equal('Dat Business!')
    merchant.zipcode.should.equal(11249)
    merchant.email.should.equal('dat@business.com')
    merchant.address.should.equal('708, Rua Duque de Caxias')
    merchant.first_name.should.equal('Ownerson')
    merchant.last_name.should.equal('Moneymaker')
    merchant.phone.should.equal('+1 (123) 456 7890')


def test_create_merchant_with_no_email():
    # When I create try to create a new merchant with no email
    data = {
        'name': 'Dat business!',
        'zipcode': 11249,
        'first_name': 'Ownerson',
        'last_name': 'Moneymaker',
        'address': '708, Rua Duque de Caxias',
    }
    Merchant.when.called_with(data).should.throw(
        ValueError,
        "You cannot create a merchant without an email address")


def test_track_competitors():
    # Given that I have two merchants in my database
    merchant1 = Merchant(
        name='Dat business!', zip_code=11249, email='merchant1@blah.com')
    merchant2 = Merchant(
        name='Dat business!', zip_code=11249, email='merchant2@blah.com')

    # When one of them try to track the other one
    CompetitorTracker(merchant1).track(merchant2)

    # Then I see that the first merchant is now tracking the second one
    CompetitorTracker(merchant1).tracking().should.equal([
        merchant2,
    ])


def test_untrack_competitors():
    # Given that I have two merchants in my database and that the first
    # one tracks the other one
    merchant1 = Merchant(
        name='Dat business!', zip_code=11249, email='merchant1@blah.com')
    merchant2 = Merchant(
        name='Dat business!', zip_code=11249, email='merchant2@blah.com')
    CompetitorTracker(merchant1).track(merchant2)

    # When I untrack the second merchant from the first
    CompetitorTracker(merchant1).untrack(merchant2)

    # Then I see that the first merchant is not tracking the second one
    # anymore
    CompetitorTracker(merchant1).tracking().should.be.empty


def test_merchant_tags():
    # Given that I have one merchant in the db
    merchant = Merchant(
        name='Cool business!', zip_code=11211, email='merchant@business.com')

    # When I add a couple tags
    merchant.tags.append('Restaurants')
    merchant.tags.append('Dining & Nightlife')

    # Then I see that the tags were properly added
    merchant.tags.should.equal([
        Category.get(label='Restaurants'),
        Category.get(label='Dining & Nightlife'),
    ])


def test_merchant_tags_avoid_repeated():
    # Given that I have one merchant in the db
    merchant = Merchant(
        name='Cool business!', zip_code=11211, email='merchant@business.com')

    # When I add a couple tags (with dupplications)
    merchant.tags.append('Restaurants')
    merchant.tags.append('Restaurants')
    merchant.tags.append('Dining & Nightlife')

    # Then I see that the tags were properly added
    merchant.tags.should.equal([
        Category.get(label='Restaurants'),
        Category.get(label='Dining & Nightlife'),
    ])
