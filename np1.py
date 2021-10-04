import urllib.request, json

class expedition:
    def __init__(self, id, conveyance, programs, first, last):
        self.id = id
        self.conveyance = conveyance
        self.programs = programs
        self.first_sample = first
        self.last_sample = last

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=False, indent=None)

url = "https://api.npolar.no/marine/biology/sample/?q=&fields=expedition,utc_date,programs,conveyance&limit=all&format=json&variant=array"
response = urllib.request.urlopen(url).read()
samples = json.loads(response.decode('UTF-8'))

expeditions: list[expedition] = []

for sample in samples:
    existing = next((x for x in expeditions if x.id == sample['expedition']), None)
    if existing is None:
        expeditions.append(expedition(sample['expedition'], sample['conveyance'], sample.get('programs'), sample['utc_date'], sample['utc_date']))
    elif existing.last_sample < sample['utc_date']:
        existing.last_sample = sample['utc_date']
    elif existing.first_sample > sample['utc_date']:
        existing.first_sample = sample['utc_date']

for ex in expeditions:
    print(ex.toJSON())
