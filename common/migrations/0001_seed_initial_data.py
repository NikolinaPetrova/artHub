from django.db import migrations
from django.contrib.auth.hashers import make_password
from artworks.choices import ArtworkTypeChoices

def get_models(apps):
    ArtHubUser = apps.get_model('accounts', 'ArtHubUser')
    Album = apps.get_model('albums', 'Album')
    Artwork = apps.get_model('artworks', 'Artwork')
    Tag = apps.get_model('artworks', 'Tag')
    Comment = apps.get_model('artworks', 'Comment')
    ArtworkLike = apps.get_model('artworks', 'ArtworkLike')
    return ArtHubUser, Album, Artwork, Tag, Comment, ArtworkLike


def seed_data(apps, schema_editor):
    ArtHubUser, Album, Artwork, Tag, Comment, ArtworkLike = get_models(apps)

    alice = ArtHubUser.objects.create(
        username='alice',
        email='alice@example.com',
        password=make_password('123pass123'),
        first_name='Alice',
        last_name='Johnson',
        professional_artist=True,
    )

    dave = ArtHubUser.objects.create(
        username='dave',
        email='dave@example.com',
        password=make_password('123pass123'),
        first_name='Dave',
        last_name='Brown'
    )

    tag_names = [
        'mountains', 'sunrise', 'landscape', 'rocks', 'adventure',
        'alps', 'autumn', 'reflection', 'snow', 'winter', 'mist',
        'valley', 'photography', 'hills', 'sunset', 'forest', 'morning', 'lake',
        'digital', 'cityscape', 'futuristic', 'neon', 'cyberpunk', 'street',
        'galaxy', 'spaceship', 'concept art', 'samurai', 'character',
        'oasis', 'desert', 'dunes', 'city', 'urban',
    ]

    tags = {}
    for name in tag_names:
        tags[name] = Tag.objects.create(name=name)

    alice_default_album = Album.objects.create(
        name='Default Album',
        owner=alice
    )

    mountain_diaries = Album.objects.create(
        name='Mountain Diaries',
        owner=alice
    )

    dave_default_album = Album.objects.create(
        name='Default Album',
        owner=dave
    )

    digital = Album.objects.create(
        name='Digital Album',
        owner=dave
    )

    artworks_data = [
        {
            'title': 'Misty Mountain Sunrise',
            'description': 'A breathtaking view of the sun rising over misty mountain peaks, with warm light touching the valleys.',
            'image_url': 'https://images.unsplash.com/photo-1732106846688-3bac122e4f97?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': alice,
            'tags': ['mountains', 'sunrise', 'landscape'],
            'albums': [mountain_diaries]
        },

        {
            'title': 'Rocky Summit',
            'description': 'A dramatic capture of a jagged rocky mountain summit under a clear blue sky.',
            'image_url': 'https://plus.unsplash.com/premium_photo-1661962807023-6f593f2b5280?q=80&w=686&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': alice,
            'tags': ['mountains', 'rocks', 'adventure'],
            'albums': [mountain_diaries]
        },

        {
            'title': 'Autumn in the Alps',
            'description': 'Golden autumn foliage covering alpine slopes with a serene lake reflecting the mountains.',
            'image_url': 'https://plus.unsplash.com/premium_photo-1696420406361-6c37ab396779?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': alice,
            'tags': ['alps', 'autumn', 'reflection'],
            'albums': [mountain_diaries]
        },

        {
            'title': 'Snowy Peak',
            'description': 'A majestic snow-capped mountain peak with clouds swirling around the summit.',
            'image_url': 'https://images.unsplash.com/photo-1659379679173-4fc5618480d8?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': alice,
            'tags': ['snow', 'mountains', 'winter'],
            'albums': [mountain_diaries]
        },

        {
            'title': 'Misty Valley',
            'description': 'Early morning fog rolling through a green valley surrounded by towering mountain cliffs.',
            'image_url': 'https://plus.unsplash.com/premium_photo-1670098044482-514304849d6b?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': alice,
            'tags': ['mist', 'valley', 'mountains'],
            'albums': [mountain_diaries]
        },

        {
            'title': 'Golden Hour Hills',
            'description': 'A stunning photograph capturing rolling hills bathed in the golden light of sunset.',
            'image_url': 'https://plus.unsplash.com/premium_photo-1666211586960-fe75a0879882?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': alice,
            'tags': ['photography', 'hills', 'sunset', 'landscape'],
            'albums': [mountain_diaries]
        },

        {
            'title': 'Misty Forest Morning',
            'description': 'Early morning fog enveloping a dense forest, creating a serene and mysterious atmosphere.',
            'image_url': 'https://images.unsplash.com/photo-1648500856992-ed26e8ae952d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': alice,
            'tags': ['photography', 'forest', 'mist', 'morning'],
            'albums': [alice_default_album]
        },

        {
            'title': 'Mountain Reflection',
            'description': 'A crystal-clear lake perfectly reflecting the snow-capped mountains under a bright blue sky.',
            'image_url': 'https://images.unsplash.com/photo-1631045282678-e4712eaaa26e?q=80&w=1074&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': alice,
            'tags': ['photography', 'mountains', 'lake', 'reflection'],
            'albums': [alice_default_album, mountain_diaries]
        },

        {
            'title': 'Futuristic Cityscape',
            'description': 'A vibrant digital artwork of a futuristic city at night, full of neon lights and towering skyscrapers.',
            'image_url': 'https://plus.unsplash.com/premium_photo-1682124843954-eb395dfa50ea?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.DIGITAL,
            'user': dave,
            'tags': ['digital', 'cityscape', 'futuristic', 'neon'],
            'albums': [digital]
        },

        {
            'title': 'Cyberpunk Streets',
            'description': 'Digital painting showing a busy cyberpunk street scene with rain-soaked pavements and glowing signs.',
            'image_url': 'https://plus.unsplash.com/premium_photo-1685011233851-22c3f4e7412b?q=80&w=1332&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.DIGITAL,
            'user': dave,
            'tags': ['digital', 'cyberpunk', 'street', 'neon'],
            'albums': [digital]
        },

        {
            'title': 'Galactic Voyage',
            'description': 'Digital concept art of a spaceship navigating through a colorful galaxy filled with stars and planets.',
            'image_url': 'https://images.unsplash.com/photo-1763198217110-07b5350aa179?q=80&w=764&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.DIGITAL,
            'user': dave,
            'tags': ['digital', 'galaxy', 'spaceship', 'concept art'],
            'albums': [digital]
        },

        {
            'title': 'Technology',
            'description': "A close up of a person's face with red lights.",
            'image_url': 'https://plus.unsplash.com/premium_photo-1672759323620-51a2ee065aad?q=80&w=755&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.DIGITAL,
            'user': dave,
            'tags': ['digital', 'samurai', 'neon', 'character'],
            'albums': [digital]
        },

        {
            'title': 'Virtual Oasis',
            'description': 'Digital artwork of a serene oasis in a futuristic virtual landscape with holographic water and glowing plants.',
            'image_url': 'https://images.unsplash.com/photo-1684127947067-ced5282d5357?q=80&w=1169&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.DIGITAL,
            'user': dave,
            'tags': ['digital', 'oasis', 'futuristic', 'landscape'],
            'albums': [digital, dave_default_album]
        },

        {
            'title': 'Desert Dunes',
            'description': 'Golden desert dunes under dramatic skies, highlighting the textures and curves of the sand.',
            'image_url': 'https://images.unsplash.com/photo-1520440718111-45fe694b330a?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': dave,
            'tags': ['photography', 'desert', 'dunes', 'landscape'],
            'albums': [dave_default_album]
        },

        {
            'title': 'Urban Sunset',
            'description': 'City skyline photographed at sunset with glowing windows and warm ambient light.',
            'image_url': 'https://images.unsplash.com/photo-1667518158690-132bcb1f5095?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
            'type': ArtworkTypeChoices.PHOTOGRAPHY,
            'user': dave,
            'tags': ['photography', 'city', 'sunset', 'urban'],
            'albums': []
        }
    ]

    artworks_objects = {}

    for data in artworks_data:
        art = Artwork.objects.create(
            title=data['title'],
            description=data['description'],
            image_url=data['image_url'],
            type=data['type'],
            user=data['user'],
        )

        for tag_name in data['tags']:
            art.tags.add(tags[tag_name])

        for album in data['albums']:
            album.artworks.add(art)

        artworks_objects[data['title']] = art

    comment1 = Comment.objects.create(
        content='Incredible shot, love the light!',
        user=dave,
        artwork=artworks_objects['Misty Mountain Sunrise']
    )

    Comment.objects.create(
        content='Thank you!',
        user=alice,
        artwork=artworks_objects['Misty Mountain Sunrise'],
        parent=comment1,
    )

    comment2 = Comment.objects.create(
        content='Looks incredible up there!',
        user=dave,
        artwork=artworks_objects['Rocky Summit']
    )

    Comment.objects.create(
        content='Yes, it was!',
        user=alice,
        artwork=artworks_objects['Rocky Summit'],
        parent=comment2,
    )

    ArtworkLike.objects.create(
        artwork=artworks_objects['Misty Mountain Sunrise'],
        user=dave,
    )

    ArtworkLike.objects.create(
        artwork=artworks_objects['Rocky Summit'],
        user=dave,
    )


def reverse_seed(apps, schema_editor):
    ArtHubUser, Album, Artwork, Tag, Comment, ArtworkLike = get_models(apps)

    ArtworkLike.objects.all().delete()
    Comment.objects.all().delete()
    Artwork.objects.all().delete()
    Album.objects.all().delete()
    Tag.objects.all().delete()
    ArtHubUser.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('albums', '0001_initial'),
        ('artworks', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_seed),
    ]
