from django.test import TestCase, Client
from django.urls import reverse
from .models import Artist, Museum, Painting
import html


# Run this specific test class with
# python3 manage.py test app.tests.DatabaseTest
class DatabaseTest(TestCase):
    def setUp(self):
        self.artist1 = Artist.objects.create(
            first_name='Leonardo',
            last_name='da Vinci',
            year_born=1452,
            year_died=1519
        )

        self.artist2 = Artist.objects.create(
            first_name='Cindy',
            last_name='Sherman',
            year_born=1954,
            year_died=None
        )
        
        self.museum1 = Museum.objects.create(
            name='Le Louvre',
            address='Rue de Rivoli, 75001 Paris, France'
        )

        self.museum2 = Museum.objects.create(
            name="Musée d'Orsay",
            address="1 Rue de la Légion d'Honneur, 75007 Paris, France"
        )
        
        self.painting1 = Painting.objects.create(
            title='Mona Lisa',
            description='A portrait of a woman with an enigmatic smile',
            creation_year=1503,
            value=860_000_000,
            artist=self.artist1,
            museum=self.museum1
        )

        self.painting2 = Painting.objects.create(
            title='Untitled#53',
            description='Color photograph, a dark image of a puppet',
            creation_year=1985,
            value=1_000_000_001,
            artist=self.artist2,
            museum=self.museum1
        )

    def test_artist(self):
        # Test existing artist
        artist = Artist.objects.get(first_name='Leonardo')
        self.assertEqual(artist.last_name, 'da Vinci')
        self.assertEqual(str(artist), 'Leonardo da Vinci')
        self.assertFalse(artist.is_alive())
        print(artist.is_alive())

        artist = Artist.objects.get(first_name='Cindy')
        self.assertIsNone(artist.year_died)
        self.assertEqual(str(artist), 'Cindy Sherman')
        self.assertTrue(artist.is_alive())
        print(artist.is_alive())

    def test_museum(self):
        museum1 = Museum.objects.get(name='Le Louvre')
        museum2 = Museum.objects.get(name="Musée d'Orsay")
        self.assertEqual(str(museum1), 'Le Louvre')
        self.assertEqual(museum1.address, 'Rue de Rivoli, 75001 Paris, France')
        self.assertEqual(str(museum2), "Musée d'Orsay")
        self.assertEqual(museum2.address, "1 Rue de la Légion d'Honneur, 75007 Paris, France")

        # Test inventory_value()
        inventory_value1 = museum1.inventory_value()
        inventory_value2 = museum2.inventory_value()
        self.assertEqual(inventory_value1, 860_000_000 + 1_000_000_001)
        self.assertIsNone(inventory_value2, 0)

        # Test number_of_paintings()
        number_of_paintings1 = museum1.number_of_paintings()
        number_of_paintings2 = museum2.number_of_paintings()
        self.assertEqual(number_of_paintings1, 2)
        self.assertEqual(number_of_paintings2, 0)

        # Test number_of_paintings_on_display()
        number_of_paintings_on_display1 = museum1.number_of_paintings_on_display()
        number_of_paintings_on_display2 = museum2.number_of_paintings_on_display()
        self.assertEqual(number_of_paintings_on_display1, 2)
        self.assertEqual(number_of_paintings_on_display2, 0)

        # Test most_expensive_painting()
        most_expensive_painting1 = museum1.most_expensive_painting()
        most_expensive_painting2 = museum2.most_expensive_painting()
        self.assertEqual(most_expensive_painting1.title, 'Untitled#53')
        self.assertIsNone(most_expensive_painting2)

    def test_painting_model(self):
        painting = Painting.objects.get(title='Mona Lisa')

        self.assertTrue(painting.is_valid_value())

        painting.value = -100
        self.assertFalse(painting.is_valid_value())

        painting.value = 1_000_000_001
        self.assertFalse(painting.is_valid_value())

    def test_paintings_added_correctly(self):
        paintings = Painting.objects.all()

        self.assertEqual(paintings.count(), 2)

        painting1 = paintings.get(title='Mona Lisa')
        painting2 = paintings.get(title='Untitled#53')

        self.assertEqual(painting1.description, 'A portrait of a woman with an enigmatic smile')
        self.assertEqual(painting1.creation_year, 1503)
        self.assertEqual(painting1.value, 860_000_000)
        self.assertEqual(painting1.artist.first_name, 'Leonardo')
        self.assertEqual(painting1.artist.last_name, 'da Vinci')
        self.assertEqual(painting1.museum.name, 'Le Louvre')

        self.assertEqual(painting2.description, 'Color photograph, a dark image of a puppet')
        self.assertEqual(painting2.creation_year, 1985)
        self.assertEqual(painting2.value, 1_000_000_001)
        self.assertEqual(painting2.artist.first_name, 'Cindy')
        self.assertEqual(painting2.artist.last_name, 'Sherman')
        self.assertEqual(painting2.museum.name, 'Le Louvre')



class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.artist1 = Artist.objects.create(
            first_name='Leonardo',
            last_name='da Vinci',
            year_born=1452,
            year_died=1519
        )

        self.artist2 = Artist.objects.create(
            first_name='Cindy',
            last_name='Sherman',
            year_born=1954,
            year_died=None
        )

        self.museum1 = Museum.objects.create(
            name='Le Louvre',
            address='Rue de Rivoli, 75001 Paris, France'
        )

        self.museum2 = Museum.objects.create(
            name="Musée d'Orsay",
            address="1 Rue de la Légion d'Honneur, 75007 Paris, France"
        )

        self.painting1 = Painting.objects.create(
            title='Mona Lisa',
            description='A portrait of a woman with an enigmatic smile',
            creation_year=1503,
            value=860_000_000,
            artist=self.artist1,
            museum=self.museum1
        )

        self.painting2 = Painting.objects.create(
            title='Untitled#53',
            description='Color photograph, a dark image of a puppet <script>alert(42)</script>',
            creation_year=1985,
            value=1_000_000_001,
            artist=self.artist2,
            museum=self.museum1
        )

    def test_list_museums(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Le Louvre')
        self.assertContains(response, html.escape("Musée d'Orsay"))

    def test_list_museum_paintings(self):
        response = self.client.get(reverse('paintings', args=[self.museum1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mona Lisa')

        # Test with non-existent museum
        response = self.client.get(reverse('paintings', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_search(self):
        # Search painting
        response = self.client.get(reverse('search'), {'q': 'Mona Lisa'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mona Lisa')

        # Search artist
        response = self.client.get(reverse('search'), {'q': 'Cindy Sherman'})
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'Untitled#53')

        # More inclusive searches
        response = self.client.get(reverse('search'), {'q': 'mona lisa'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mona Lisa')
        response = self.client.get(reverse('search'), {'q': 'Lisa'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mona Lisa')
        response = self.client.get(reverse('search'), {'q': 'Leonardo'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mona Lisa')
        response = self.client.get(reverse('search'), {'q': 'L'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mona Lisa')
        self.assertContains(response, 'Untitled#53')

        # Test with non-existent painting
        # make sure "No paintings found" is displayed in the output
        response = self.client.get(reverse('search'), {'q': 'Non-existent painting'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No paintings found')


    def test_painting_info(self):
        response = self.client.get(reverse('painting_info', args=[self.painting1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'title': 'Mona Lisa',
                'description': 'A portrait of a woman with an enigmatic smile',
                'creation_year': 1503,
                'image': '/media/paintings/default.jpg',
                'value': 860_000_000,
                'is_on_display': True,
                'artist': 'Leonardo da Vinci',
                'museum': 'Le Louvre'
            }
        )

        # Test with non-existent painting
        response = self.client.get(reverse('painting_info', args=[9999]))
        self.assertEqual(response.status_code, 404)

        # Make sure special characters in html are escaped
        # Might have to use the html package here
        response = self.client.get(reverse('painting_info', args=[self.painting2.id]))
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {
                'title': 'Untitled#53',
                'description': 'Color photograph, a dark image of a puppet &lt;script&gt;alert(42)&lt;/script&gt;',
                'creation_year': 1985,
                'image': '/media/paintings/default.jpg',
                'value': 1_000_000_001,
                'is_on_display': True,
                'artist': 'Cindy Sherman',
                'museum': 'Le Louvre'
            }
        )
